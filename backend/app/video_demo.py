from __future__ import annotations


def build_video_demo_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>YOLOS Video Demo</title>
    <style>
      :root {
        color-scheme: light;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      }

      body {
        margin: 0;
        background: #f4f6fb;
        color: #1f2937;
      }

      .page {
        max-width: 1200px;
        margin: 0 auto;
        padding: 24px;
      }

      .hero {
        margin-bottom: 16px;
      }

      .hero h1 {
        margin: 0 0 8px;
        font-size: 30px;
      }

      .hero p {
        margin: 0;
        line-height: 1.6;
        color: #475569;
      }

      .panel-grid {
        display: grid;
        grid-template-columns: 340px 1fr;
        gap: 16px;
        align-items: start;
      }

      .card {
        background: #ffffff;
        border: 1px solid #dbe3f0;
        border-radius: 18px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
        padding: 18px;
      }

      .card h2,
      .card h3 {
        margin-top: 0;
      }

      .controls {
        display: grid;
        gap: 14px;
      }

      .field {
        display: grid;
        gap: 6px;
      }

      .field label {
        font-weight: 600;
        font-size: 14px;
      }

      .field input,
      .field select,
      .field button {
        font: inherit;
      }

      .field input[type="number"],
      .field select,
      .field input[type="file"] {
        width: 100%;
        box-sizing: border-box;
        padding: 10px 12px;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        background: #fff;
      }

      .button-row {
        display: grid;
        gap: 10px;
      }

      button {
        border: 0;
        border-radius: 12px;
        padding: 11px 14px;
        cursor: pointer;
        background: #0f766e;
        color: #fff;
        font-weight: 600;
      }

      button.secondary {
        background: #334155;
      }

      button.ghost {
        background: #e2e8f0;
        color: #0f172a;
      }

      button:disabled {
        cursor: not-allowed;
        opacity: 0.55;
      }

      .status {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        border-radius: 12px;
        padding: 12px 14px;
        line-height: 1.5;
      }

      .status.error {
        background: #fff1f2;
        border-color: #fecdd3;
        color: #be123c;
      }

      .video-shell {
        position: relative;
        overflow: hidden;
        border-radius: 18px;
        background: #0f172a;
        min-height: 360px;
      }

      video,
      canvas.overlay {
        display: block;
        width: 100%;
        height: auto;
      }

      canvas.overlay {
        position: absolute;
        inset: 0;
        pointer-events: none;
      }

      .stats {
        margin-top: 12px;
        display: grid;
        gap: 12px;
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }

      .stat {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px;
      }

      .stat .label {
        display: block;
        color: #64748b;
        font-size: 13px;
        margin-bottom: 6px;
      }

      .stat strong {
        font-size: 20px;
      }

      .detections {
        margin-top: 16px;
      }

      .detections ul {
        list-style: none;
        padding: 0;
        margin: 12px 0 0;
        display: grid;
        gap: 10px;
      }

      .detections li {
        border: 1px solid #dbe3f0;
        border-radius: 12px;
        padding: 12px 14px;
        background: #fff;
      }

      .muted {
        color: #64748b;
      }

      @media (max-width: 980px) {
        .panel-grid {
          grid-template-columns: 1fr;
        }

        .stats {
          grid-template-columns: 1fr;
        }
      }
    </style>
  </head>
  <body>
    <div class="page">
      <section class="hero">
        <h1>YOLOS Video Demo</h1>
        <p>
          Halaman ini adalah versi backend/Python untuk deteksi video sederhana.
          Kamera atau video dibuka di browser, lalu frame dikirim berkala ke backend
          untuk diprediksi menggunakan model aktif.
        </p>
      </section>

      <section class="panel-grid">
        <aside class="card controls">
          <div class="field">
            <label for="intervalSelect">Interval Prediksi</label>
            <select id="intervalSelect">
              <option value="1000">1 detik</option>
              <option value="500">0.5 detik</option>
              <option value="1500">1.5 detik</option>
            </select>
          </div>

          <div class="field">
            <label for="scoreThreshold">Score Threshold</label>
            <input id="scoreThreshold" type="number" min="0" max="1" step="0.05" value="0.5" />
          </div>

          <div class="field">
            <label for="videoFile">Pilih File Video</label>
            <input id="videoFile" type="file" accept="video/*" />
          </div>

          <div class="button-row">
            <button id="startCameraButton">Buka Kamera</button>
            <button id="startDetectionButton" class="secondary">Mulai Deteksi</button>
            <button id="stopDetectionButton" class="ghost">Hentikan Deteksi</button>
            <button id="stopSourceButton" class="ghost">Tutup Kamera / Video</button>
          </div>

          <div id="statusBox" class="status">
            Menunggu kamera atau video dipilih.
          </div>
        </aside>

        <main class="card">
          <div class="video-shell">
            <video id="videoElement" playsinline autoplay muted controls></video>
            <canvas id="overlayCanvas" class="overlay"></canvas>
          </div>

          <div class="stats">
            <div class="stat">
              <span class="label">Model Aktif</span>
              <strong id="activeModelText">Memuat...</strong>
            </div>
            <div class="stat">
              <span class="label">Status Deteksi</span>
              <strong id="detectionStateText">Idle</strong>
            </div>
            <div class="stat">
              <span class="label">Deteksi Terakhir</span>
              <strong id="detectionCountText">0 objek</strong>
            </div>
          </div>

          <section class="detections">
            <h3>Daftar Hasil Deteksi</h3>
            <p class="muted">
              Hasil di bawah ini menampilkan prediksi terakhir yang berhasil diterima dari backend.
            </p>
            <ul id="detectionList">
              <li class="muted">Belum ada hasil deteksi.</li>
            </ul>
          </section>
        </main>
      </section>
    </div>

    <script>
      const videoElement = document.getElementById("videoElement");
      const overlayCanvas = document.getElementById("overlayCanvas");
      const overlayContext = overlayCanvas.getContext("2d");
      const hiddenCanvas = document.createElement("canvas");
      const hiddenContext = hiddenCanvas.getContext("2d");

      const intervalSelect = document.getElementById("intervalSelect");
      const scoreThresholdInput = document.getElementById("scoreThreshold");
      const videoFileInput = document.getElementById("videoFile");
      const startCameraButton = document.getElementById("startCameraButton");
      const startDetectionButton = document.getElementById("startDetectionButton");
      const stopDetectionButton = document.getElementById("stopDetectionButton");
      const stopSourceButton = document.getElementById("stopSourceButton");
      const statusBox = document.getElementById("statusBox");
      const activeModelText = document.getElementById("activeModelText");
      const detectionStateText = document.getElementById("detectionStateText");
      const detectionCountText = document.getElementById("detectionCountText");
      const detectionList = document.getElementById("detectionList");

      let mediaStream = null;
      let uploadedVideoUrl = null;
      let detectionTimeout = null;
      let detectionActive = false;
      let requestInFlight = false;

      function setStatus(message, kind = "info") {
        statusBox.textContent = message;
        statusBox.className = kind === "error" ? "status error" : "status";
      }

      function resizeOverlay() {
        const width = videoElement.clientWidth || videoElement.videoWidth || 640;
        const height = videoElement.clientHeight || videoElement.videoHeight || 480;
        overlayCanvas.width = width;
        overlayCanvas.height = height;
        overlayCanvas.style.width = width + "px";
        overlayCanvas.style.height = height + "px";
        overlayContext.clearRect(0, 0, width, height);
      }

      function stopMediaStream() {
        if (!mediaStream) {
          return;
        }
        mediaStream.getTracks().forEach((track) => track.stop());
        mediaStream = null;
      }

      function stopUploadedVideo() {
        if (uploadedVideoUrl) {
          URL.revokeObjectURL(uploadedVideoUrl);
          uploadedVideoUrl = null;
        }
      }

      function stopDetection() {
        detectionActive = false;
        requestInFlight = false;
        detectionStateText.textContent = "Stopped";
        window.clearTimeout(detectionTimeout);
      }

      function resetDetections() {
        overlayContext.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
        detectionCountText.textContent = "0 objek";
        detectionList.innerHTML = '<li class="muted">Belum ada hasil deteksi.</li>';
      }

      function renderDetections(payload) {
        resizeOverlay();
        overlayContext.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

        const detections = payload.detections || [];
        detectionCountText.textContent = `${detections.length} objek`;

        if (!detections.length) {
          detectionList.innerHTML = '<li class="muted">Tidak ada objek yang terdeteksi pada frame terakhir.</li>';
          return;
        }

        const scaleX = overlayCanvas.width / payload.image_width;
        const scaleY = overlayCanvas.height / payload.image_height;

        detectionList.innerHTML = "";
        detections.forEach((item) => {
          const [x1, y1, x2, y2] = item.box;
          const left = x1 * scaleX;
          const top = y1 * scaleY;
          const width = (x2 - x1) * scaleX;
          const height = (y2 - y1) * scaleY;

          overlayContext.strokeStyle = "#22c55e";
          overlayContext.lineWidth = 3;
          overlayContext.strokeRect(left, top, width, height);

          const label = `${item.class} (${(item.confidence * 100).toFixed(1)}%)`;
          overlayContext.fillStyle = "#22c55e";
          overlayContext.font = "bold 14px Segoe UI";
          const textWidth = overlayContext.measureText(label).width;
          const textY = Math.max(20, top);
          overlayContext.fillRect(left, textY - 18, textWidth + 12, 22);
          overlayContext.fillStyle = "#052e16";
          overlayContext.fillText(label, left + 6, textY - 3);

          const li = document.createElement("li");
          li.textContent = `${item.class} | confidence ${(item.confidence * 100).toFixed(1)}% | box [${item.box.map((value) => value.toFixed(1)).join(", ")}]`;
          detectionList.appendChild(li);
        });
      }

      async function fetchActiveModel() {
        try {
          const response = await fetch("/models/active");
          if (!response.ok) {
            throw new Error("Model aktif belum tersedia");
          }
          const payload = await response.json();
          activeModelText.textContent = payload.display_name || payload.version || "Aktif";
        } catch (error) {
          activeModelText.textContent = "Tidak tersedia";
        }
      }

      async function startCamera() {
        stopDetection();
        stopMediaStream();
        stopUploadedVideo();
        videoElement.pause();
        videoElement.removeAttribute("src");
        videoElement.srcObject = null;

        try {
          mediaStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: "environment" },
            audio: false,
          });
          videoElement.srcObject = mediaStream;
          await videoElement.play();
          resizeOverlay();
          resetDetections();
          setStatus("Kamera berhasil dibuka. Tekan Mulai Deteksi untuk memulai prediksi frame berkala.");
        } catch (error) {
          setStatus("Kamera gagal dibuka. Pastikan browser sudah diberi izin kamera.", "error");
        }
      }

      async function loadVideoFile(file) {
        stopDetection();
        stopMediaStream();
        stopUploadedVideo();
        videoElement.pause();
        videoElement.srcObject = null;

        uploadedVideoUrl = URL.createObjectURL(file);
        videoElement.src = uploadedVideoUrl;
        try {
          await videoElement.play();
        } catch (error) {
          // Beberapa browser butuh interaksi user sebelum autoplay.
        }
        resizeOverlay();
        resetDetections();
        setStatus("Video berhasil dimuat. Tekan Mulai Deteksi untuk memproses frame berkala.");
      }

      function closeSource() {
        stopDetection();
        stopMediaStream();
        stopUploadedVideo();
        videoElement.pause();
        videoElement.removeAttribute("src");
        videoElement.srcObject = null;
        videoElement.load();
        videoFileInput.value = "";
        resetDetections();
        setStatus("Sumber video ditutup.");
      }

      function scheduleNextRun() {
        if (!detectionActive) {
          return;
        }
        const delay = Number(intervalSelect.value) || 1000;
        detectionTimeout = window.setTimeout(runDetectionCycle, delay);
      }

      async function runDetectionCycle() {
        if (!detectionActive || requestInFlight) {
          scheduleNextRun();
          return;
        }

        if (!videoElement.videoWidth || !videoElement.videoHeight) {
          setStatus("Video belum siap diproses. Tunggu beberapa saat lalu coba lagi.", "error");
          scheduleNextRun();
          return;
        }

        requestInFlight = true;
        detectionStateText.textContent = "Running";

        hiddenCanvas.width = videoElement.videoWidth;
        hiddenCanvas.height = videoElement.videoHeight;
        hiddenContext.drawImage(videoElement, 0, 0, hiddenCanvas.width, hiddenCanvas.height);

        hiddenCanvas.toBlob(async (blob) => {
          if (!blob) {
            requestInFlight = false;
            detectionStateText.textContent = "Idle";
            scheduleNextRun();
            return;
          }

          const formData = new FormData();
          formData.append("file", blob, "frame.jpg");

          const threshold = Number(scoreThresholdInput.value || "0.5");
          try {
            const response = await fetch(`/predict?score_threshold=${encodeURIComponent(threshold)}`, {
              method: "POST",
              body: formData,
            });

            if (!response.ok) {
              const errorPayload = await response.json().catch(() => ({}));
              throw new Error(errorPayload.detail || "Prediksi frame gagal");
            }

            const payload = await response.json();
            renderDetections(payload);
            setStatus(`Prediksi frame berhasil. Ditemukan ${payload.detections.length} objek pada frame terakhir.`);
          } catch (error) {
            setStatus(error.message || "Terjadi kesalahan saat memproses frame video.", "error");
          } finally {
            requestInFlight = false;
            detectionStateText.textContent = detectionActive ? "Running" : "Stopped";
            scheduleNextRun();
          }
        }, "image/jpeg", 0.92);
      }

      function startDetection() {
        if (!videoElement.videoWidth || !videoElement.videoHeight) {
          setStatus("Buka kamera atau pilih video terlebih dahulu sebelum memulai deteksi.", "error");
          return;
        }
        if (detectionActive) {
          setStatus("Deteksi sudah berjalan.");
          return;
        }

        detectionActive = true;
        detectionStateText.textContent = "Running";
        setStatus("Deteksi frame berkala dimulai.");
        runDetectionCycle();
      }

      startCameraButton.addEventListener("click", startCamera);
      startDetectionButton.addEventListener("click", startDetection);
      stopDetectionButton.addEventListener("click", () => {
        stopDetection();
        setStatus("Deteksi dihentikan.");
      });
      stopSourceButton.addEventListener("click", closeSource);

      videoFileInput.addEventListener("change", async (event) => {
        const [file] = event.target.files || [];
        if (!file) {
          return;
        }
        await loadVideoFile(file);
      });

      videoElement.addEventListener("loadedmetadata", resizeOverlay);
      window.addEventListener("resize", resizeOverlay);

      fetchActiveModel();
    </script>
  </body>
</html>
"""
