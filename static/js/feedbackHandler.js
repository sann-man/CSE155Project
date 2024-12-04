// need this for checking if we have a playlist playing
import { state } from './state.js';

// user feedback managment 

// this function runs when feedback buttons are clicked 
export function submitFeedback(score) {
    // make sure we actually have a playlist to rate
    if (!state.currentPlaylistUri) {
        console.log('No current playlist to rate');
        return;
    }

    // drop down info 
    const activity = $('#activity').val();
    const genre = $('#genre').val();
    const mood = $('#mood').val();

    // make sure they picked everything we need
    if (!activity || !genre || !mood) {
        $('#message').text('Please select an activity, genre, and mood first.');
        return;
    }

    // put all the feedback info together in one object
    const feedbackData = {
        activity: activity,
        genre: genre,
        mood: mood,
        playlist_uri: state.currentPlaylistUri,
        score: score  // score is 1 for thumbs up -1 for thumbs down
    };

    // send the feedback to our server
    fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(feedbackData)
    })
    .then(response => {
        // if something went wrong with the request throw an error
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        // show the thanks message
        // having problems dispalying feedback info
        const feedbackMessage = document.getElementById('feedback-message');
        feedbackMessage.textContent = 'Thanks for your feedback!';
        feedbackMessage.style.display = 'block';
        
        // make the message go away after 2 seconds
        setTimeout(() => {
            feedbackMessage.style.display = 'none';
        }, 2000);
    })
    .catch(error => {
        console.error('Error submitting feedback:', error);
        $('#message').text('Error submitting feedback. Please try again.');
    });
}