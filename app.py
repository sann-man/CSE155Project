from flask import Flask, render_template, Response, request, jsonify
import cv2
from fer import FER
import time
import threading
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Initialize the FER emotion detector
detector = FER(mtcnn=True)

# Spotify configuration
SPOTIFY_CLIENT_ID = 'a41d0355f65c4ac794e7cb098321585c'  # Replace with your Spotify Client ID
SPOTIFY_CLIENT_SECRET = '7f97e47faffc43b391d3fa38ee6dc3c2'  # Replace with your Spotify Client Secret
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'

scope = 'user-read-playback-state user-modify-playback-state playlist-read-private playlist-modify-public'
spotify_auth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                            client_secret=SPOTIFY_CLIENT_SECRET,
                            redirect_uri=SPOTIFY_REDIRECT_URI,
                            scope=scope)
spotify = Spotify(auth_manager=spotify_auth)

# Global variables
camera = None
last_emotion = "No emotion detected"
frame_counter = 0
lock = threading.Lock()

def get_camera():
    """Get or create camera instance"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)  # 0 is usually the built-in webcam
        if not camera.isOpened():
            raise RuntimeError("Unable to access the camera.")
    return camera

def process_frame():
    """Get a frame from the camera and process it"""
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

                    # Draw the emotion text on the frame
                    cv2.putText(frame, 
                                f"Emotion: {strongest_emotion}", 
                                (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1, 
                                (0, 255, 0), 
                                2)
            except Exception as e:
                print(f"Error detecting emotions: {e}")

        # Encode the frame to JPEG
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
        time.sleep(0.1)  # Small delay to reduce CPU usage

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video feed route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotion')
def get_emotion():
    """Get the current emotion"""
    with lock:
        return jsonify({'emotion': last_emotion})

@app.route('/callback')
def callback():
    """Spotify authentication callback"""
    code = request.args.get('code')
    token_info = spotify_auth.get_access_token(code)
    return "Spotify authentication successful. You can return to the app."

playlist_dict = {
    ('study', 'pop', 'happy'): 'spotify:playlist:37i9dQZF1DWSoyxGghlqv5',
    # Add more combinations and their corresponding playlist URIs
}

def create_playlist(activity, genre, mood):
    """Fetch a playlist based on activity, genre, and mood from a predefined dictionary"""
    # Check predefined dictionary first
    playlist_uri = playlist_dict.get((activity, genre, mood))
    
    if playlist_uri:
        return playlist_uri
    else:
        # Search Spotify with the given combination
        playlist_name = f"{activity} {genre} {mood}"
        results = spotify.search(q=playlist_name, type='playlist', limit=5)  # Get up to 5 playlists for variety
        if results['playlists']['items']:
            # Return a list of URIs and names for better selection
            playlists = [(item['name'], item['uri']) for item in results['playlists']['items']]
            return playlists
        else:
            return None

@app.route('/play_music', methods=['GET'])
def play_music():
    """Play music based on the selected activity, genre, and mood"""
    activity = request.args.get('activity')
    genre = request.args.get('genre')
    mood = request.args.get('mood')

    playlist_result = create_playlist(activity, genre, mood)

    if playlist_result:
        if isinstance(playlist_result, list):
            # Multiple playlists found - pick the first one or return a choice to user
            playlist_name, playlist_uri = playlist_result[0]  # You could implement a user choice here
        else:
            # Single playlist found in the dictionary
            playlist_uri = playlist_result
        
        # Start playing the playlist
        devices = spotify.devices()
        if devices['devices']:
            spotify.start_playback(device_id=devices['devices'][0]['id'], context_uri=playlist_uri)
            return jsonify({'message': f"Playing {activity} {genre} {mood} playlist: {playlist_name}"})
        else:
            return jsonify({'message': "No device available."})
    else:
        return jsonify({'message': "No playlist found matching the given criteria."})


if __name__ == '__main__':
    # Pre-initialize the camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Failed to open the camera. Exiting.")
        exit(1)

    app.run(debug=True)