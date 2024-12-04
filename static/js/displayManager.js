import { state } from './state.js';

// this function updates what song is playing at the momenmt 
export function updateCurrentSongDisplay() {
    // grab the current song from the server
    fetch('/current_song')
        .then(response => response.json())
        .then(data => {
            // check if we got a song playing
            if (data.track_name && data.artists) {
                // put the song name and artist on the page
                document.getElementById('song-info').innerText = `${data.track_name} by ${data.artists}`;
                // if we got an album pic show it
                if (data.album_image_url) {
                    document.getElementById('album-image').src = data.album_image_url;
                    document.getElementById('album-image').style.display = 'block';
                }
                updateFeedbackDisplay(); // show user feedback buttons
            } else {
                // no song playing so clear everything
                document.getElementById('song-info').innerText = 'No song is currently playing';
                document.getElementById('album-image').style.display = 'none';
                document.querySelector('.feedback-container').style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error updating song display:', error);
        });
}

// this shows what emotion the camera thinks u have
export function updateEmotionDisplay(emotion, targetMood, showCooldown = false) {
    // find the container where we show emotions
    const container = document.querySelector('.emotion-detection-container');
    let displayDiv = document.getElementById('emotion-display');
    
    // make a new div if we dont have one yet
    // havent needed to use this anymore but fixed previous problems
    if (!displayDiv) {
        displayDiv = document.createElement('div');
        displayDiv.id = 'emotion-display';
        container.appendChild(displayDiv);
    }
    
    // figure out if we need to show the cooldown timer
    let cooldownInfo = '';
    if (showCooldown && state.lastDecisionTime) {
        // math stuff to show how many seconds till next suggestion
        const remainingCooldown = Math.ceil((constants.DECISION_COOLDOWN - (Date.now() - state.lastDecisionTime)) / 1000);
        if (remainingCooldown > 0) {
            cooldownInfo = `<p>Next suggestion in: ${remainingCooldown} seconds</p>`;
        }
    }
    
    // put all the emotion info on the screen
    // displayDiv.innerHTML = `
    //     <h3>Current State</h3>
    //     <p>Detected Emotion: ${emotion}</p>
    //     <p>Target Mood: ${targetMood}</p>
    //     <p>Last Updated: ${new Date().toLocaleTimeString()}</p>
    //     ${cooldownInfo}
    // `;
}

// this shows or hides the feedback buttons 
function updateFeedbackDisplay() {
    // find the feedback container
    const container = document.querySelector('.feedback-container');
    if (!container) return;

    // only show feedback buttons if we got a playlist playing
    if (state.currentPlaylistUri) {
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
    }
}