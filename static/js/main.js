// Playlist state management
let currentPlaylistUri = null;
let isTransitioningPlaylist = false;
let lastDecisionTime = null;
let lastMoodChange = null;

// Timing constants (in milliseconds)
const DECISION_COOLDOWN = 60000;      // 60 seconds between suggested changes
const MOOD_CHECK_INTERVAL = 10000;    // Check mood every 10 seconds
const EMOTION_DISPLAY_INTERVAL = 1000; // Update display every second

function initializePlaylistManagement() {
    // Add event listeners for music controls
    setupMusicControls();
    
    // Set up playlist change handlers
    setupPlaylistChangeHandlers();
}

// Update document ready function
$(document).ready(function() {
    // Initialize playlist management
    initializePlaylistManagement();
    
    // Set up single emotion check interval
    setInterval(checkEmotionAndUpdatePlaylist, MOOD_CHECK_INTERVAL);
});

function setupMusicControls() {
    $('#playButton').click(function() {
        const activity = $('#activity').val();
        const genre = $('#genre').val();
        const mood = $('#mood').val();

        if (!activity || !genre || !mood) {
            $('#message').text('Please select all options first.');
            return;
        }

        playMusic(activity, genre, mood);
    });
}

async function playMusic(activity, genre, mood) {
    try {
        const response = await fetch(`/play_music?activity=${encodeURIComponent(activity)}&genre=${encodeURIComponent(genre)}&mood=${encodeURIComponent(mood)}`);
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        $('#message').text(data.message);
        if (data.playlist_uri) {
            currentPlaylistUri = data.playlist_uri;
            updateCurrentSongDisplay();
        }
    } catch (error) {
        console.error('Error playing music:', error);
        $('#message').text('Error playing music. Please try again.');
    }
}

async function checkEmotionAndUpdatePlaylist() {
    if (isTransitioningPlaylist || !currentPlaylistUri) {
        return;
    }

    // Check only decision cooldown now
    const currentTime = Date.now();
    if (lastDecisionTime && (currentTime - lastDecisionTime) < DECISION_COOLDOWN) {
        console.log('Skipping mood check - in cooldown period');
        const remainingCooldown = DECISION_COOLDOWN - (currentTime - lastDecisionTime);
        console.log(`Cooldown remaining: ${Math.ceil(remainingCooldown / 1000)} seconds`);
        return;
    }

    try {
        const currentMood = $('#mood').val();
        const response = await fetch('/update_emotion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                current_mood: currentMood,
                current_playlist: currentPlaylistUri
            })
        });
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        updateEmotionDisplay(data.current_emotion, currentMood);

        if (data.should_change && data.suggested_mood) {
            let message;
            if (currentMood === 'energetic' || currentMood === 'happy') {
                message = `Your current emotion is ${data.current_emotion}, which is lower energy than your target. Would you like to switch to a ${data.suggested_mood} playlist to boost your energy?`;
            } else {
                message = `Your current emotion is ${data.current_emotion}, which is higher energy than your target. Would you like to switch to a ${data.suggested_mood} playlist to help you calm down?`;
            }
            
            const changeNow = confirm(message);
            lastDecisionTime = Date.now(); // Update decision timestamp regardless of choice
            
            if (changeNow) {
                await switchToNewPlaylist(data.suggested_mood);
                lastMoodChange = Date.now();
            } else {
                console.log(`User chose to stay on current playlist. Next suggestion in ${DECISION_COOLDOWN/1000} seconds.`);
                updateEmotionDisplay(data.current_emotion, currentMood, true);
            }
        }
    } catch (error) {
        console.error('Error checking emotion:', error);
    }
}


function updateEmotionDisplay(emotion, targetMood, showCooldown = false) {
    const container = document.querySelector('.emotion-detection-container');
    let displayDiv = document.getElementById('emotion-display');
    
    if (!displayDiv) {
        displayDiv = document.createElement('div');
        displayDiv.id = 'emotion-display';
        container.appendChild(displayDiv);
    }
    
    let cooldownInfo = '';
    if (showCooldown && lastDecisionTime) {
        const remainingCooldown = Math.ceil((DECISION_COOLDOWN - (Date.now() - lastDecisionTime)) / 1000);
        if (remainingCooldown > 0) {
            cooldownInfo = `<p>Next suggestion in: ${remainingCooldown} seconds</p>`;
        }
    }
    
    displayDiv.innerHTML = `
        <h3>Current State</h3>
        <p>Detected Emotion: ${emotion}</p>
        <p>Target Mood: ${targetMood}</p>
        <p>Last Updated: ${new Date().toLocaleTimeString()}</p>
        ${cooldownInfo}
    `;
}

async function handlePlaylistChange(suggestedMood) {
    if (isTransitioningPlaylist) {
        return;
    }

    const shouldChange = confirm(`Your emotional state suggests a ${suggestedMood} playlist might be better. Would you like to switch playlists?`);
    
    if (shouldChange) {
        isTransitioningPlaylist = true;
        
        try {
            await switchToNewPlaylist(suggestedMood);
        } catch (error) {
            console.error('Error during playlist transition:', error);
            $('#message').text('Error changing playlist');
        } finally {
            isTransitioningPlaylist = false;
        }
    }
}

async function getCurrentTrackInfo() {
    const response = await fetch('/current_song');
    return response.json();
}

async function switchToNewPlaylist(newMood) {
    console.log('Switching to new playlist with mood:', newMood);
    const activity = $('#activity').val();
    const genre = $('#genre').val();
    
    try {
        // Include current playlist URI to ensure we get a different one
        console.log('Requesting new playlist:', { activity, genre, newMood, currentPlaylist: currentPlaylistUri });
        const response = await fetch(
            `/play_music?` + new URLSearchParams({
                activity: activity,
                genre: genre,
                mood: newMood,
                current_playlist: currentPlaylistUri // Pass current playlist to avoid getting the same one
            })
        );
        const data = await response.json();
        console.log('Play music response:', data);
        
        if (data.error) {
            $('#message').text(`Couldn't find a different ${newMood} playlist. Try again later.`);
            throw new Error(data.error);
        }

        if (data.playlist_uri && data.playlist_uri !== currentPlaylistUri) {
            console.log('New playlist URI received:', data.playlist_uri);
            currentPlaylistUri = data.playlist_uri;
            $('#mood').val(newMood);
            $('#message').text(`Switched to ${newMood} playlist: ${data.playlist_name}`);
            updateCurrentSongDisplay();
            lastMoodChange = Date.now();
        } else {
            console.log('Received same playlist or invalid URI');
            $('#message').text(`Couldn't find a different ${newMood} playlist. Try again later.`);
        }
    } catch (error) {
        console.error('Error switching playlist:', error);
        $('#message').text('Error switching playlist. Please try again.');
        throw error; // Rethrow to handle in calling function
    }
}

// Add these functions to your main.js

function updateFeedbackDisplay() {
    const container = document.querySelector('.feedback-container');
    if (!container) return;

    // Only show feedback options if a playlist is currently playing
    if (currentPlaylistUri) {
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
    }
}

function updateCurrentSongDisplay() {
    fetch('/current_song')
        .then(response => response.json())
        .then(data => {
            if (data.track_name && data.artists) {
                document.getElementById('song-info').innerText = `${data.track_name} by ${data.artists}`;
                if (data.album_image_url) {
                    document.getElementById('album-image').src = data.album_image_url;
                    document.getElementById('album-image').style.display = 'block';
                }
                // Update feedback UI when song is playing
                updateFeedbackDisplay();
            } else {
                document.getElementById('song-info').innerText = 'No song is currently playing';
                document.getElementById('album-image').style.display = 'none';
                // Hide feedback UI when no song is playing
                document.querySelector('.feedback-container').style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error updating song display:', error);
        });
}

function updateEmotionDisplay(emotion) {
    const container = document.querySelector('.emotion-detection-container');
    let displayDiv = document.getElementById('emotion-display');
    
    if (!displayDiv) {
        displayDiv = document.createElement('div');
        displayDiv.id = 'emotion-display';
        container.appendChild(displayDiv);
    }
    
    const targetMood = $('#mood').val();
    displayDiv.innerHTML = `
        <h3>Emotion Status</h3>
        <p>Current Emotion: ${emotion}</p>
        <p>Target Mood: ${targetMood}</p>
        <p>Last Updated: ${new Date().toLocaleTimeString()}</p>
    `;
}

function setupPlaylistChangeHandlers() {
    // Set up handlers for playlist changes
    setInterval(updateCurrentSongDisplay, 1000); // Update song display every second
}

// Add basic music control functions if not already present
function pauseMusic() {
    fetch('/pause_music', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error('Error:', error));
}

function resumeMusic() {
    fetch('/resume_music', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error('Error:', error));
}

async function nextTrack() {
    // If we're supposed to change playlists, do that instead of next track
    if (pendingPlaylistChange) {
        try {
            await switchToNewPlaylist(pendingPlaylistChange.suggestedMood);
            pendingPlaylistChange = null; // Clear the pending change
            return;
        } catch (error) {
            console.error('Error switching playlist:', error);
        }
    }
    
    // Otherwise, just go to next track
    try {
        const response = await fetch('/next_track', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        console.log('Next track response:', data);
    } catch (error) {
        console.error('Error changing track:', error);
    }
}

function submitFeedback(score) {
    // Verify we have all required data
    if (!currentPlaylistUri) {
        console.log('No current playlist to rate');
        return;
    }

    const activity = $('#activity').val();
    const genre = $('#genre').val();
    const mood = $('#mood').val();

    if (!activity || !genre || !mood) {
        $('#message').text('Please select an activity, genre, and mood first.');
        return;
    }

    // Prepare feedback data
    const feedbackData = {
        activity: activity,
        genre: genre,
        mood: mood,
        playlist_uri: currentPlaylistUri,
        score: score  // 1 for positive feedback, -1 for negative
    };

    console.log('Submitting feedback:', feedbackData);

    // Send feedback to server
    fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(feedbackData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Show feedback confirmation
        const feedbackMessage = document.getElementById('feedback-message');
        feedbackMessage.textContent = 'Thanks for your feedback!';
        feedbackMessage.style.display = 'block';
        
        // Hide the message after 2 seconds
        setTimeout(() => {
            feedbackMessage.style.display = 'none';
        }, 2000);
    })
    .catch(error => {
        console.error('Error submitting feedback:', error);
        $('#message').text('Error submitting feedback. Please try again.');
    });
}


