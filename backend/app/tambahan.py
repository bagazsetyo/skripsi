"""
Halaman web impor gambar dari traffic_sign_tambahan ke dataset utama.
"""
from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

REPO_ROOT    = Path(__file__).resolve().parents[2]
TAMBAHAN_DIR = REPO_ROOT / "data" / "traffic_sign_tambahan"

_IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def _find_label_for(img_path: Path) -> Path | None:
    if img_path.parent.name == "images":
        return img_path.parent.parent / "labels" / (img_path.stem + ".txt")
    candidate = img_path.with_suffix(".txt")
    return candidate if candidate.exists() else None


def _parse_bboxes(txt_path: Path | None) -> list[list[float]]:
    if txt_path is None or not txt_path.exists():
        return []
    bboxes: list[list[float]] = []
    for line in txt_path.read_text(encoding="utf-8").strip().splitlines():
        parts = line.strip().split()
        if len(parts) >= 5:
            try:
                bboxes.append([float(p) for p in parts[1:5]])  # cx cy w h
            except ValueError:
                pass
    return bboxes


def list_image_sources() -> list[dict]:
    """Daftar semua folder images/ yang tersedia di tambahan."""
    if not TAMBAHAN_DIR.exists():
        return []
    sources = []
    for images_dir in sorted(TAMBAHAN_DIR.rglob("images")):
        if not images_dir.is_dir():
            continue
        count = sum(1 for f in images_dir.iterdir() if f.suffix.lower() in _IMG_EXTS)
        if count == 0:
            continue
        rel = images_dir.relative_to(TAMBAHAN_DIR)
        sources.append({
            "key": rel.as_posix(),
            "label": rel.parent.as_posix(),
            "count": count,
        })
    return sources


def get_images_page(source_key: str, page: int, per_page: int) -> dict:
    """Ambil halaman gambar dari folder source_key (relatif terhadap TAMBAHAN_DIR)."""
    images_dir = TAMBAHAN_DIR / Path(source_key)
    if not images_dir.exists():
        return {"images": [], "total": 0, "page": 1, "per_page": per_page, "total_pages": 1}

    all_images = sorted(f for f in images_dir.iterdir() if f.suffix.lower() in _IMG_EXTS)
    total       = len(all_images)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page        = max(1, min(page, total_pages))
    chunk       = all_images[(page - 1) * per_page : page * per_page]

    images = []
    for img_path in chunk:
        bboxes = _parse_bboxes(_find_label_for(img_path))
        images.append({
            "path":   img_path.relative_to(TAMBAHAN_DIR).as_posix(),
            "name":   img_path.name,
            "bboxes": bboxes,
        })

    return {
        "images":      images,
        "total":       total,
        "page":        page,
        "per_page":    per_page,
        "total_pages": total_pages,
    }


def move_images(
    paths: list[str],
    class_label: str,
    split: str,
    class_label_to_id: dict[str, int],
    data_dir: Path,
) -> dict:
    """Pindahkan gambar + hapus label sumber, tulis label baru ke dataset."""
    dest_dir = data_dir / split / class_label
    dest_dir.mkdir(parents=True, exist_ok=True)
    class_id = class_label_to_id[class_label]

    moved:  int       = 0
    errors: list[str] = []

    for rel_str in paths:
        img_path = TAMBAHAN_DIR / Path(rel_str)
        if not img_path.exists():
            errors.append(f"Tidak ditemukan: {rel_str}")
            continue

        bboxes = _parse_bboxes(_find_label_for(img_path))
        if not bboxes:
            errors.append(f"Tidak ada bbox: {rel_str}")
            continue

        # Tentukan nama tujuan (hindari tabrakan)
        suffix = img_path.suffix.lower()
        if suffix not in {".jpg", ".jpeg", ".png", ".bmp"}:
            suffix = ".jpg"
        ts = int(time.time() * 1000) % 1_000_000
        dest_img = dest_dir / f"{img_path.stem}_{ts}{suffix}"
        while dest_img.exists():
            ts += 1
            dest_img = dest_dir / f"{img_path.stem}_{ts}{suffix}"

        # Pindahkan gambar
        try:
            shutil.move(str(img_path), str(dest_img))
        except Exception as exc:
            errors.append(f"Gagal pindah {rel_str}: {exc}")
            continue

        # Hapus label sumber
        src_label = _find_label_for(img_path)
        if src_label and src_label.exists():
            try:
                src_label.unlink()
            except Exception:
                pass

        # Tulis label baru (class_id baru sesuai kelas yang dipilih)
        lines = [f"{class_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}" for cx, cy, bw, bh in bboxes]
        dest_img.with_suffix(".txt").write_text("\n".join(lines), encoding="utf-8")
        moved += 1

    return {"moved": moved, "errors": errors, "ok": len(errors) == 0}


# ---------------------------------------------------------------------------
# HTML builder
# ---------------------------------------------------------------------------

def build_tambahan_html(class_names: list[str]) -> str:
    class_options = "\n".join(
        f'        <option value="{c}">{c}</option>' for c in class_names
    )
    class_names_json = json.dumps(class_names)
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Impor Gambar Tambahan</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#1a1a2e;color:#ecf0f1;font-family:'Segoe UI',sans-serif;display:flex;flex-direction:column;height:100vh;overflow:hidden}}

    header{{background:#2c3e50;padding:10px 16px;display:flex;align-items:center;gap:14px;border-bottom:2px solid #8e44ad;flex-shrink:0}}
    header h1{{font-size:15px;color:#a29bfe;white-space:nowrap}}
    .toolbar{{display:flex;align-items:center;gap:12px;flex:1;flex-wrap:wrap}}
    .toolbar label{{font-size:12px;color:#7f8c8d;margin-right:3px}}
    select,input[type=number]{{background:#34495e;color:#ecf0f1;border:1px solid #4a6278;border-radius:4px;padding:4px 8px;font-size:13px}}

    .layout{{display:flex;flex:1;overflow:hidden}}

    .main{{flex:1;display:flex;flex-direction:column;overflow:hidden}}
    .grid-wrap{{flex:1;overflow-y:auto;padding:12px}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}}

    .card{{position:relative;border-radius:8px;overflow:hidden;cursor:pointer;border:2px solid #2c3e50;transition:border-color .15s,transform .1s;background:#0f172a}}
    .card:hover{{border-color:#6c5ce7;transform:scale(1.02)}}
    .card.selected{{border-color:#8e44ad;box-shadow:0 0 14px rgba(142,68,173,.55)}}
    .card canvas{{width:100%;display:block}}
    .card-label{{position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,.65);font-size:10px;color:#bdc3c7;padding:3px 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
    .chk{{position:absolute;top:6px;right:6px;width:22px;height:22px;border-radius:50%;background:rgba(0,0,0,.55);border:2px solid #7f8c8d;display:flex;align-items:center;justify-content:center;font-size:12px;color:transparent;transition:background .15s,border-color .15s}}
    .card.selected .chk{{background:#8e44ad;border-color:#8e44ad;color:#fff}}

    .pagination{{display:flex;align-items:center;justify-content:center;gap:6px;padding:9px;border-top:1px solid #2c3e50;flex-shrink:0;background:#16213e;flex-wrap:wrap}}
    .btn{{background:#34495e;color:#ecf0f1;border:1px solid #4a6278;border-radius:4px;padding:5px 11px;cursor:pointer;font-size:13px}}
    .btn:hover:not(:disabled){{background:#4a6278}}
    .btn:disabled{{opacity:.4;cursor:default}}
    .btn.active{{background:#8e44ad;border-color:#8e44ad}}
    .pg-info{{color:#7f8c8d;font-size:12px}}

    .panel{{width:240px;background:#16213e;border-left:1px solid #2c3e50;padding:14px;display:flex;flex-direction:column;gap:12px;overflow-y:auto;flex-shrink:0}}
    .panel h3{{font-size:11px;color:#a29bfe;text-transform:uppercase;letter-spacing:.5px}}
    .panel .row-label{{font-size:12px;color:#7f8c8d;display:block;margin-bottom:4px}}
    .panel select{{width:100%}}
    .split-opts{{display:flex;gap:14px}}
    .split-opts label{{display:flex;align-items:center;gap:5px;color:#ecf0f1;cursor:pointer;font-size:13px}}
    .count-box{{background:#2c3e50;border-radius:8px;padding:10px;text-align:center}}
    .count-box .num{{font-size:30px;font-weight:700;color:#8e44ad;display:block;line-height:1}}
    .count-box .lbl{{font-size:11px;color:#7f8c8d;margin-top:2px}}
    .act-btn{{background:#8e44ad;color:#fff;border:none;border-radius:6px;padding:10px 14px;font-size:14px;font-weight:700;cursor:pointer;width:100%;transition:background .15s}}
    .act-btn:hover:not(:disabled){{background:#9b59b6}}
    .act-btn:disabled{{opacity:.4;cursor:default}}
    .act-btn.sec{{background:#2c3e50;border:1px solid #4a6278;font-weight:400;font-size:12px;padding:7px}}
    .act-btn.sec:hover:not(:disabled){{background:#34495e}}

    .empty{{text-align:center;padding:48px;color:#7f8c8d;font-size:14px}}

    .toast{{position:fixed;bottom:20px;right:20px;background:#27ae60;color:#fff;padding:10px 18px;border-radius:8px;font-size:13px;display:none;z-index:999;max-width:320px}}
    .toast.err{{background:#c0392b}}
  </style>
</head>
<body>

<header>
  <h1>Impor dari Tambahan</h1>
  <div class="toolbar">
    <div>
      <label>Folder:</label>
      <select id="srcSel" onchange="onSourceChange()"></select>
    </div>
    <div>
      <label>Per hal:</label>
      <select id="ppSel" onchange="onPerPageChange()">
        <option value="12">12</option>
        <option value="20">20</option>
        <option value="50" selected>50</option>
        <option value="30">30</option>
        <option value="48">48</option>
      </select>
    </div>
    <span id="totalInfo" style="color:#7f8c8d;font-size:12px"></span>
  </div>
</header>

<div class="layout">
  <div class="main">
    <div class="grid-wrap">
      <div class="grid" id="grid"><div class="empty">Memuat...</div></div>
    </div>
    <div class="pagination" id="pagination"></div>
  </div>

  <div class="panel">
    <div>
      <h3>Kelas Tujuan</h3>
      <span class="row-label">Pilih kelas:</span>
      <select id="clsSel">
{class_options}
      </select>
    </div>

    <div>
      <h3>Split Tujuan</h3>
      <div class="split-opts">
        <label><input type="radio" name="split" value="train" checked> Train</label>
        <label><input type="radio" name="split" value="test"> Test</label>
      </div>
    </div>

    <div class="count-box">
      <span class="num" id="selNum">0</span>
      <span class="lbl">gambar dipilih</span>
    </div>

    <button class="act-btn sec" onclick="selectPage()">Pilih Semua di Halaman</button>
    <button class="act-btn sec" onclick="clearPage()">Batal Pilih di Halaman</button>
    <button class="act-btn sec" onclick="clearAll()">Batal Semua Pilihan</button>

    <button class="act-btn" id="moveBtn" onclick="moveSelected()" disabled>
      Pindahkan ke Dataset ▶
    </button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const CLASSES = {class_names_json};
let selected = new Set();
let curPage  = 1;
let curSrc   = '';
let totPages = 1;
let perPage  = 50;
let pageImgs = [];

// ── Init ──────────────────────────────────────────────────────────────────
async function init() {{
  try {{
    const res = await fetch('/tambahan/api/sources');
    const srcs = await res.json();
    const sel = document.getElementById('srcSel');
    srcs.forEach(s => {{
      const o = document.createElement('option');
      o.value = s.key;
      o.textContent = s.label + '  (' + s.count + ')';
      sel.appendChild(o);
    }});
    if (srcs.length > 0) {{ curSrc = srcs[0].key; loadPage(1); }}
    else {{ document.getElementById('grid').innerHTML = '<div class="empty">Folder tambahan kosong atau tidak ditemukan.</div>'; }}
  }} catch(e) {{ showToast('Gagal memuat sumber: ' + e.message, true); }}
}}

// ── Load page ─────────────────────────────────────────────────────────────
async function loadPage(page) {{
  document.getElementById('grid').innerHTML = '<div class="empty">Memuat...</div>';
  const p = new URLSearchParams({{ source: curSrc, page, per_page: perPage }});
  const res = await fetch('/tambahan/api/images?' + p);
  const data = await res.json();

  curPage  = data.page;
  totPages = data.total_pages;
  pageImgs = data.images;

  document.getElementById('totalInfo').textContent = 'Total: ' + data.total + ' gambar';
  renderGrid(data.images);
  renderPagination();
}}

// ── Grid ──────────────────────────────────────────────────────────────────
function renderGrid(imgs) {{
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  if (!imgs.length) {{ grid.innerHTML = '<div class="empty">Tidak ada gambar.</div>'; return; }}
  imgs.forEach(img => grid.appendChild(makeCard(img)));
}}

function makeCard(imgData) {{
  const card = document.createElement('div');
  card.className = 'card' + (selected.has(imgData.path) ? ' selected' : '');
  card.dataset.path = imgData.path;

  const canvas = document.createElement('canvas');
  card.appendChild(canvas);

  const image = new Image();
  image.onload = () => {{
    canvas.width  = image.naturalWidth;
    canvas.height = image.naturalHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(image, 0, 0);
    const colors = ['#e74c3c','#2ecc71','#3498db','#f39c12','#9b59b6'];
    imgData.bboxes.forEach(([cx,cy,bw,bh], i) => {{
      const x = (cx - bw/2) * canvas.width;
      const y = (cy - bh/2) * canvas.height;
      const w = bw * canvas.width;
      const h = bh * canvas.height;
      ctx.strokeStyle = colors[i % colors.length];
      ctx.lineWidth = Math.max(2, canvas.width / 180);
      ctx.strokeRect(x, y, w, h);
    }});
  }};
  image.onerror = () => {{ canvas.width=170; canvas.height=120; const ctx=canvas.getContext('2d'); ctx.fillStyle='#2c3e50'; ctx.fillRect(0,0,170,120); ctx.fillStyle='#7f8c8d'; ctx.textAlign='center'; ctx.fillText('?',85,65); }};
  image.src = '/tambahan/img/' + imgData.path;

  const lbl = document.createElement('div');
  lbl.className = 'card-label';
  lbl.title = imgData.name;
  lbl.textContent = imgData.name;
  card.appendChild(lbl);

  const chk = document.createElement('div');
  chk.className = 'chk';
  chk.textContent = '✓';
  card.appendChild(chk);

  card.addEventListener('click', () => toggleCard(card, imgData.path));
  return card;
}}

function toggleCard(card, path) {{
  if (selected.has(path)) {{ selected.delete(path); card.classList.remove('selected'); }}
  else {{ selected.add(path); card.classList.add('selected'); }}
  updateUI();
}}

// ── Selection ─────────────────────────────────────────────────────────────
function selectPage() {{
  pageImgs.forEach(i => selected.add(i.path));
  document.querySelectorAll('.card').forEach(c => c.classList.add('selected'));
  updateUI();
}}
function clearPage() {{
  pageImgs.forEach(i => selected.delete(i.path));
  document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
  updateUI();
}}
function clearAll() {{
  selected.clear();
  document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
  updateUI();
}}
function updateUI() {{
  document.getElementById('selNum').textContent = selected.size;
  document.getElementById('moveBtn').disabled = selected.size === 0;
}}

// ── Move ──────────────────────────────────────────────────────────────────
async function moveSelected() {{
  if (!selected.size) return;
  const cls   = document.getElementById('clsSel').value;
  const split = document.querySelector('input[name="split"]:checked').value;
  if (!confirm(`Pindahkan ${{selected.size}} gambar ke:\\n${{split}} / ${{cls}} ?`)) return;

  const btn = document.getElementById('moveBtn');
  btn.disabled = true;
  btn.textContent = 'Memproses...';

  try {{
    const res = await fetch('/tambahan/move', {{
      method: 'POST',
      headers: {{'Content-Type':'application/json'}},
      body: JSON.stringify({{ paths:[...selected], class_label:cls, split }})
    }});
    const data = await res.json();
    if (res.ok) {{
      showToast(data.moved + ' gambar berhasil dipindahkan' + (data.errors.length ? ' (' + data.errors.length + ' gagal)' : ''), false);
      selected.clear();
      updateUI();
      loadPage(curPage);
    }} else {{
      showToast('Gagal: ' + (data.detail || JSON.stringify(data)), true);
    }}
  }} catch(e) {{ showToast('Error: ' + e.message, true); }}

  btn.textContent = 'Pindahkan ke Dataset ▶';
}}

// ── Pagination ────────────────────────────────────────────────────────────
function renderPagination() {{
  const el = document.getElementById('pagination');
  el.innerHTML = '';

  const prev = mkBtn('◀ Prev', curPage <= 1, () => loadPage(curPage-1));
  el.appendChild(prev);

  pRange(curPage, totPages, 7).forEach(p => {{
    if (p === '...') {{ const s=document.createElement('span'); s.textContent='…'; s.style.color='#7f8c8d'; el.appendChild(s); }}
    else {{
      const b = mkBtn(p, false, () => loadPage(p));
      if (p === curPage) b.classList.add('active');
      el.appendChild(b);
    }}
  }});

  el.appendChild(mkBtn('Next ▶', curPage >= totPages, () => loadPage(curPage+1)));

  const info = document.createElement('span');
  info.className = 'pg-info';
  info.textContent = 'Hal. ' + curPage + ' / ' + totPages;
  el.appendChild(info);
}}

function mkBtn(text, disabled, onClick) {{
  const b = document.createElement('button');
  b.className = 'btn';
  b.textContent = text;
  b.disabled = disabled;
  if (!disabled) b.onclick = onClick;
  return b;
}}

function pRange(cur, tot, max) {{
  if (tot <= max) return Array.from({{length:tot}}, (_,i) => i+1);
  const half=Math.floor(max/2);
  let s=Math.max(1,cur-half), e=Math.min(tot,s+max-1);
  if (e-s < max-1) s=Math.max(1,e-max+1);
  const r=[];
  if (s>1){{r.push(1);if(s>2)r.push('...');}}
  for(let p=s;p<=e;p++) r.push(p);
  if(e<tot){{if(e<tot-1)r.push('...');r.push(tot);}}
  return r;
}}

// ── Source/perPage change ──────────────────────────────────────────────────
function onSourceChange() {{
  curSrc = document.getElementById('srcSel').value;
  selected.clear(); updateUI(); loadPage(1);
}}
function onPerPageChange() {{
  perPage = parseInt(document.getElementById('ppSel').value);
  selected.clear(); updateUI(); loadPage(1);
}}

// ── Toast ─────────────────────────────────────────────────────────────────
function showToast(msg, isErr) {{
  const t=document.getElementById('toast');
  t.textContent=msg; t.className='toast'+(isErr?' err':'');
  t.style.display='block';
  setTimeout(()=>{{t.style.display='none';}},3500);
}}

init();
</script>
</body>
</html>"""
