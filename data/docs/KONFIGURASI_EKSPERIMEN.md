# Konfigurasi Eksperimen — YOLOS-small (img500 / img600 / img700)

Semua preset menggunakan model `hustvl/yolos-small` dan dataset yang sama
(18 kelas, 5.494 train / 540 test). Satu-satunya variabel yang berbeda adalah
**image size**. Seluruh parameter lain identik.

---

## Tabel Konfigurasi

| Parameter | small-img500 | small-img600 | small-img700 |
|-----------|:------------:|:------------:|:------------:|
| **Image Size** | 500 px | 600 px | 700 px |
| **Batch Size** | 2 | 2 | 2 |
| **Epochs** | 40 | 40 | 40 |
| **Learning Rate** | 5×10⁻⁵ | 5×10⁻⁵ | 5×10⁻⁵ |
| **LR Warmup Epochs** | 4 | 4 | 4 |
| **LR Scheduler** | Cosine Decay | Cosine Decay | Cosine Decay |
| **Weight Decay** | 1×10⁻⁴ | 1×10⁻⁴ | 1×10⁻⁴ |
| **Gradient Clipping** | 0.1 | 0.1 | 0.1 |
| **Score Threshold** | 0.3 | 0.3 | 0.3 |
| **Mixed Precision (AMP)** | Ya | Ya | Ya |
| **Num Workers** | 4 | 4 | 4 |
| **GPU** | A100 80 GB | A100 80 GB | A100 80 GB |
| **VRAM (terukur/est.)** | ~35 GB est. | ~43 GB ✓ | ~46–50 GB ✓ |
| **Est. Durasi Training** | ~8.8 jam est. | ~8.75 jam ✓ | ~8.8 jam est. |

---

## Cara Menjalankan di Google Colab

```python
# img500
!python experiment_runner.py --preset small-img500

# img600
!python experiment_runner.py --preset small-img600

# img700
!python experiment_runner.py --preset small-img700
```

---

## Catatan

- **Ketiga config identik** (bs=2, LR=5e-5, epochs=40) — satu-satunya variabel
  yang berbeda adalah image size, sehingga perbandingan benar-benar fair.
- **Per-epoch img700 ≈ img600** (~793s vs ~788s, terukur aktual) — bottleneck
  bukan di attention/patch tapi di I/O dan preprocessing.
- **Config didasarkan pada model `yolos-600---small-latest`** yang sudah di-training
  dan menghasilkan mAP@0.5 = **92.07%**, Precision = 94.16%, Recall = 92.31%.
- img700 terukur ~46–50 GB VRAM di A100 80 GB saat training.
