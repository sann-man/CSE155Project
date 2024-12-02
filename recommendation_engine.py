from collections import defaultdict
import pandas as pd

class MusicRecommendationEngine:
    def __init__(self):
        self.emotion_to_mood = {
            'happy': 'happy',
            'sad': 'calm',
            'angry': 'calm',
            'fearful': 'calm',
            'disgusted': 'energetic',
            'surprised': 'energetic',
            'neutral': 'focus',
            'No emotion detected': 'focus'
        }
        
        self.feedback_history = defaultdict(list)
        self.playlist_data = None

    def prepare_training_data(self, training_data):
        # store the training data for future recommendations
        self.playlist_data = training_data
        return self

    def get_playlist_recommendation(self, activity, genre, target_mood, current_emotion):
        # get playlist recommendation based on current context
        try:
            if self.playlist_data is None:
                print("No training data available")
                return None

            matching_playlists = self.playlist_data[
                (self.playlist_data['activity'] == activity) &
                (self.playlist_data['genre'] == genre) &
                (self.playlist_data['mood'] == target_mood)
            ]

            if matching_playlists.empty:
                matching_playlists = self.playlist_data[
                    (self.playlist_data['activity'] == activity) &
                    (self.playlist_data['genre'] == genre)
                ]

            if not matching_playlists.empty:
                return matching_playlists['playlist_uri'].sample().iloc[0]
            
            return None

        except Exception as e:
            print(f"Error in recommendation: {str(e)}")
            return None

    def log_interaction(self, user_id, activity, genre, mood, emotion, playlist_uri, feedback_score):
        # Log user interaction with a playlist
        try:
            interaction = {
                'timestamp': pd.Timestamp.now(),
                'activity': activity,
                'genre': genre,
                'mood': mood,
                'emotion': emotion,
                'playlist_uri': playlist_uri,
                'feedback_score': feedback_score
            }
            
            self.feedback_history[user_id].append(interaction)
            print(f"Logged feedback for user {user_id}: {interaction}")
            return True
            
        except Exception as e:
            print(f"Error logging interaction: {e}")
            return False

    def should_change_playlist(self, current_emotion, target_mood):
        
        # determine if playlist should be changed based on emotion
        suggested_mood = self.emotion_to_mood.get(current_emotion)
        return suggested_mood is not None and suggested_mood != target_mood