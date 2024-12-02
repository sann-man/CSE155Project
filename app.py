# app.py
from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from emotion_detector import EmotionDetector
from spotify_handler import SpotifyHandler
from config import SPOTIFY_CONFIG
from playlist_manager import create_playlist, process_emotions
from collections import deque
import threading
import time

app = Flask(__name__)

# Initialize global variables and components
emotion_detector = EmotionDetector()
spotify_handler = SpotifyHandler(SPOTIFY_CONFIG)
emotion_history = deque(maxlen=30)  # Store last 30 emotion readings
lock = threading.Lock()

@app.route('/')
def index():
    # serve the main page
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Route for streaming video feed
    return Response(emotion_detector.generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/callback')
def callback():
    # spotify authentication callback route 
    code = request.args.get('code')
    return spotify_handler.handle_callback(code)

@app.route('/get_emotion')
def get_emotion():
    # route for getting current detected emotion
    with lock:
        return jsonify({'emotion': emotion_detector.last_emotion})

@app.route('/play_music', methods=['GET'])
def play_music():
    # Handle playing music with improved playlist selection
    return spotify_handler.handle_play_music(request)

@app.route('/update_emotion', methods=['POST'])
def update_emotion():
    # handle emotion updates and playlist suggestions
    try:
        data = request.get_json()
        target_mood = data.get('current_mood', 'focus')
        
        with lock:
            current_emotion = emotion_detector.last_emotion
        
        emotion_history.append(current_emotion)
        should_change, suggested_mood = process_emotions(emotion_history, current_emotion, target_mood)
        
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
    # Get detailed information about currently playing track
    return spotify_handler.get_current_song()

# Basic playback control routes
@app.route('/pause_music', methods=['POST'])
def pause_music():
    return spotify_handler.pause_playback()

@app.route('/resume_music', methods=['POST'])
def resume_music():
    return spotify_handler.resume_playback()

@app.route('/next_track', methods=['POST'])
def next_track():
    return spotify_handler.next_track()

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    # Handle user feedback about playlists
    try:
        if not request.is_json:
            return jsonify({'error': 'Missing JSON in request'}), 400
        
        data = request.get_json()
        required_fields = ['activity', 'genre', 'mood', 'playlist_uri', 'score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field} in request'}), 400

        with lock:
            current_emotion = emotion_detector.last_emotion
            
        spotify_handler.recommendation_engine.log_interaction(
            user_id='default_user',
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
    
@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

if __name__ == '__main__':
    app.run(debug=True)