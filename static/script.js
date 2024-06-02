const video = document.getElementById('video');
const captureBtn = document.getElementById('captureBtn');
const qrCount = document.getElementById('qrCount');
const processingStatus = document.getElementById('processingStatus');
let currentCount = 0;

navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } })
    .then(stream => {
        video.srcObject = stream;

        const ws = new WebSocket('ws://' + window.location.host + '/stream');
        ws.onopen = () => {
            setInterval(() => {
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                canvas.toBlob(blob => {
                    ws.send(blob);
                }, 'image/jpeg');
            }, 1000);
        };
    })
    .catch(err => {
        console.error("Ошибка доступа к камере: ", err);
    });

captureBtn.addEventListener('click', () => {
    processingStatus.style.display = 'block';
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'capture.png');

        fetch('/scan-qr/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then((data) => {
            if (data.data && data.data !== "No QR code found.") {
                currentCount += data.data.length;
                qrCount.textContent = currentCount;
            } else {
                alert('Данные QR-кода: ' + data.data);
            }
            processingStatus.style.display = 'none';
        })
        .catch(error => {
            console.error('Ошибка:', error);
            processingStatus.style.display = 'none';
        });
    }, 'image/png');
});
