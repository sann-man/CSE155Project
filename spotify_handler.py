from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from recommendation_engine import MusicRecommendationEngine
from data_config import get_training_data
from playlist_manager import create_playlist
from flask import jsonify
import random 

# playing music and changing songs
# handles all sptoify stuff 

class SpotifyHandler:
    def __init__(self, config):
        # set up spotify connection with our app info
        # from config 
        self.spotify_auth = SpotifyOAuth(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            redirect_uri=config['redirect_uri'],
            scope=config['scope']
        )
        self.spotify = Spotify(auth_manager=self.spotify_auth)
        
        # Initialize recommendation engine
        initial_training_data = get_training_data()
        self.recommendation_engine = MusicRecommendationEngine()
        self.recommendation_engine.prepare_training_data(initial_training_data)

    def handle_callback(self, code):

        # handle Spotify authentication callback
        token_info = self.spotify_auth.get_access_token(code)
        return "authentication success!"

    def handle_play_music(self, request):
        # Handle playing music request
        try:
            activity = request.args.get('activity')
            genre = request.args.get('genre')
            mood = request.args.get('mood')
            current_playlist = request.args.get('current_playlist')
            
            if not all([activity, genre, mood]):
                return jsonify({'error': 'Missing required parameters'}), 400

            playlists = create_playlist(self.spotify, activity, genre, mood, current_playlist)
            if not playlists:
                return jsonify({'error': 'No suitable playlists found'}), 404

            different_playlists = [p for p in playlists if p[1] != current_playlist]
            if not different_playlists:
                return jsonify({'error': 'No different playlists available'}), 404

            playlist_name, playlist_uri = random.choice(different_playlists)
            
            devices = self.spotify.devices()
            if not devices['devices']:
                return jsonify({'error': 'No active Spotify device found'}), 400
            
            device_id = devices['devices'][0]['id']
            
            self.spotify.start_playback(
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

    def get_current_song(self):
    #    get current playing song information
        try:
            current_playback = self.spotify.current_playback()
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

    def pause_playback(self):
        try:
            self.spotify.pause_playback()
            return jsonify({'message': 'Playback paused'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def resume_playback(self):
        try:
            self.spotify.start_playback()
            return jsonify({'message': 'Playback resumed'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def next_track(self):
        try:
            self.spotify.next_track()
            return jsonify({'message': 'Skipped to next track'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500