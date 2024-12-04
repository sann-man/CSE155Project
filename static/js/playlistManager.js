
import { state, constants } from './state.js';
import { updateCurrentSongDisplay, updateEmotionDisplay } from './displayManager.js';
// handles switching between playlists

// this function changes to a new playlist when ur mood changes
export async function switchToNewPlaylist(newMood) {

   // lets us know plkaylist is swithcing 
   console.log('Switching to new playlist with mood:', newMood);
   // get what activity / genre user picked before
   const activity = $('#activity').val();
   const genre = $('#genre').val();
   
   try {
       // ask server for a new playlist
       // we send the current playlist so it doesnt give us the same one again
       const response = await fetch(
           `/play_music?` + new URLSearchParams({
               activity: activity,
               genre: genre,
               mood: newMood,
               current_playlist: state.currentPlaylistUri
           })
       );
       const data = await response.json();
       
       // if server had a problem tell the user
       if (data.error) {
           $('#message').text(`Couldn't find a different ${newMood} playlist. Try again later.`);
           throw new Error(data.error);
       }

       // check if we got a new playlist thats different from current one
       if (data.playlist_uri && data.playlist_uri !== state.currentPlaylistUri) {
           // save the new playlist
           state.currentPlaylistUri = data.playlist_uri;
           // update the mood dropdown to match new playlist
           $('#mood').val(newMood);

           // tell user we switched playlists
           $('#message').text(`Switched to ${newMood} playlist: ${data.playlist_name}`);
           // update whats showing on screen
           updateCurrentSongDisplay();
           // remember when we changed mood
           
           state.lastMoodChange = Date.now();
       } else {
           // couldnt find a different playlist
           $('#message').text(`Couldn't find a different ${newMood} playlist. Try again later.`);
       }
   } catch (error) {
       console.error('Error switching playlist:', error);
       $('#message').text('Error switching playlist. Please try again.');
       throw error;
   }
}