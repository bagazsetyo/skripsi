from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from config import (
    CLASS_NAMES,
    DEFAULT_BATCH_SIZE,
    DEFAULT_EPOCHS,
    DEFAULT_IMAGE_SIZE,
    DEFAULT_LEARNING_RATE,
    DEFAULT_TRAIN_MODEL_NAME,
    DEFAULT_WEIGHT_DECAY,
)


class TrainingRequest(BaseModel):
    run_name: str = Field(min_length=1, max_length=100)
    output_version: str | None = Field(default=None, max_length=100)
    selection_mode: Literal["all", "subset"] = "all"
    selected_classes: list[str] = Field(default_factory=list)
    model_name: str = DEFAULT_TRAIN_MODEL_NAME
    image_size: int = Field(default=DEFAULT_IMAGE_SIZE, ge=224, le=1024)
    epochs: int = Field(default=DEFAULT_EPOCHS, ge=1, le=500)
    batch_size: int = Field(default=DEFAULT_BATCH_SIZE, ge=1, le=64)
    learning_rate: float = Field(default=DEFAULT_LEARNING_RATE, gt=0)
    weight_decay: float = Field(default=DEFAULT_WEIGHT_DECAY, ge=0)
    num_workers: int = Field(default=2, ge=0, le=16)
    lr_step: int = Field(default=0, ge=0)
    lr_gamma: float = Field(default=0.5, gt=0)
    use_amp: bool = True
    activate_after_training: bool = True
    score_threshold: float = Field(default=0.5, ge=0, le=1)

    @model_validator(mode="after")
    def validate_selected_classes(self):
        if self.selection_mode == "all":
            self.selected_classes = list(CLASS_NAMES)
            return self

        if not self.selected_classes:
            raise ValueError("selected_classes must not be empty for subset mode")

        invalid = sorted(set(self.selected_classes) - set(CLASS_NAMES))
        if invalid:
            raise ValueError(f"Unknown classes: {invalid}")

        seen: set[str] = set()
        normalized: list[str] = []
        for class_name in self.selected_classes:
            if class_name in seen:
                continue
            seen.add(class_name)
            normalized.append(class_name)
        self.selected_classes = normalized
        return self


class ActivateModelRequest(BaseModel):
    model_id: int


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=100)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str


class PredictionResponse(BaseModel):
    model_id: int | None
    model_version: str | None
    model_display_name: str | None
    score_threshold: float
    image_width: int
    image_height: int
    detections: list[dict]
