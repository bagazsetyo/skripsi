from __future__ import annotations


def build_video_demo_html() -> str:
    return """<!DOCTYPE html>
<html lang="id">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Deteksi dan Klasifikasi Real-Time</title>
    <style>
      :root {
        color-scheme: light;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      }

      * { box-sizing: border-box; margin: 0; padding: 0; }

      body {
        background: #f4f6fb;
        color: #1f2937;
      }

      .page {
        max-width: 1200px;
        margin: 0 auto;
        padding: 16px;
      }

      .layout {
        display: grid;
        grid-template-columns: 280px 1fr;
        gap: 16px;
        align-items: start;
      }

      .card {
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
        padding: 16px;
      }

      .sidebar { display: grid; gap: 14px; }

      .field { display: grid; gap: 5px; }

      .field label {
        font-weight: 600;
        font-size: 13px;
        color: #475569;
      }

      .field select,
      .field input[type="number"] {
        font: inherit;
        width: 100%;
        padding: 8px 10px;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        background: #fff;
        font-size: 14px;
      }

      .btn-group { display: grid; gap: 8px; }

      button {
        border: 0;
        border-radius: 10px;
        padding: 10px 14px;
        cursor: pointer;
        font: inherit;
        font-weight: 600;
        font-size: 13px;
        transition: opacity .15s;
      }

      button:hover:not(:disabled) { opacity: 0.85; }
      button:disabled { cursor: not-allowed; opacity: 0.45; }

      .btn-primary { background: #0f766e; color: #fff; }
      .btn-danger  { background: #dc2626; color: #fff; }
      .btn-ghost   { background: #e2e8f0; color: #1e293b; }

      .status-box {
        font-size: 13px;
        line-height: 1.5;
        padding: 10px 12px;
        border-radius: 10px;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534;
      }

      .status-box.error {
        background: #fef2f2;
        border-color: #fecaca;
        color: #991b1b;
      }

      .status-box.idle {
        background: #f8fafc;
        border-color: #e2e8f0;
        color: #64748b;
      }

      .video-area {
        position: relative;
        overflow: hidden;
        border-radius: 14px;
        background: #0f172a;
        min-height: 320px;
      }

      video {
        display: block;
        width: 100%;
        height: auto;
      }

      canvas.overlay {
        position: absolute;
        inset: 0;
        pointer-events: none;
        display: block;
        width: 100%;
        height: auto;
      }

      .stats-row {
        margin-top: 12px;
        display: grid;
        gap: 10px;
        grid-template-columns: repeat(3, 1fr);
      }

      .stat-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
      }

      .stat-card .lbl {
        display: block;
        color: #64748b;
        font-size: 12px;
        margin-bottom: 4px;
      }

      .stat-card .val {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
      }

      .stat-card .val.running { color: #16a34a; }

      .results {
        margin-top: 14px;
      }

      .results h3 {
        font-size: 15px;
        margin-bottom: 10px;
        color: #334155;
      }

      .results-list {
        list-style: none;
        display: grid;
        gap: 6px;
      }

      .results-list li {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px 12px;
        background: #fff;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 10px;
      }

      .results-list .class-badge {
        background: #0f766e;
        color: #fff;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
        white-space: nowrap;
      }

      .results-list .conf {
        color: #0f766e;
        font-weight: 700;
        font-size: 14px;
        min-width: 52px;
      }

      .results-list .muted { color: #94a3b8; font-size: 12px; }

      .empty-msg {
        color: #94a3b8;
        font-size: 13px;
        padding: 8px 0;
      }

      @media (max-width: 780px) {
        .layout { grid-template-columns: 1fr; }
        .stats-row { grid-template-columns: 1fr; }
      }
    </style>
  </head>
  <body>
    <div class="page">
      <section class="layout">
        <aside class="card sidebar">
          <div class="field">
            <label for="intervalSelect">Interval Klasifikasi</label>
            <select id="intervalSelect">
              <option value="500">0.5 detik</option>
              <option value="1000" selected>1 detik</option>
              <option value="1500">1.5 detik</option>
              <option value="2000">2 detik</option>
            </select>
          </div>

          <div class="field">
            <label for="scoreThreshold">Score Threshold</label>
            <input id="scoreThreshold" type="number" min="0" max="1" step="0.05" value="0.5" />
          </div>

          <div class="btn-group">
            <button id="startCameraButton" class="btn-primary">Buka Kamera</button>
            <button id="startDetectionButton" class="btn-primary" style="background:#1d4ed8">
              Mulai Deteksi
            </button>
            <button id="stopDetectionButton" class="btn-danger">Hentikan Deteksi</button>
          </div>

          <div id="statusBox" class="status-box idle">
            Tekan Buka Kamera untuk memulai.
          </div>
        </aside>

        <main class="card" style="padding: 12px;">
          <div class="video-area">
            <video id="videoElement" playsinline autoplay muted></video>
            <canvas id="overlayCanvas" class="overlay"></canvas>
          </div>

          <div class="stats-row">
            <div class="stat-card">
              <span class="lbl">Model Aktif</span>
              <span class="val" id="activeModelText">Memuat...</span>
            </div>
            <div class="stat-card">
              <span class="lbl">Status</span>
              <span class="val" id="detectionStateText">Idle</span>
            </div>
            <div class="stat-card">
              <span class="lbl">Objek Terdeteksi</span>
              <span class="val" id="detectionCountText">0</span>
            </div>
          </div>

          <section class="results">
            <h3>Hasil Deteksi</h3>
            <ul class="results-list" id="detectionList">
              <li><span class="empty-msg">Belum ada hasil. Buka kamera lalu tekan Mulai Deteksi.</span></li>
            </ul>
          </section>
        </main>
      </section>
    </div>

    <script>
      const videoElement = document.getElementById("videoElement");
      const overlayCanvas = document.getElementById("overlayCanvas");
      const overlayCtx = overlayCanvas.getContext("2d");
      const captureCanvas = document.createElement("canvas");
      const captureCtx = captureCanvas.getContext("2d");

      const intervalSelect = document.getElementById("intervalSelect");
      const scoreThresholdInput = document.getElementById("scoreThreshold");
      const startCameraButton = document.getElementById("startCameraButton");
      const startDetectionButton = document.getElementById("startDetectionButton");
      const stopDetectionButton = document.getElementById("stopDetectionButton");
      const statusBox = document.getElementById("statusBox");
      const activeModelText = document.getElementById("activeModelText");
      const detectionStateText = document.getElementById("detectionStateText");
      const detectionCountText = document.getElementById("detectionCountText");
      const detectionList = document.getElementById("detectionList");

      let mediaStream = null;
      let detectionTimer = null;
      let detecting = false;
      let inflight = false;

      function setStatus(msg, kind) {
        statusBox.textContent = msg;
        statusBox.className = "status-box" + (kind === "error" ? " error" : kind === "idle" ? " idle" : "");
      }

      function resizeOverlay() {
        const w = videoElement.clientWidth || videoElement.videoWidth || 640;
        const h = videoElement.clientHeight || videoElement.videoHeight || 480;
        overlayCanvas.width = w;
        overlayCanvas.height = h;
        overlayCanvas.style.width = w + "px";
        overlayCanvas.style.height = h + "px";
        overlayCtx.clearRect(0, 0, w, h);
      }

      function stopStream() {
        if (!mediaStream) return;
        mediaStream.getTracks().forEach(t => t.stop());
        mediaStream = null;
      }

      function stopDetection() {
        detecting = false;
        inflight = false;
        detectionStateText.textContent = "Idle";
        detectionStateText.classList.remove("running");
        clearTimeout(detectionTimer);
      }

      function resetUI() {
        overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
        detectionCountText.textContent = "0";
        detectionList.innerHTML = '<li><span class="empty-msg">Belum ada hasil deteksi.</span></li>';
      }

      function renderDetections(payload) {
        resizeOverlay();
        overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

        const dets = payload.detections || [];
        detectionCountText.textContent = dets.length;

        if (!dets.length) {
          detectionList.innerHTML = '<li><span class="empty-msg">Tidak ada objek terdeteksi pada frame ini.</span></li>';
          return;
        }

        const sx = overlayCanvas.width / payload.image_width;
        const sy = overlayCanvas.height / payload.image_height;
        const colors = ["#22c55e","#3b82f6","#f59e0b","#ef4444","#8b5cf6","#ec4899","#14b8a6","#f97316"];

        detectionList.innerHTML = "";
        dets.forEach((d, i) => {
          const [x1, y1, x2, y2] = d.box;
          const l = x1 * sx, t = y1 * sy, w = (x2 - x1) * sx, h = (y2 - y1) * sy;
          const color = colors[i % colors.length];

          // Kotak — stroke berwarna agar tiap objek bisa dibedakan
          overlayCtx.strokeStyle = color;
          overlayCtx.lineWidth = 3;
          overlayCtx.strokeRect(l, t, w, h);

          // Label — background gelap semi-transparan supaya teks putih selalu terbaca
          const label = d.class + " " + (d.confidence * 100).toFixed(1) + "%";
          overlayCtx.font = "bold 13px Segoe UI, sans-serif";
          const tw = overlayCtx.measureText(label).width;
          const ty = Math.max(18, t);
          overlayCtx.fillStyle = "rgba(0,0,0,0.75)";
          overlayCtx.fillRect(l, ty - 17, tw + 10, 20);
          // Strip warna tipis di sisi kiri label — penanda kelas tetap ada
          overlayCtx.fillStyle = color;
          overlayCtx.fillRect(l, ty - 17, 4, 20);
          overlayCtx.fillStyle = "#fff";
          overlayCtx.fillText(label, l + 9, ty - 2);

          // List item — warna sebagai aksen border kiri, teks gelap di atas putih
          const li = document.createElement("li");
          li.innerHTML =
            '<span class="class-badge" style="border-left:4px solid ' + color + ';background:#f8fafc;color:#1e293b">' + d.class + '</span>' +
            '<span class="conf" style="color:#1e293b">' + (d.confidence * 100).toFixed(1) + '%</span>' +
            '<span class="muted">box [' + d.box.map(v => v.toFixed(0)).join(", ") + ']</span>';
          detectionList.appendChild(li);
        });
      }

      async function fetchActiveModel() {
        try {
          const res = await fetch("/models/active");
          if (!res.ok) throw new Error();
          const data = await res.json();
          activeModelText.textContent = data.display_name || data.version || "Aktif";
        } catch {
          activeModelText.textContent = "Tidak tersedia";
        }
      }

      function closeCamera() {
        stopDetection();
        stopStream();
        videoElement.srcObject = null;
        videoElement.load();
        resetUI();
        startCameraButton.textContent = "Buka Kamera";
        startCameraButton.className = "btn-primary";
        setStatus("Kamera ditutup.", "idle");
      }

      async function openCamera() {
        stopDetection();
        stopStream();
        videoElement.srcObject = null;

        try {
          mediaStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: "environment", width: { ideal: 1280 } },
            audio: false,
          });
          videoElement.srcObject = mediaStream;
          await videoElement.play();
          resizeOverlay();
          resetUI();
          startCameraButton.textContent = "Tutup Kamera";
          startCameraButton.className = "btn-danger";
          setStatus("Kamera aktif. Tekan Mulai Deteksi untuk memproses frame.");
        } catch {
          setStatus("Gagal membuka kamera. Pastikan izin kamera sudah diberikan.", "error");
        }
      }

      function toggleCamera() {
        if (mediaStream) {
          closeCamera();
        } else {
          openCamera();
        }
      }

      function scheduleNext() {
        if (!detecting) return;
        detectionTimer = setTimeout(runCycle, Number(intervalSelect.value) || 1000);
      }

      async function runCycle() {
        if (!detecting || inflight) { scheduleNext(); return; }
        if (!videoElement.videoWidth || !videoElement.videoHeight) {
          setStatus("Video belum siap.", "error");
          scheduleNext();
          return;
        }

        inflight = true;
        detectionStateText.textContent = "Running";
        detectionStateText.classList.add("running");

        captureCanvas.width = videoElement.videoWidth;
        captureCanvas.height = videoElement.videoHeight;
        captureCtx.drawImage(videoElement, 0, 0);

        captureCanvas.toBlob(async (blob) => {
          if (!blob) { inflight = false; scheduleNext(); return; }

          const fd = new FormData();
          fd.append("file", blob, "frame.jpg");
          const thr = Number(scoreThresholdInput.value || "0.5");

          try {
            const res = await fetch("/predict?score_threshold=" + encodeURIComponent(thr), {
              method: "POST", body: fd,
            });
            if (!res.ok) {
              const err = await res.json().catch(() => ({}));
              throw new Error(err.detail || "Klasifikasi gagal");
            }
            const payload = await res.json();
            renderDetections(payload);
            setStatus("Terdeteksi " + payload.detections.length + " objek pada frame terakhir.");
          } catch (e) {
            setStatus(e.message || "Error memproses frame.", "error");
          } finally {
            inflight = false;
            if (detecting) {
              detectionStateText.textContent = "Running";
              detectionStateText.classList.add("running");
            }
            scheduleNext();
          }
        }, "image/jpeg", 0.85);
      }

      function startDetection() {
        if (!videoElement.videoWidth) {
          setStatus("Buka kamera terlebih dahulu.", "error");
          return;
        }
        if (detecting) return;
        detecting = true;
        detectionStateText.textContent = "Running";
        detectionStateText.classList.add("running");
        setStatus("Deteksi berjalan...");
        runCycle();
      }

      startCameraButton.addEventListener("click", toggleCamera);
      startDetectionButton.addEventListener("click", startDetection);
      stopDetectionButton.addEventListener("click", () => {
        stopDetection();
        setStatus("Deteksi dihentikan.", "idle");
      });

      videoElement.addEventListener("loadedmetadata", resizeOverlay);
      window.addEventListener("resize", resizeOverlay);

      fetchActiveModel();
    </script>
  </body>
</html>
"""
