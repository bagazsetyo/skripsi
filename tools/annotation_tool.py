#!/usr/bin/env python3
"""
Annotation Tool — Tambah gambar + bounding box ke dataset traffic sign.

Cara pakai:
    python tools/annotation_tool.py

Keyboard:
    Ctrl+O          Buka gambar
    Ctrl+S          Simpan ke dataset
    Delete          Hapus anotasi yang dipilih di list
    Escape          Batalkan drag bbox yang sedang digambar
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from typing import List, Optional, Tuple

from PIL import Image, ImageTk

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from config import CLASS_LABEL_TO_ID, CLASS_NAMES, DATA_DIR

# Warna bbox berurutan per indeks anotasi
BBOX_COLORS = [
    "#e74c3c", "#2ecc71", "#3498db", "#f39c12",
    "#9b59b6", "#1abc9c", "#e67e22", "#16a085",
]
MIN_BOX_PX = 8   # ukuran minimum bbox di canvas (pixel) agar tidak accidental click
PANEL_W    = 270 # lebar panel kanan (pixel)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

class Annotation:
    """Satu bounding box pada gambar, beserta labelnya."""

    def __init__(self, label: str, box: Tuple[int, int, int, int]) -> None:
        self.label = label
        # box = (x1, y1, x2, y2) dalam koordinat gambar asli (pixel)
        x1, y1, x2, y2 = box
        self.box: Tuple[int, int, int, int] = (
            min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        )

    def to_yolo_line(self, img_w: int, img_h: int) -> str:
        x1, y1, x2, y2 = self.box
        cx = (x1 + x2) / 2.0 / img_w
        cy = (y1 + y2) / 2.0 / img_h
        w  = (x2 - x1) / img_w
        h  = (y2 - y1) / img_h
        cid = CLASS_LABEL_TO_ID[self.label]
        return f"{cid} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"

    def summary(self, index: int) -> str:
        x1, y1, x2, y2 = self.box
        short = self.label.split("-")[-1]
        return f"{index}. {short}  [{x1},{y1} → {x2},{y2}]"


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class AnnotationTool(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Annotation Tool — Traffic Sign Dataset")
        self.minsize(860, 540)

        # State gambar
        self._image_path:  Optional[Path]             = None
        self._orig_image:  Optional[Image.Image]      = None
        self._tk_image:    Optional[ImageTk.PhotoImage] = None
        self._scale:       float                      = 1.0
        self._off_x:       int                        = 0
        self._off_y:       int                        = 0

        # State drag
        self._drag_start:   Optional[Tuple[int, int]] = None
        self._drag_rect_id: Optional[int]             = None

        # Anotasi
        self._annotations: List[Annotation] = []

        self._build_ui()
        self._bind_keys()
        self._set_status("Buka gambar untuk mulai anotasi.  |  Ctrl+O = buka  |  Ctrl+S = simpan")

    # -----------------------------------------------------------------------
    # UI builder
    # -----------------------------------------------------------------------

    def _build_ui(self) -> None:
        # ── Top bar ────────────────────────────────────────────────────────
        top = tk.Frame(self, pady=5, padx=8, bg="#2c3e50")
        top.pack(fill=tk.X)

        tk.Button(
            top, text="  Buka Gambar  ", command=self.cmd_open,
            bg="#3498db", fg="white", relief=tk.FLAT, padx=8, pady=3,
        ).pack(side=tk.LEFT)

        self._lbl_file = tk.Label(
            top, text="(belum ada gambar)", anchor="w",
            fg="#bdc3c7", bg="#2c3e50", font=("", 9),
        )
        self._lbl_file.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self._lbl_size = tk.Label(
            top, text="", anchor="e",
            fg="#7f8c8d", bg="#2c3e50", font=("", 9),
        )
        self._lbl_size.pack(side=tk.RIGHT, padx=8)

        # ── Main area ──────────────────────────────────────────────────────
        body = tk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Canvas
        canvas_wrap = tk.LabelFrame(body, text=" Gambar — klik-drag untuk menambah bbox ")
        canvas_wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(canvas_wrap, bg="#1a1a2e", cursor="crosshair")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<ButtonPress-1>",   self._on_press)
        self._canvas.bind("<B1-Motion>",        self._on_drag)
        self._canvas.bind("<ButtonRelease-1>",  self._on_release)
        self._canvas.bind("<Configure>",        self._on_canvas_resize)

        # ── Right panel ───────────────────────────────────────────────────
        panel = tk.Frame(body, width=PANEL_W, bg="#ecf0f1")
        panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(6, 0))
        panel.pack_propagate(False)

        # Kelas
        frm_cls = tk.LabelFrame(panel, text=" Kelas ", padx=6, pady=6)
        frm_cls.pack(fill=tk.X, pady=(0, 6))

        self._var_class = tk.StringVar(value=CLASS_NAMES[0])
        self._cmb_class = ttk.Combobox(
            frm_cls, textvariable=self._var_class,
            values=CLASS_NAMES, state="readonly",
        )
        self._cmb_class.pack(fill=tk.X)

        # Split
        frm_split = tk.LabelFrame(panel, text=" Simpan ke Split ", padx=6, pady=6)
        frm_split.pack(fill=tk.X, pady=(0, 6))

        self._var_split = tk.StringVar(value="train")
        for s in ("train", "test"):
            tk.Radiobutton(
                frm_split, text=s.capitalize(),
                variable=self._var_split, value=s,
            ).pack(side=tk.LEFT, padx=10)

        # Preview path
        self._lbl_dest = tk.Label(
            panel, text="", anchor="w", fg="#7f8c8d",
            font=("", 8), wraplength=PANEL_W - 16, justify=tk.LEFT,
        )
        self._lbl_dest.pack(fill=tk.X, padx=6)
        self._var_class.trace_add("write",  lambda *_: self._update_dest_preview())
        self._var_split.trace_add("write",  lambda *_: self._update_dest_preview())

        # Anotasi list
        frm_ann = tk.LabelFrame(panel, text=" Anotasi ", padx=4, pady=4)
        frm_ann.pack(fill=tk.BOTH, expand=True, pady=(6, 4))

        scrollbar = tk.Scrollbar(frm_ann)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._listbox = tk.Listbox(
            frm_ann, yscrollcommand=scrollbar.set,
            font=("Consolas", 9), selectmode=tk.SINGLE,
            activestyle="dotbox",
        )
        self._listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self._listbox.yview)

        # Buttons
        frm_btn = tk.Frame(panel, pady=4)
        frm_btn.pack(fill=tk.X, padx=4)

        tk.Button(
            frm_btn, text="Hapus Dipilih",
            command=self.cmd_delete_selected,
            fg="#e74c3c", relief=tk.GROOVE,
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            frm_btn, text="Hapus Semua",
            command=self.cmd_clear_all,
            fg="#c0392b", relief=tk.GROOVE,
        ).pack(fill=tk.X, pady=2)

        ttk.Separator(frm_btn).pack(fill=tk.X, pady=6)

        tk.Button(
            frm_btn, text="  Simpan ke Dataset  ",
            command=self.cmd_save,
            bg="#27ae60", fg="white",
            font=("", 10, "bold"), pady=6, relief=tk.FLAT,
        ).pack(fill=tk.X)

        # ── Status bar ────────────────────────────────────────────────────
        self._lbl_status = tk.Label(
            self, text="", anchor="w",
            bg="#dfe6e9", relief=tk.SUNKEN, padx=8, pady=3,
            font=("", 9),
        )
        self._lbl_status.pack(fill=tk.X, side=tk.BOTTOM)

        self._update_dest_preview()

    def _bind_keys(self) -> None:
        self.bind("<Control-o>", lambda _: self.cmd_open())
        self.bind("<Control-s>", lambda _: self.cmd_save())
        self.bind("<Delete>",    lambda _: self.cmd_delete_selected())
        self.bind("<Escape>",    self._cancel_drag)

    # -----------------------------------------------------------------------
    # Commands
    # -----------------------------------------------------------------------

    def cmd_open(self) -> None:
        path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[
                ("Gambar", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("Semua File", "*.*"),
            ],
        )
        if not path:
            return

        self._image_path = Path(path)
        try:
            self._orig_image = Image.open(path).convert("RGB")
        except Exception as exc:
            messagebox.showerror("Gagal membuka gambar", str(exc))
            return

        self._annotations.clear()
        self._refresh_listbox()
        self._lbl_file.config(text=self._image_path.name)
        w, h = self._orig_image.size
        self._lbl_size.config(text=f"{w} × {h} px")
        self._render()
        self._set_status(f"Gambar dimuat: {self._image_path.name}  ({w}×{h} px)")

    def cmd_delete_selected(self) -> None:
        sel = self._listbox.curselection()
        idx = sel[0] if sel else (len(self._annotations) - 1 if self._annotations else -1)
        if idx < 0:
            return
        removed = self._annotations.pop(idx)
        self._refresh_listbox()
        self._render()
        self._set_status(f"Anotasi dihapus: {removed.summary(idx + 1)}")

    def cmd_clear_all(self) -> None:
        if not self._annotations:
            return
        if messagebox.askyesno("Hapus Semua", "Hapus semua anotasi pada gambar ini?"):
            self._annotations.clear()
            self._refresh_listbox()
            self._render()
            self._set_status("Semua anotasi dihapus.")

    def cmd_save(self) -> None:
        if self._orig_image is None or self._image_path is None:
            messagebox.showwarning("Tidak ada gambar", "Buka gambar terlebih dahulu.")
            return
        if not self._annotations:
            messagebox.showwarning("Tidak ada anotasi", "Tambahkan minimal satu bounding box.")
            return

        label = self._var_class.get()
        split = self._var_split.get()

        dest_dir = DATA_DIR / split / label
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Nama file unik — hindari tabrakan dengan yang sudah ada
        suffix = self._image_path.suffix.lower()
        if suffix not in {".jpg", ".jpeg", ".png", ".bmp"}:
            suffix = ".jpg"
        stem = self._image_path.stem
        ts = int(time.time() * 1000) % 1_000_000
        dest_img = dest_dir / f"{stem}_{ts}{suffix}"
        while dest_img.exists():
            ts += 1
            dest_img = dest_dir / f"{stem}_{ts}{suffix}"

        # Simpan gambar
        try:
            self._orig_image.save(dest_img)
        except Exception as exc:
            messagebox.showerror("Gagal menyimpan gambar", str(exc))
            return

        # Tulis anotasi YOLO — semua bbox pakai class_id dari label folder
        iw, ih = self._orig_image.size
        lines = []
        for ann in self._annotations:
            # Override label ke class yang dipilih agar konsisten dengan folder
            forced = Annotation(label, ann.box)
            lines.append(forced.to_yolo_line(iw, ih))

        dest_txt = dest_img.with_suffix(".txt")
        dest_txt.write_text("\n".join(lines), encoding="utf-8")

        rel = dest_img.relative_to(REPO_ROOT)
        messagebox.showinfo(
            "Tersimpan",
            f"Gambar dan label berhasil disimpan.\n\n"
            f"File  : {rel}\n"
            f"Kelas : {label}\n"
            f"Split : {split}\n"
            f"BBox  : {len(self._annotations)} anotasi\n\n"
            f"Label YOLO ditulis ke:\n{dest_txt.name}",
        )
        self._set_status(
            f"Tersimpan → {dest_img.name}  |  "
            f"kelas={label}  split={split}  bbox={len(self._annotations)}"
        )

    # -----------------------------------------------------------------------
    # Canvas rendering
    # -----------------------------------------------------------------------

    def _on_canvas_resize(self, _event: tk.Event) -> None:
        if self._orig_image:
            self.after(10, self._render)

    def _render(self) -> None:
        if self._orig_image is None:
            return
        cw = max(self._canvas.winfo_width(),  1)
        ch = max(self._canvas.winfo_height(), 1)
        iw, ih = self._orig_image.size

        self._scale = min(cw / iw, ch / ih)
        nw = int(iw * self._scale)
        nh = int(ih * self._scale)
        self._off_x = (cw - nw) // 2
        self._off_y = (ch - nh) // 2

        resized = self._orig_image.resize((nw, nh), Image.LANCZOS)
        self._tk_image = ImageTk.PhotoImage(resized)
        self._canvas.delete("all")
        self._canvas.create_image(self._off_x, self._off_y, anchor=tk.NW, image=self._tk_image)
        self._draw_all_boxes()

    def _draw_all_boxes(self) -> None:
        selected_idx = -1
        sel = self._listbox.curselection()
        if sel:
            selected_idx = sel[0]

        for i, ann in enumerate(self._annotations):
            color = BBOX_COLORS[i % len(BBOX_COLORS)]
            cx1, cy1 = self._img_to_canvas(ann.box[0], ann.box[1])
            cx2, cy2 = self._img_to_canvas(ann.box[2], ann.box[3])
            width = 3 if i == selected_idx else 2

            self._canvas.create_rectangle(
                cx1, cy1, cx2, cy2,
                outline=color, width=width, tags="bbox",
            )
            # Label pill
            short = ann.label.split("-")[-1]
            pill_x2 = cx1 + len(short) * 7 + 14
            pill_y1 = cy1 - 18
            self._canvas.create_rectangle(
                cx1, pill_y1, pill_x2, cy1,
                fill=color, outline="", tags="bbox",
            )
            self._canvas.create_text(
                cx1 + 5, cy1 - 9,
                text=short, fill="white", anchor=tk.W,
                font=("", 9), tags="bbox",
            )

    # -----------------------------------------------------------------------
    # Mouse events
    # -----------------------------------------------------------------------

    def _on_press(self, event: tk.Event) -> None:
        if self._orig_image is None:
            return
        self._drag_start = (event.x, event.y)

    def _on_drag(self, event: tk.Event) -> None:
        if self._drag_start is None:
            return
        if self._drag_rect_id is not None:
            self._canvas.delete(self._drag_rect_id)
        sx, sy = self._drag_start
        self._drag_rect_id = self._canvas.create_rectangle(
            sx, sy, event.x, event.y,
            outline="#f1c40f", width=2, dash=(5, 3),
        )
        # Tampilkan ukuran box sementara di status bar
        ix1, iy1 = self._canvas_to_img(min(sx, event.x), min(sy, event.y))
        ix2, iy2 = self._canvas_to_img(max(sx, event.x), max(sy, event.y))
        self._set_status(
            f"Menggambar bbox ...  [{ix1},{iy1}] → [{ix2},{iy2}]  "
            f"({ix2-ix1}×{iy2-iy1} px)  |  Esc = batal"
        )

    def _on_release(self, event: tk.Event) -> None:
        if self._drag_start is None or self._orig_image is None:
            return
        sx, sy = self._drag_start
        self._drag_start    = None
        if self._drag_rect_id is not None:
            self._canvas.delete(self._drag_rect_id)
            self._drag_rect_id = None

        # Abaikan klik tanpa drag
        if abs(event.x - sx) < MIN_BOX_PX or abs(event.y - sy) < MIN_BOX_PX:
            self._set_status("Bbox terlalu kecil, diabaikan.  Klik-drag lebih jauh.")
            return

        ix1, iy1 = self._canvas_to_img(min(sx, event.x), min(sy, event.y))
        ix2, iy2 = self._canvas_to_img(max(sx, event.x), max(sy, event.y))

        ann = Annotation(self._var_class.get(), (ix1, iy1, ix2, iy2))
        self._annotations.append(ann)
        self._refresh_listbox()
        self._listbox.selection_clear(0, tk.END)
        self._listbox.selection_set(len(self._annotations) - 1)
        self._listbox.see(tk.END)
        self._draw_all_boxes()
        self._set_status(
            f"Bbox {len(self._annotations)} ditambahkan  "
            f"[{ix1},{iy1}→{ix2},{iy2}]  ({ix2-ix1}×{iy2-iy1} px)"
        )

    def _cancel_drag(self, _event: tk.Event) -> None:
        self._drag_start = None
        if self._drag_rect_id is not None:
            self._canvas.delete(self._drag_rect_id)
            self._drag_rect_id = None
        self._set_status("Drag dibatalkan.")

    # -----------------------------------------------------------------------
    # Coordinate helpers
    # -----------------------------------------------------------------------

    def _img_to_canvas(self, x: int, y: int) -> Tuple[int, int]:
        return int(x * self._scale) + self._off_x, int(y * self._scale) + self._off_y

    def _canvas_to_img(self, cx: int, cy: int) -> Tuple[int, int]:
        x = int((cx - self._off_x) / self._scale)
        y = int((cy - self._off_y) / self._scale)
        if self._orig_image:
            x = max(0, min(x, self._orig_image.width  - 1))
            y = max(0, min(y, self._orig_image.height - 1))
        return x, y

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _refresh_listbox(self) -> None:
        self._listbox.delete(0, tk.END)
        for i, ann in enumerate(self._annotations, start=1):
            self._listbox.insert(tk.END, ann.summary(i))
        if self._annotations:
            self._listbox.see(tk.END)

    def _update_dest_preview(self) -> None:
        label = self._var_class.get()
        split = self._var_split.get()
        rel = Path("data") / "traffic_sign" / split / label
        self._lbl_dest.config(text=f"Tujuan: {rel}/")

    def _set_status(self, msg: str) -> None:
        self._lbl_status.config(text=f"  {msg}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    app = AnnotationTool()
    app.mainloop()


if __name__ == "__main__":
    main()
