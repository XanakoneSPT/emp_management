// Department filter auto-submit
document.getElementById('department').addEventListener('change', function() {
    this.form.submit();
});

// Face registration with camera
let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let preview = document.getElementById('preview');
let startButton = document.getElementById('startCamera');
let captureButton = document.getElementById('capturePhoto');
let submitBtn = document.getElementById('submitBtn');
let stream = null;

// Handle file upload
document.getElementById('face_image').addEventListener('change', function(e) {
    if (this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            video.style.display = 'none';
            captureButton.style.display = 'none';
            submitBtn.style.display = 'block';
        };
        reader.readAsDataURL(this.files[0]);
    }
});

// Start camera
startButton.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 }
            }
        });
        video.srcObject = stream;
        video.style.display = 'block';
        preview.style.display = 'none';
        startButton.style.display = 'none';
        captureButton.style.display = 'block';
        video.play();
    } catch (err) {
        console.error('Error accessing camera:', err);
        alert('Lỗi truy cập camera. Vui lòng đảm bảo bạn đã cấp quyền truy cập camera.');
    }
});

// Capture photo
captureButton.addEventListener('click', () => {
    const employeeId = captureButton.getAttribute('data-employee-id');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let image = canvas.toDataURL('image/jpeg');
    preview.src = image;
    preview.style.display = 'block';
    video.style.display = 'none';
    captureButton.style.display = 'none';
    submitBtn.style.display = 'block';
    
    // Convert base64 to blob
    fetch(image)
        .then(res => res.blob())
        .then(blob => {
            // Use employee ID in the filename
            const file = new File([blob], `${employeeId}.jpg`, { type: "image/jpeg" });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            document.getElementById('face_image').files = dataTransfer.files;
        });
    
    // Stop the camera
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
}); 