// Update emotion every second
setInterval(() => {
    fetch('/get_emotion')
        .then(response => response.json())
        .then(data => {
            document.getElementById('current-emotion').textContent = data.emotion;
        });
}, 1000);