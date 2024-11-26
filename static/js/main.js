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