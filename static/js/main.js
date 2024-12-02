// get all the stuff we need from other files
import { state, constants } from './state.js';
import { playMusic, pauseMusic, resumeMusic, nextTrack } from './musicControls.js';
import { updateCurrentSongDisplay, updateEmotionDisplay } from './displayManager.js';
import { switchToNewPlaylist } from './playlistManager.js';
import { submitFeedback } from './feedbackHandler.js';

window.pauseMusic = pauseMusic;
window.resumeMusic = resumeMusic;
window.nextTrack = nextTrack;
window.submitFeedback = submitFeedback;

// sets up what happens when user click the play button
function setupMusicControls() {
   $('#playButton').click(function() {
       // get what the user picked from dropdowns
       const activity = $('#activity').val();
       const genre = $('#genre').val();
       const mood = $('#mood').val();

       // make sure they picked everything
       if (!activity || !genre || !mood) {
           $('#message').text('Please select all options first.');
           return;
       }

       // start playing music with their choices
       playMusic(activity, genre, mood);
   });
}

// this checks ur emotion and maybe changes playlist if needed
async function checkEmotionAndUpdatePlaylist() {
   // dont do anything if were already switching playlists
   if (state.isTransitioningPlaylist || !state.currentPlaylistUri) {
       return;
   }

   // check if we need to wait before suggesting again
   const currentTime = Date.now();
   if (state.lastDecisionTime && (currentTime - state.lastDecisionTime) < constants.DECISION_COOLDOWN) {
       return;
   }

   try {
       // get current mood and ask server about emotion
       const currentMood = $('#mood').val();
       const response = await fetch('/update_emotion', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({
               current_mood: currentMood,
               current_playlist: state.currentPlaylistUri
           })
       });
       const data = await response.json();

       // if something went wrong stop here
       if (data.error) throw new Error(data.error);

       // show the emotion on screen
       updateEmotionDisplay(data.current_emotion, currentMood);

       // check if we should change the playlist
       if (data.should_change && data.suggested_mood) {
           // ask user if they wanna change playlist
           const changeNow = confirm(
               currentMood === 'energetic' || currentMood === 'happy'
                   ? `Your current emotion is ${data.current_emotion}, which is lower energy than your target. Would you like to switch to a ${data.suggested_mood} playlist to boost your energy?`
                   : `Your current emotion is ${data.current_emotion}, which is higher energy than your target. Would you like to switch to a ${data.suggested_mood} playlist to help you calm down?`
           );
           
           // remember when we last asked about changing
           state.lastDecisionTime = Date.now();
           
           // if they said yes change playlist 
        //    if no just update display
           if (changeNow) {
               await switchToNewPlaylist(data.suggested_mood);
               state.lastMoodChange = Date.now();
           } else {
               updateEmotionDisplay(data.current_emotion, currentMood, true);
           }
       }
   } catch (error) {
       console.error('Error checking emotion:', error);
   }
}

// this gets everything started
function initializePlaylistManagement() {
   // set up the play button
   setupMusicControls();
   // update what song is playing every second
   setInterval(updateCurrentSongDisplay, constants.EMOTION_DISPLAY_INTERVAL);
}

// when page loads start everything up
$(document).ready(function() {
   initializePlaylistManagement();
   // check emotion every 10 seconds
   setInterval(checkEmotionAndUpdatePlaylist, constants.MOOD_CHECK_INTERVAL);
});