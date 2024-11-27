$(document).ready(function() {
    $('#playButton').click(function() {
        var activity = $('#activity').val();
        var genre = $('#genre').val();
        var mood = $('#mood').val();

        if (!activity || !genre || !mood) {
            $('#message').text('Please select an activity, genre, and mood.');
            return;
        }

        $.getJSON('/play_music', {activity: activity, genre: genre, mood: mood}, function(data) {
            $('#message').text(data.message);
        });
    });
});

function pauseMusic() {
    fetch('/pause_music', {method: 'POST'})
        .then(response => response.json())
        .then(data => alert(data.message || data.error));
}

function resumeMusic() {
    fetch('/resume_music', {method: 'POST'})
        .then(response => response.json())
        .then(data => alert(data.message || data.error));
}

function nextTrack() {
    fetch('/next_track', {method: 'POST'})
        .then(response => response.json())
        .then(data => alert(data.message || data.error));
}

function getCurrentSong() {
    fetch('/current_song', {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            if (data.track_name && data.artists && data.album_image_url) {
                let songStatus = '';

                if (data.is_playing) {
                    songStatus = `${data.track_name} by ${data.artists}`;
                } else {
                    songStatus = `Song: ${data.track_name} by ${data.artists} is paused`;
                }

                document.getElementById('song-info').innerText = songStatus;
                document.getElementById('album-image').src = data.album_image_url;
                document.getElementById('album-image').style.display = 'block';
            } else if (data.message) {
                document.getElementById('song-info').innerText = 'No song is currently playing.';
                document.getElementById('album-image').style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching current song:', error);
        });
}

// Automatically refresh the current song every 2 seconds for a faster update
setInterval(getCurrentSong, 2000);

// Run the function once initially to load song info immediately when the page is loaded
getCurrentSong();