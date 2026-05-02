from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import REGISTRY_DB_PATH


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _connect(db_path: Path = REGISTRY_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def get_connection(db_path: Path = REGISTRY_DB_PATH):
    connection = _connect(db_path)
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_db(db_path: Path = REGISTRY_DB_PATH) -> None:
    with get_connection(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT NOT NULL UNIQUE,
                display_name TEXT NOT NULL,
                model_name TEXT NOT NULL,
                path TEXT NOT NULL,
                status TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 0,
                class_names_json TEXT NOT NULL,
                metrics_json TEXT,
                config_json TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS training_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_name TEXT NOT NULL,
                status TEXT NOT NULL,
                selected_classes_json TEXT NOT NULL,
                request_json TEXT NOT NULL,
                output_dir TEXT NOT NULL,
                model_id INTEGER,
                metrics_json TEXT,
                error_message TEXT,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(model_id) REFERENCES models(id)
            )
            """
        )


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True)


def _row_to_model(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    return {
        "id": row["id"],
        "version": row["version"],
        "display_name": row["display_name"],
        "model_name": row["model_name"],
        "path": row["path"],
        "status": row["status"],
        "is_active": bool(row["is_active"]),
        "class_names": json.loads(row["class_names_json"]),
        "metrics": json.loads(row["metrics_json"]) if row["metrics_json"] else None,
        "config": json.loads(row["config_json"]) if row["config_json"] else None,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _row_to_training_run(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    return {
        "id": row["id"],
        "run_name": row["run_name"],
        "status": row["status"],
        "selected_classes": json.loads(row["selected_classes_json"]),
        "request": json.loads(row["request_json"]),
        "output_dir": row["output_dir"],
        "model_id": row["model_id"],
        "metrics": json.loads(row["metrics_json"]) if row["metrics_json"] else None,
        "error_message": row["error_message"],
        "started_at": row["started_at"],
        "completed_at": row["completed_at"],
        "updated_at": row["updated_at"],
    }


def list_models() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM models ORDER BY created_at DESC, id DESC"
        ).fetchall()
    return [_row_to_model(row) for row in rows]


def get_model(model_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM models WHERE id = ?", (model_id,)
        ).fetchone()
    return _row_to_model(row)


def get_model_by_version(version: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM models WHERE version = ?", (version,)
        ).fetchone()
    return _row_to_model(row)


def get_active_model() -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM models WHERE is_active = 1 ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return _row_to_model(row)


def upsert_model(
    *,
    version: str,
    display_name: str,
    model_name: str,
    path: str,
    status: str,
    class_names: list[str],
    metrics: dict | None = None,
    config: dict | None = None,
    is_active: bool = False,
) -> dict:
    existing = get_model_by_version(version)
    now = utc_now()
    with get_connection() as connection:
        if is_active:
            connection.execute("UPDATE models SET is_active = 0")
        if existing is None:
            connection.execute(
                """
                INSERT INTO models (
                    version, display_name, model_name, path, status, is_active,
                    class_names_json, metrics_json, config_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    version,
                    display_name,
                    model_name,
                    path,
                    status,
                    int(is_active),
                    _json_dump(class_names),
                    _json_dump(metrics) if metrics is not None else None,
                    _json_dump(config) if config is not None else None,
                    now,
                    now,
                ),
            )
        else:
            connection.execute(
                """
                UPDATE models
                SET display_name = ?, model_name = ?, path = ?, status = ?, is_active = ?,
                    class_names_json = ?, metrics_json = ?, config_json = ?, updated_at = ?
                WHERE version = ?
                """,
                (
                    display_name,
                    model_name,
                    path,
                    status,
                    int(is_active),
                    _json_dump(class_names),
                    _json_dump(metrics) if metrics is not None else _json_dump(existing["metrics"]),
                    _json_dump(config) if config is not None else _json_dump(existing["config"]),
                    now,
                    version,
                ),
            )
    return get_model_by_version(version)


def set_active_model(model_id: int) -> dict | None:
    with get_connection() as connection:
        connection.execute("UPDATE models SET is_active = 0")
        connection.execute(
            "UPDATE models SET is_active = 1, updated_at = ? WHERE id = ?",
            (utc_now(), model_id),
        )
    return get_model(model_id)


def create_training_run(
    *,
    run_name: str,
    selected_classes: list[str],
    request: dict,
    output_dir: str,
    status: str = "queued",
) -> dict:
    now = utc_now()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO training_runs (
                run_name, status, selected_classes_json, request_json,
                output_dir, started_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_name,
                status,
                _json_dump(selected_classes),
                _json_dump(request),
                output_dir,
                now,
                now,
            ),
        )
        run_id = cursor.lastrowid
    return get_training_run(run_id)


def get_training_run(run_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM training_runs WHERE id = ?", (run_id,)
        ).fetchone()
    return _row_to_training_run(row)


def list_training_runs() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM training_runs ORDER BY started_at DESC, id DESC"
        ).fetchall()
    return [_row_to_training_run(row) for row in rows]


def update_training_run(
    run_id: int,
    *,
    status: str | None = None,
    model_id: int | None = None,
    metrics: dict | None = None,
    error_message: str | None = None,
    completed_at: str | None = None,
) -> dict | None:
    existing = get_training_run(run_id)
    if existing is None:
        return None

    next_status = status or existing["status"]
    next_model_id = model_id if model_id is not None else existing["model_id"]
    next_metrics = metrics if metrics is not None else existing["metrics"]
    next_error_message = error_message
    next_completed_at = completed_at if completed_at is not None else existing["completed_at"]

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE training_runs
            SET status = ?, model_id = ?, metrics_json = ?, error_message = ?,
                completed_at = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                next_status,
                next_model_id,
                _json_dump(next_metrics) if next_metrics is not None else None,
                next_error_message,
                next_completed_at,
                utc_now(),
                run_id,
            ),
        )
    return get_training_run(run_id)
