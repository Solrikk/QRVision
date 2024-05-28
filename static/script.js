const video = document.getElementById('video');
const captureBtn = document.getElementById('captureBtn');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Ошибка доступа к камере: ", err);
    });

captureBtn.addEventListener('click', () => {
    setTimeout(() => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.style.display = 'block';
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
                alert('Данные QR-кода: ' + data.data);
                canvas.style.display = 'none';
            })
            .catch(error => {
                console.error('Ошибка:', error);
                canvas.style.display = 'none';
            });
        }, 'image/png');
    }, 500);
});
