from __future__ import annotations


def build_annotate_html(class_names: list[str]) -> str:
    classes_js = str(class_names).replace("'", '"')
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Annotation Tool — Traffic Sign</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      --accent: #0f766e;
      --danger: #be123c;
      --border: #dbe3f0;
      --bg: #f4f6fb;
      --card: #ffffff;
      --muted: #64748b;
    }}
    body {{ background: var(--bg); color: #1f2937; height: 100vh; display: flex; flex-direction: column; }}

    /* ── Top bar ── */
    .topbar {{
      background: #1e293b;
      color: #f1f5f9;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 14px;
      flex-shrink: 0;
    }}
    .topbar h1 {{ font-size: 18px; font-weight: 700; }}
    .topbar .sub {{ font-size: 13px; color: #94a3b8; }}

    /* ── Main layout ── */
    .workspace {{
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 280px;
      gap: 0;
      overflow: hidden;
    }}

    /* ── Canvas area ── */
    .canvas-area {{
      background: #1a1a2e;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }}
    .canvas-toolbar {{
      background: #0f172a;
      padding: 8px 12px;
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }}
    .canvas-toolbar label {{
      background: #3b82f6;
      color: white;
      padding: 6px 14px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      white-space: nowrap;
    }}
    .canvas-toolbar input[type=file] {{ display: none; }}
    .file-name {{
      color: #94a3b8;
      font-size: 13px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .canvas-wrap {{
      flex: 1;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }}
    #mainCanvas {{
      cursor: crosshair;
      display: block;
      max-width: 100%;
      max-height: 100%;
    }}
    .hint {{
      position: absolute;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0,0,0,.6);
      color: #e2e8f0;
      font-size: 12px;
      padding: 4px 12px;
      border-radius: 20px;
      pointer-events: none;
      white-space: nowrap;
    }}

    /* ── Right panel ── */
    .panel {{
      background: var(--card);
      border-left: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .panel-section {{
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      flex-shrink: 0;
    }}
    .panel-section h3 {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .05em;
      color: var(--muted);
      margin-bottom: 8px;
    }}
    select, .radio-row {{
      width: 100%;
      padding: 8px 10px;
      border: 1px solid var(--border);
      border-radius: 8px;
      font: inherit;
      font-size: 13px;
      background: #f8fafc;
    }}
    .radio-row {{
      display: flex;
      gap: 20px;
      align-items: center;
      padding: 8px 10px;
    }}
    .radio-row label {{ display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 13px; }}
    .dest-preview {{
      font-size: 11px;
      color: var(--muted);
      margin-top: 6px;
      word-break: break-all;
    }}

    /* ── Annotation list ── */
    .ann-list-wrap {{
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }}
    .ann-empty {{
      color: var(--muted);
      font-size: 13px;
      text-align: center;
      padding: 24px 0;
    }}
    .ann-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 8px;
      border-radius: 8px;
      margin-bottom: 4px;
      border: 1px solid var(--border);
      background: #f8fafc;
      font-size: 12px;
    }}
    .ann-item.selected {{ border-color: #3b82f6; background: #eff6ff; }}
    .ann-dot {{
      width: 12px; height: 12px;
      border-radius: 3px;
      flex-shrink: 0;
    }}
    .ann-text {{ flex: 1; overflow: hidden; }}
    .ann-label {{ font-weight: 600; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .ann-coords {{ color: var(--muted); }}
    .ann-del {{
      background: none;
      border: none;
      color: var(--danger);
      cursor: pointer;
      font-size: 16px;
      line-height: 1;
      padding: 0 2px;
      flex-shrink: 0;
    }}

    /* ── Bottom buttons ── */
    .panel-footer {{ padding: 12px 16px; border-top: 1px solid var(--border); display: grid; gap: 8px; flex-shrink: 0; }}
    .btn {{
      display: block;
      width: 100%;
      padding: 10px;
      border: none;
      border-radius: 10px;
      font: inherit;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
    }}
    .btn-primary {{ background: var(--accent); color: white; font-size: 14px; padding: 12px; }}
    .btn-ghost {{ background: #e2e8f0; color: #334155; }}
    .btn:disabled {{ opacity: .45; cursor: not-allowed; }}

    /* ── Status bar ── */
    .statusbar {{
      background: #dfe6e9;
      border-top: 1px solid #b2bec3;
      padding: 5px 16px;
      font-size: 12px;
      color: #2d3436;
      flex-shrink: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .statusbar.ok {{ color: #065f46; }}
    .statusbar.err {{ color: var(--danger); }}

    /* ── Toast ── */
    .toast {{
      position: fixed;
      bottom: 36px;
      left: 50%;
      transform: translateX(-50%);
      background: #1e293b;
      color: #f1f5f9;
      padding: 12px 24px;
      border-radius: 12px;
      font-size: 14px;
      opacity: 0;
      transition: opacity .25s;
      pointer-events: none;
      z-index: 99;
      white-space: pre-line;
      text-align: center;
    }}
    .toast.show {{ opacity: 1; }}
    .toast.ok {{ background: #065f46; }}
    .toast.err {{ background: #9f1239; }}
  </style>
</head>
<body>

<div class="topbar">
  <div>
    <h1>Annotation Tool</h1>
    <div class="sub">Tambah data ke dataset traffic sign</div>
  </div>
</div>

<div class="workspace">

  <!-- Canvas -->
  <div class="canvas-area">
    <div class="canvas-toolbar">
      <label>
        Pilih Gambar
        <input type="file" id="fileInput" accept="image/*" />
      </label>
      <span class="file-name" id="fileName">(belum ada gambar)</span>
    </div>
    <div class="canvas-wrap">
      <canvas id="mainCanvas"></canvas>
      <div class="hint" id="hint">Pilih gambar untuk mulai anotasi</div>
    </div>
  </div>

  <!-- Panel -->
  <div class="panel">

    <div class="panel-section">
      <h3>Kelas</h3>
      <select id="classSelect"></select>
    </div>

    <div class="panel-section">
      <h3>Split</h3>
      <div class="radio-row">
        <label><input type="radio" name="split" value="train" checked /> Train</label>
        <label><input type="radio" name="split" value="test" /> Test</label>
      </div>
      <div class="dest-preview" id="destPreview"></div>
    </div>

    <div class="panel-section" style="flex-shrink:0">
      <h3>Anotasi (<span id="annCount">0</span>)</h3>
    </div>

    <div class="ann-list-wrap" id="annList">
      <div class="ann-empty">Belum ada bbox. Klik-drag di gambar.</div>
    </div>

    <div class="panel-footer">
      <button class="btn btn-ghost" id="clearBtn" disabled>Hapus Semua</button>
      <button class="btn btn-primary" id="saveBtn" disabled>Simpan ke Dataset</button>
    </div>

  </div>
</div>

<div class="statusbar" id="statusBar">Siap.</div>
<div class="toast" id="toast"></div>

<script>
const CLASS_NAMES = {classes_js};
const COLORS = [
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#9b59b6","#1abc9c","#e67e22","#8e44ad",
];

// ── State ──────────────────────────────────────────────────────────────────
let origImage = null;   // HTMLImageElement (ukuran asli)
let imgFile   = null;   // File object
let imgW = 0, imgH = 0; // ukuran gambar asli
let scale = 1, offX = 0, offY = 0; // mapping canvas ↔ gambar

let annotations = []; // {{ class_label, x1,y1,x2,y2 }} — koordinat gambar asli
let selectedIdx = -1;

let dragging  = false;
let dragStart = null; // {{cx, cy}} canvas coords

// ── DOM refs ───────────────────────────────────────────────────────────────
const canvas      = document.getElementById("mainCanvas");
const ctx         = canvas.getContext("2d");
const fileInput   = document.getElementById("fileInput");
const fileName    = document.getElementById("fileName");
const hint        = document.getElementById("hint");
const classSelect = document.getElementById("classSelect");
const annList     = document.getElementById("annList");
const annCount    = document.getElementById("annCount");
const destPreview = document.getElementById("destPreview");
const clearBtn    = document.getElementById("clearBtn");
const saveBtn     = document.getElementById("saveBtn");
const statusBar   = document.getElementById("statusBar");
const toast       = document.getElementById("toast");

// ── Init class dropdown ────────────────────────────────────────────────────
CLASS_NAMES.forEach(name => {{
  const opt = document.createElement("option");
  opt.value = opt.textContent = name;
  classSelect.appendChild(opt);
}});
classSelect.addEventListener("change", () => {{ updateDest(); render(); }});
document.querySelectorAll("input[name=split]").forEach(r =>
  r.addEventListener("change", updateDest)
);
updateDest();

// ── File input ─────────────────────────────────────────────────────────────
fileInput.addEventListener("change", e => {{
  const file = e.target.files?.[0];
  if (!file) return;
  imgFile = file;
  fileName.textContent = file.name;
  const url = URL.createObjectURL(file);
  const img = new Image();
  img.onload = () => {{
    origImage = img;
    imgW = img.naturalWidth;
    imgH = img.naturalHeight;
    annotations = [];
    selectedIdx = -1;
    resizeCanvas();
    hint.style.display = "none";
    setStatus(`Gambar dimuat: ${{file.name}}  (${{imgW}}×${{imgH}} px)`);
    refreshList();
  }};
  img.src = url;
}});

// ── Canvas resize ──────────────────────────────────────────────────────────
function resizeCanvas() {{
  if (!origImage) return;
  const wrap = canvas.parentElement;
  const maxW = wrap.clientWidth  - 2;
  const maxH = wrap.clientHeight - 2;
  scale = Math.min(maxW / imgW, maxH / imgH, 1);
  const dispW = Math.floor(imgW * scale);
  const dispH = Math.floor(imgH * scale);
  canvas.width  = dispW;
  canvas.height = dispH;
  offX = 0; offY = 0;
  render();
}}
window.addEventListener("resize", () => {{ if (origImage) resizeCanvas(); }});

// ── Render ─────────────────────────────────────────────────────────────────
function render() {{
  if (!origImage) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(origImage, 0, 0, canvas.width, canvas.height);
  annotations.forEach((ann, i) => drawBox(ann, i, i === selectedIdx));
}}

function drawBox(ann, i, isSelected) {{
  const color = COLORS[i % COLORS.length];
  const cx1 = ann.x1 * scale;
  const cy1 = ann.y1 * scale;
  const cx2 = ann.x2 * scale;
  const cy2 = ann.y2 * scale;

  ctx.strokeStyle = color;
  ctx.lineWidth   = isSelected ? 3 : 2;
  ctx.strokeRect(cx1, cy1, cx2 - cx1, cy2 - cy1);

  // Label pill
  const short = ann.class_label.split("-").slice(-1)[0];
  ctx.font = "bold 12px Segoe UI";
  const tw = ctx.measureText(short).width;
  const py = Math.max(cy1, 18);
  ctx.fillStyle = color;
  ctx.fillRect(cx1, py - 18, tw + 10, 18);
  ctx.fillStyle = "#fff";
  ctx.fillText(short, cx1 + 5, py - 5);
}}

// ── Mouse events ───────────────────────────────────────────────────────────
canvas.addEventListener("mousedown", e => {{
  if (!origImage) return;
  dragging  = true;
  dragStart = {{ cx: e.offsetX, cy: e.offsetY }};
}});

canvas.addEventListener("mousemove", e => {{
  if (!dragging || !dragStart) return;
  render();
  ctx.strokeStyle = "#f1c40f";
  ctx.lineWidth   = 2;
  ctx.setLineDash([5, 3]);
  ctx.strokeRect(
    dragStart.cx, dragStart.cy,
    e.offsetX - dragStart.cx, e.offsetY - dragStart.cy
  );
  ctx.setLineDash([]);

  // koordinat di status bar
  const ix1 = Math.round(Math.min(dragStart.cx, e.offsetX) / scale);
  const iy1 = Math.round(Math.min(dragStart.cy, e.offsetY) / scale);
  const ix2 = Math.round(Math.max(dragStart.cx, e.offsetX) / scale);
  const iy2 = Math.round(Math.max(dragStart.cy, e.offsetY) / scale);
  setStatus(`Menggambar bbox  [${{ix1}},${{iy1}} → ${{ix2}},${{iy2}}]  (${{ix2-ix1}}×${{iy2-iy1}} px)  |  Esc = batal`);
}});

canvas.addEventListener("mouseup", e => {{
  if (!dragging || !dragStart) return;
  dragging = false;
  ctx.setLineDash([]);

  const sx = dragStart.cx, sy = dragStart.cy;
  const ex = e.offsetX,    ey = e.offsetY;
  dragStart = null;

  if (Math.abs(ex - sx) < 8 || Math.abs(ey - sy) < 8) {{
    setStatus("Bbox terlalu kecil, diabaikan. Klik-drag lebih jauh.");
    render();
    return;
  }}

  const x1 = Math.max(0, Math.round(Math.min(sx, ex) / scale));
  const y1 = Math.max(0, Math.round(Math.min(sy, ey) / scale));
  const x2 = Math.min(imgW, Math.round(Math.max(sx, ex) / scale));
  const y2 = Math.min(imgH, Math.round(Math.max(sy, ey) / scale));

  annotations.push({{ class_label: classSelect.value, x1, y1, x2, y2 }});
  selectedIdx = annotations.length - 1;
  refreshList();
  render();
  setStatus(`Bbox ${{annotations.length}} ditambahkan  [${{x1}},${{y1}} → ${{x2}},${{y2}}]  (${{x2-x1}}×${{y2-y1}} px)`);
}});

document.addEventListener("keydown", e => {{
  if (e.key === "Escape") {{ dragging = false; dragStart = null; ctx.setLineDash([]); render(); }}
  if ((e.key === "Delete" || e.key === "Backspace") && selectedIdx >= 0) deleteAnn(selectedIdx);
}});

// ── Annotation list ────────────────────────────────────────────────────────
function refreshList() {{
  annCount.textContent = annotations.length;
  clearBtn.disabled = saveBtn.disabled = annotations.length === 0 || !imgFile;

  if (annotations.length === 0) {{
    annList.innerHTML = '<div class="ann-empty">Belum ada bbox. Klik-drag di gambar.</div>';
    return;
  }}

  annList.innerHTML = "";
  annotations.forEach((ann, i) => {{
    const color = COLORS[i % COLORS.length];
    const item = document.createElement("div");
    item.className = "ann-item" + (i === selectedIdx ? " selected" : "");
    item.innerHTML = `
      <div class="ann-dot" style="background:${{color}}"></div>
      <div class="ann-text">
        <span class="ann-label">${{ann.class_label}}</span>
        <span class="ann-coords">[${{ann.x1}},${{ann.y1}} → ${{ann.x2}},${{ann.y2}}]</span>
      </div>
      <button class="ann-del" title="Hapus" data-i="${{i}}">×</button>
    `;
    item.addEventListener("click", ev => {{
      if (ev.target.classList.contains("ann-del")) return;
      selectedIdx = i;
      refreshList();
      render();
    }});
    item.querySelector(".ann-del").addEventListener("click", () => deleteAnn(i));
    annList.appendChild(item);
  }});
}}

function deleteAnn(i) {{
  annotations.splice(i, 1);
  selectedIdx = Math.min(selectedIdx, annotations.length - 1);
  refreshList();
  render();
  setStatus(`Anotasi ${{i + 1}} dihapus.`);
}}

clearBtn.addEventListener("click", () => {{
  if (!confirm("Hapus semua anotasi?")) return;
  annotations = []; selectedIdx = -1;
  refreshList(); render();
  setStatus("Semua anotasi dihapus.");
}});

// ── Dest preview ───────────────────────────────────────────────────────────
function updateDest() {{
  const cls   = classSelect.value;
  const split = document.querySelector("input[name=split]:checked").value;
  destPreview.textContent = `Tujuan: data/traffic_sign/${{split}}/${{cls}}/`;
}}

// ── Save ───────────────────────────────────────────────────────────────────
saveBtn.addEventListener("click", async () => {{
  if (!imgFile || annotations.length === 0) return;

  const split       = document.querySelector("input[name=split]:checked").value;
  const class_label = classSelect.value;

  const fd = new FormData();
  fd.append("file",         imgFile);
  fd.append("annotations",  JSON.stringify(annotations));
  fd.append("class_label",  class_label);
  fd.append("split",        split);
  fd.append("img_width",    String(imgW));
  fd.append("img_height",   String(imgH));

  saveBtn.disabled = true;
  setStatus("Menyimpan ...");

  try {{
    const res = await fetch("/data/save-annotation", {{ method: "POST", body: fd }});
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Gagal menyimpan");
    showToast(`Tersimpan!\\n${{data.saved_as}}\\n${{data.bbox_count}} bbox`, "ok");
    setStatus(`Tersimpan → ${{data.saved_as}}  |  ${{data.bbox_count}} bbox  |  split=${{split}}`, "ok");
  }} catch (err) {{
    showToast(err.message, "err");
    setStatus(err.message, "err");
  }} finally {{
    saveBtn.disabled = false;
  }}
}});

// ── Helpers ────────────────────────────────────────────────────────────────
function setStatus(msg, kind = "") {{
  statusBar.textContent = msg;
  statusBar.className = "statusbar" + (kind ? " " + kind : "");
}}

let toastTimer = null;
function showToast(msg, kind = "") {{
  toast.textContent  = msg;
  toast.className    = "toast show" + (kind ? " " + kind : "");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 3500);
}}
</script>
</body>
</html>
"""
