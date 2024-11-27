from flask import Flask, render_template, Response, request, jsonify
import cv2
import random
from fer import FER
import time
import threading
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# initialize the FER emotion detector
detector = FER(mtcnn=True)

# spotify configuration stuff
SPOTIFY_CLIENT_ID = 'a41d0355f65c4ac794e7cb098321585c' 
SPOTIFY_CLIENT_SECRET = '7f97e47faffc43b391d3fa38ee6dc3c2'  
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'

scope = 'user-read-playback-state user-modify-playback-state playlist-read-private playlist-modify-public'
spotify_auth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                            client_secret=SPOTIFY_CLIENT_SECRET,
                            redirect_uri=SPOTIFY_REDIRECT_URI,
                            scope=scope)
spotify = Spotify(auth_manager=spotify_auth)

# variables 
camera = None
last_emotion = "No emotion detected"
frame_counter = 0
lock = threading.Lock()


# --------- WEB AND FER implementation ------------
# get camera 
def get_camera():
    # get or create camera instance
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)  # 0 for built in webcam 
        if not camera.isOpened():
            raise RuntimeError("Unable to access the camera.")
    return camera

# process frames 
def process_frame():
    # Get a frame from the camera and process it
    global frame_counter, last_emotion
    camera = get_camera()
    success, frame = camera.read()

    if success:
        # Resize the frame to improve processing speed
        frame = cv2.resize(frame, (640, 480))
        frame_counter += 1

        # Process every 10th frame to reduce load
        if frame_counter % 10 == 0:
            try:
                emotions = detector.detect_emotions(frame)
                if emotions:  # If a face was detected
                    emotion_data = emotions[0]['emotions']
                    strongest_emotion = max(emotion_data.items(), key=lambda x: x[1])[0]

                    # Update the global emotion variable
                    with lock:
                        last_emotion = strongest_emotion

                    # draw the emotion text on the frame
                    cv2.putText(frame, 
                                f"Emotion: {strongest_emotion}", 
                                (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1, 
                                (0, 255, 0), 
                                2)
            except Exception as e:
                print(f"Error detecting emotions: {e}")

        # encode the frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        return frame_bytes
    return None

def generate_frames():
    """Generate camera frames"""
    while True:
        frame_bytes = process_frame()
        if frame_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.1)  # helps with CPU usage

@app.route('/')
def home():
    # home page route 
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # vide feed route 
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotion')
def get_emotion():
    # get current emotion
    with lock:
        return jsonify({'emotion': last_emotion})

@app.route('/callback')
def callback():
    # authetnication for spotify 
    code = request.args.get('code')
    token_info = spotify_auth.get_access_token(code)
    return "Spotify authentication successful. You can return to the app."

# add more to playlist
# add functionality to stop certain playlist from appearing in same setting...

playlist_dict = {
    ('study', 'pop', 'happy'): 'spotify:playlist:37i9dQZF1DWSoyxGghlqv5',
}

def create_playlist(activity, genre, mood):
    # get a playlist based on activity genre and mood from a predefined dictionay
    # Check predefined dictionary first
    playlist_uri = playlist_dict.get((activity, genre, mood))
    
    if playlist_uri:
        return playlist_uri
    else:
        # Search Spotify with the given combination
        playlist_name = f"{activity} {genre} {mood}"
        results = spotify.search(q=playlist_name, type='playlist', limit=5)  #playlist amount 
        if results['playlists']['items']:
            # Return a list of URIs and names for better selection
            playlists = [(item['name'], item['uri']) for item in results['playlists']['items']]
            return playlists
        else:
            return None

@app.route('/play_music', methods=['GET'])
def play_music():
    # Play music based on the selected items 
    activity = request.args.get('activity')
    genre = request.args.get('genre')
    mood = request.args.get('mood')

    playlist_result = create_playlist(activity, genre, mood)

    if isinstance(playlist_result, list):
        # Pick a random playlist from the list

        playlist_name, playlist_uri = random.choice(playlist_result)
    elif playlist_result:
        # If it's a single playlist, just use it

        playlist_uri = playlist_result
        playlist_name = 'Selected playlist'  

    if playlist_uri:

        # Start playing the playlist

        devices = spotify.devices()
        if devices['devices']:
            spotify.start_playback(device_id=devices['devices'][0]['id'], context_uri=playlist_uri)
            return jsonify({'message': f"Playing {activity} {genre} {mood} playlist: {playlist_name}"})
        else:
            return jsonify({'message': "No device available."})
    else:
        return jsonify({'message': "No playlist found matching the given criteria."})

    

@app.route('/pause_music', methods=['POST'])
def pause_music():
    # Pause currently playing music
    try:
        spotify.pause_playback()
        return jsonify({'message': 'Playback paused successfully.'})
    except Exception as e:
        return jsonify({'error': f"Unable to pause playback: {e}"})


@app.route('/resume_music', methods=['POST'])
def resume_music(): 
    try:
        spotify.start_playback()
        return jsonify({'message': 'Playback resumed successfully.'})
    except Exception as e:
        return jsonify({'error': f"Unable to resume playback: {e}"})


@app.route('/next_track', methods=['POST'])
def next_track():
    try:
        spotify.next_track()
        return jsonify({'message': 'Skipped to the next track.'})
    except Exception as e:
        return jsonify({'error': f"Unable to skip to the next track: {e}"})
    
@app.route('/current_song', methods=['GET'])
def current_song():
    # get details of the currently playing song
    try:
        current_playback = spotify.current_playback()
        if current_playback and current_playback['item']:
            track = current_playback['item']
            track_name = track['name']
            artists = ', '.join(artist['name'] for artist in track['artists'])
            album_image_url = track['album']['images'][0]['url']  # get the album image URL
            is_playing = current_playback['is_playing']

            return jsonify({
                'track_name': track_name,
                'artists': artists,
                'album_image_url': album_image_url,
                'is_playing': is_playing
            })
        else:
            return jsonify({'message': 'No song is currently playing.'})
    except Exception as e:
        return jsonify({'error': f"Unable to get current song: {e}"})


if __name__ == '__main__':
    # Pre-initialize the camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Failed to open the camera. Exiting.")
        exit(1)

    app.run(debug=True)