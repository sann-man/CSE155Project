// this file controls playing pausing and changing songs


import { state } from './state.js';
import { updateCurrentSongDisplay } from './displayManager.js';

// this starts playing music based on what the user picked
export async function playMusic(activity, genre, mood) {
   try {
       // ask server to play music with these options
       // encodeuricomponent makes sure the urls work right with spaces
       const response = await fetch(`/play_music?activity=${encodeURIComponent(activity)}&genre=${encodeURIComponent(genre)}&mood=${encodeURIComponent(mood)}`);
       const data = await response.json();
       
       // if server had a problem stop here
       if (data.error) {
           throw new Error(data.error);
       }

       // show message from server
       $('#message').text(data.message);
       // if we got a playlist save it and update display
       if (data.playlist_uri) {
           state.currentPlaylistUri = data.playlist_uri;
           updateCurrentSongDisplay();
       }
   } catch (error) {
       console.error('Error playing music:', error);
       $('#message').text('Error playing music. Please try again.');
   }
}

// tells spotify to pause the music
export function pauseMusic() {
   fetch('/pause_music', { method: 'POST' })
       .then(response => response.json())
       .then(data => console.log(data.message))
       .catch(error => console.error('Error:', error));
}

// tells spotify to start playing again
export function resumeMusic() {
   fetch('/resume_music', { method: 'POST' })
       .then(response => response.json())
       .then(data => console.log(data.message))
       .catch(error => console.error('Error:', error));
}

// skips to next song
export async function nextTrack() {
   try {
       // tell server to go to next track
       const response = await fetch('/next_track', { 
           method: 'POST',
           headers: {
               'Content-Type': 'application/json'
           }
       });
       const data = await response.json();
       // print what server said
       console.log('Next track response:', data);
   } catch (error) {
       // something broke when changing tracks
       console.error('Error changing track:', error);
   }
}