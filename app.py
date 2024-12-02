from flask import Flask, render_template, Response, request, jsonify
from fer import FER
import cv2
import random
import time
import threading
from collections import deque
from spotipy import Spotify
from data_config import get_playlist_dict, get_training_data
from spotipy.oauth2 import SpotifyOAuth

from recommendation_engine import MusicRecommendationEngine
# Initialize the recommendation engine with training data
initial_training_data = get_training_data()
recommendation_engine = MusicRecommendationEngine()
recommendation_engine.prepare_training_data(initial_training_data)

import cv2
from fer import FER
import threading
import time

# Global variables
camera = None
frame_counter = 0
last_emotion = "No emotion detected"
lock = threading.Lock()

# Initialize FER
detector = FER(mtcnn=True)

app = Flask(__name__)

# Initialize global variables
camera = None
last_emotion = "No emotion detected"
emotion_history = deque(maxlen=30)  # Store last 30 emotion readings
lock = threading.Lock()

# Emotion detection setup
detector = FER(mtcnn=True)

# Spotify configuration
SPOTIFY_CLIENT_ID = 'a41d0355f65c4ac794e7cb098321585c'
SPOTIFY_CLIENT_SECRET = '7f97e47faffc43b391d3fa38ee6dc3c2'
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'
scope = 'user-read-playback-state user-modify-playback-state playlist-read-private playlist-modify-public playlist-read-collaborative'

spotify_auth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
)
spotify = Spotify(auth_manager=spotify_auth)

def get_camera():
    """Initialize or get existing camera instance"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError("Unable to access the camera.")
    return camera

def process_frame():
    """Process video frame and detect emotions"""
    global frame_counter, last_emotion
    camera = get_camera()
    success, frame = camera.read()

    if success:
        frame = cv2.resize(frame, (640, 480))
        
        # Only process every 10th frame for performance
        if frame_counter % 10 == 0:
            try:
                emotions = detector.detect_emotions(frame)
                if emotions:
                    emotion_data = emotions[0]['emotions']
                    strongest_emotion = max(emotion_data.items(), key=lambda x: x[1])
                    
                    with lock:
                        last_emotion = strongest_emotion[0]

                    # Draw emotion and confidence on frame
                    text = f"Emotion: {strongest_emotion[0]} ({strongest_emotion[1]:.2f})"
                    cv2.putText(frame, text, (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            except Exception as e:
                print(f"Error detecting emotions: {e}")

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        return frame_bytes
    return None

def generate_frames():
    """Generate camera frames for streaming"""
    while True:
        frame_bytes = process_frame()
        if frame_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.1)  # Reduce CPU usage

@app.route('/video_feed')
def video_feed():
    """Route for streaming video feed"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/callback')
def callback():
    """Handle Spotify authentication callback"""
    code = request.args.get('code')
    token_info = spotify_auth.get_access_token(code)
    return "Authentication successful! You can close this window."

@app.route('/get_emotion')
def get_emotion():
    """Route for getting current detected emotion"""
    with lock:
        return jsonify({'emotion': last_emotion})
    
def create_playlist(activity, genre, mood, current_playlist_uri=None):
    """Get playlist recommendations based on activity, genre, and mood"""
    try:
        playlists = []
        playlist_dict = get_playlist_dict()
        
        print(f"\nFinding playlist for: {activity} - {genre} - {mood}")
        print(f"Excluding current playlist: {current_playlist_uri}")
        
        # First try exact match from predefined playlists
        playlist_key = (activity, genre, mood)
        predefined_uri = playlist_dict.get(playlist_key)
        if predefined_uri and predefined_uri != current_playlist_uri:
            try:
                playlist_info = spotify.playlist(predefined_uri)
                playlists.append((playlist_info['name'], predefined_uri))
                print(f"Found predefined playlist: {playlist_info['name']}")
            except Exception as e:
                print(f"Error accessing predefined playlist: {e}")
        
        # Search Spotify if we need more options
        search_terms = [
            f"{activity} {genre} {mood}",
            f"{activity} {genre}",
            f"{genre} {mood}"
        ]
        
        if activity == 'exercise':
            search_terms.extend([
                f"workout {genre}",
                f"gym {genre} {mood}"
            ])
            if genre == 'hiphop':
                search_terms.extend([
                    "workout rap",
                    "gym hip hop"
                ])
        
        # Search for additional playlists
        for search_term in search_terms:
            try:
                results = spotify.search(
                    q=search_term + " playlist",
                    type='playlist',
                    limit=5  # Get more results to have options
                )
                
                if results and 'playlists' in results and results['playlists']['items']:
                    for item in results['playlists']['items']:
                        playlist_uri = item['uri']
                        # Skip if this is the current playlist
                        if playlist_uri == current_playlist_uri:
                            continue
                        # Skip if we already have this playlist
                        if not any(uri == playlist_uri for _, uri in playlists):
                            playlists.append((item['name'], playlist_uri))
                            print(f"Found playlist: {item['name']}")
                            
                if len(playlists) >= 5:  # Get multiple options
                    break
                    
            except Exception as e:
                print(f"Error searching for term '{search_term}': {e}")
                continue

        if playlists:
            print(f"Found {len(playlists)} different playlists")
            # Randomly select a playlist that's different from the current one
            selected_playlist = random.choice(playlists)
            print(f"Selected: {selected_playlist[0]}")
            return [selected_playlist]  # Return as list for compatibility
        else:
            print("No alternative playlists found")
            return None

    except Exception as e:
        print(f"Error in create_playlist: {e}")
        return None

@app.route('/play_music', methods=['GET'])
def play_music():
    """Handle playing music with improved playlist selection"""
    try:
        activity = request.args.get('activity')
        genre = request.args.get('genre')
        mood = request.args.get('mood')
        current_playlist = request.args.get('current_playlist')
        
        print(f"\nPlay music request:")
        print(f"Activity: {activity}")
        print(f"Genre: {genre}")
        print(f"Mood: {mood}")
        print(f"Current playlist: {current_playlist}")
        
        if not all([activity, genre, mood]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Get multiple playlist options
        playlists = create_playlist(activity, genre, mood)
        if not playlists:
            return jsonify({'error': 'No suitable playlists found'}), 404

        # Filter out current playlist if it exists
        different_playlists = [p for p in playlists if p[1] != current_playlist]
        
        if not different_playlists:
            return jsonify({'error': 'No different playlists available'}), 404

        # Select a random playlist from available options
        playlist_name, playlist_uri = random.choice(different_playlists)
        
        # Get active device
        devices = spotify.devices()
        if not devices['devices']:
            return jsonify({'error': 'No active Spotify device found'}), 400
        
        device_id = devices['devices'][0]['id']
        
        # Start playback
        spotify.start_playback(
            device_id=device_id,
            context_uri=playlist_uri
        )
        
        return jsonify({
            'message': f"Playing {playlist_name}",
            'playlist_uri': playlist_uri,
            'playlist_name': playlist_name
        }), 200
            
    except Exception as e:
        print(f"Error in play_music: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/update_emotion', methods=['POST'])
def update_emotion():
    """Handle emotion updates and playlist suggestions"""
    try:
        data = request.get_json()
        target_mood = data.get('current_mood', 'focus')  # Get user's target mood
        
        with lock:
            current_emotion = last_emotion
        
        emotion_history.append(current_emotion)
        
        # Pass target mood to process_emotions
        should_change, suggested_mood = process_emotions(current_emotion, target_mood)
        
        return jsonify({
            'current_emotion': current_emotion,
            'should_change': should_change,
            'suggested_mood': suggested_mood,
            'target_mood': target_mood
        }), 200
    except Exception as e:
        print(f"Error in update_emotion: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/current_song', methods=['GET'])
def current_song():
    """Get detailed information about currently playing track"""
    try:
        current_playback = spotify.current_playback()
        if current_playback and current_playback['item']:
            track = current_playback['item']
            return jsonify({
                'track_name': track['name'],
                'artists': ', '.join(artist['name'] for artist in track['artists']),
                'album_image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'is_playing': current_playback['is_playing'],
                'duration_ms': track['duration_ms'],
                'progress_ms': current_playback['progress_ms'],
                'playlist_uri': current_playback.get('context', {}).get('uri')
            })
        return jsonify({
            'message': 'No song is currently playing',
            'is_playing': False
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def process_emotions(current_emotion, target_mood):
    """Determine if playlist should change based on emotional state and target mood"""
    print("\n=== Emotion Processing Details ===")
    print(f"Current emotion: {current_emotion}")
    print(f"Target mood: {target_mood}")
    
    if len(emotion_history) < 5:
        print("Not enough emotion samples yet")
        return False, None
        
    # Map emotions to their energy/mood levels
    emotion_energy_levels = {
        'happy': 'energetic',
        'sad': 'calm',
        'angry': 'energetic',
        'fearful': 'calm',
        'fear': 'calm',
        'disgusted': 'energetic',
        'surprised': 'energetic',
        'surprise': 'energetic',
        'neutral': 'focus',
        'No emotion detected': None
    }
    
    # Define mood categories
    high_energy_moods = {'energetic', 'happy'}
    low_energy_moods = {'calm', 'focus'}
    
    # Count recent emotions
    recent_emotions = list(emotion_history)[-5:]
    emotion_counts = {}
    for emotion in recent_emotions:
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    print(f"Recent emotions: {recent_emotions}")
    print(f"Emotion counts: {emotion_counts}")
    
    # Get dominant emotion
    dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
    print(f"Dominant emotion: {dominant_emotion}")
    
    # Get the energy level of current emotion
    current_energy = emotion_energy_levels.get(dominant_emotion)
    print(f"Current energy level: {current_energy}")
    
    # Determine if we need to change based on target mood
    should_change = False
    suggested_mood = None
    
    if current_energy and emotion_counts[dominant_emotion] >= 2:
        if target_mood in high_energy_moods and current_energy == 'calm':
            # If targeting high energy but feeling calm, suggest energetic
            suggested_mood = 'energetic'
            should_change = True
        elif target_mood in low_energy_moods and current_energy == 'energetic':
            # If targeting calm/focus but feeling energetic, suggest calm
            suggested_mood = target_mood
            should_change = True
    
    print(f"Should change: {should_change}")
    print(f"Suggested mood: {suggested_mood}")
    
    return should_change, suggested_mood

def get_current_mood():
    """Helper function to get current mood from the client"""
    # You'll need to implement a way to get the current mood
    # For now, we'll use a global variable or default
    return getattr(get_current_mood, 'current_mood', 'focus')

# Add a way to update the current mood
def set_current_mood(mood):
    get_current_mood.current_mood = mood

def get_random_track_offset(playlist_uri):
    """Get random track position for playlist"""
    try:
        playlist = spotify.playlist(playlist_uri)
        total_tracks = playlist['tracks']['total']
        return random.randint(0, max(0, total_tracks - 1))
    except Exception as e:
        print(f"Error getting random track: {e}")
        return 0

# Basic playback control routes
@app.route('/pause_music', methods=['POST'])
def pause_music():
    try:
        spotify.pause_playback()
        return jsonify({'message': 'Playback paused'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resume_music', methods=['POST'])
def resume_music():
    try:
        spotify.start_playback()
        return jsonify({'message': 'Playback resumed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/next_track', methods=['POST'])
def next_track():
    try:
        spotify.next_track()
        return jsonify({'message': 'Skipped to next track'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/feedback', methods=['POST'])
def handle_feedback():
    """Handle user feedback about playlists"""
    try:
        # Check if the request has JSON data
        if not request.is_json:
            return jsonify({'error': 'Missing JSON in request'}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['activity', 'genre', 'mood', 'playlist_uri', 'score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field} in request'}), 400

        # Get current emotion with lock to ensure thread safety
        with lock:
            current_emotion = last_emotion
            
        # Log the interaction in the recommendation engine
        recommendation_engine.log_interaction(
            user_id='default_user',  # You can implement user tracking later
            activity=data['activity'],
            genre=data['genre'],
            mood=data['mood'],
            emotion=current_emotion,
            playlist_uri=data['playlist_uri'],
            feedback_score=data['score']
        )
        
        print(f"Received feedback: {data}")
        print(f"Current emotion during feedback: {current_emotion}")
        
        return jsonify({
            'message': 'Feedback received successfully',
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error handling feedback: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Failed to open the camera. Exiting.")
        exit(1)
        
    app.run(debug=True)