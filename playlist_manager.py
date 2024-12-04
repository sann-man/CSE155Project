
import random
import time 
# gets data from data_config.py

def create_playlist(spotify, activity, genre, mood, current_playlist_uri=None):
   # try to find a good playlist based on user input
    # without the pre defined playlit libnrary 
   try:
       playlists = []
       playlist_dict = get_playlist_dict()
       
       print(f"\nFinding playlist for: {activity} - {genre} - {mood}")
       print(f"Excluding current playlist: {current_playlist_uri}")
       
       # first check if we got a playlist already made for this combo
       playlist_key = (activity, genre, mood)
       predefined_uri = playlist_dict.get(playlist_key)
       if predefined_uri and predefined_uri != current_playlist_uri:
           try:
               
               playlist_info = spotify.playlist(predefined_uri)
               playlists.append((playlist_info['name'], predefined_uri))
               print(f"Found predefined playlist: {playlist_info['name']}")

           except Exception as e:
               print(f"couldnt find a playlist that matches: {e}")
       
       # search spotify with these terms if we need to more playlists 
    #    add other 2 cases becasue it enhances search capabilities 
       search_terms = [
           f"{activity} {genre} {mood}",
           f"{activity} {genre}",
           f"{genre} {mood}"
       ]
       # add some extra search terms for workout playlists
    #    if activity == 'exercise':
    #        search_terms.extend([
    #            f"workout {genre}",
    #            f"gym {genre} {mood}"
    #        ])
    #        if genre == 'hiphop':
    #            search_terms.extend([
    #                "workout rap",
    #                "gym hip hop"
    #            ])
       
       # look for more playlists on spotify
       for search_term in search_terms:
           try:
            #    ApI call 
               results = spotify.search(
                   q=search_term + " playlist",
                   type='playlist',
                   limit=5
               )
               
               # if we found playlists add them to our list
               if results and 'playlists' in results and results['playlists']['items']:
                   for item in results['playlists']['items']:
                       playlist_uri = item['uri']

                       # skip the playlist were already playing
                       if playlist_uri == current_playlist_uri:
                           continue
                       # gets rid of duplicate playlist URIS 
                       if not any(uri == playlist_uri for _, uri in playlists):
                           playlists.append((item['name'], playlist_uri))
                           print(f"Found playlist: {item['name']}")
                           
               # stop looking if we got enough playlists
            #    had to add this for some reason wasnt stoping at 5 
               if len(playlists) >= 5:
                   break
                   
           except Exception as e:
               print(f"searching for {search_term} failed: {e}")
               continue

       # pick a random playlist from what we found
       if playlists:
           print(f"Found {len(playlists)} different playlists")
           selected_playlist = random.choice(playlists)
           print(f"picked this one: {selected_playlist[0]}")
           return [selected_playlist]
       else:
           print("couldnt find any other playlists")
           return None

   except Exception as e:
       print(f"something broke in create_playlist: {e}")
       return None

def process_emotions(emotion_history, current_emotion, target_mood):
   
   # figure out if we should change the playlist based on user emotions
#    used these mainly for debuging 
   print("\n=== checking emotions ===")
   print(f"your feeling: {current_emotion}")
   print(f"trying to feel: {target_mood}")
   
   # need at least 5 emotion readings before deciding
   if len(emotion_history) < 5:
       print("need more emotion data first")
       return False, None
       
   # map emotions to energy levels
#    energy levels make it easier to decide if new playlist should be used
# had trouble without it 
   emotion_energy_levels = {
       'happy': 'energetic',
       'sad': 'calm',
       'angry': 'energetic', 
       'fearful': 'energetic',
       'fear': 'energetic',
       'disgusted': 'energetic',
       'surprised': 'energetic',
       'surprise': 'energetic', 
       'neutral': 'focus',
       'No emotion detected': None
   }
   
   # group moods by energy level
   high_energy_moods = {'energetic', 'happy'}
   low_energy_moods = {'calm', 'focus'}
   
   # last 5 emotions
   recent_emotions = list(emotion_history)[-5:]
   emotion_counts = {}
   for emotion in recent_emotions:
       emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

   print(f"emotions in last 5 checks: {recent_emotions}")
   print(f"how many times each emotion showed up: {emotion_counts}")
   
   # figure out main / dominant emotion
#    lmada is just another way to creeate a function 
   dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
   print(f"main emotion rn: {dominant_emotion}")
   
   # get energy level of main emotion
   current_energy = emotion_energy_levels.get(dominant_emotion)
   print(f"energy level rn: {current_energy}")
   
   should_change = False
   suggested_mood = None
   
   # decide if we should change playlist
   if current_energy and emotion_counts[dominant_emotion] >= 2:
    
        # energy level differentiation 
       # if trying to be energetic but feeling calm
       if target_mood in high_energy_moods and current_energy == 'calm':
           suggested_mood = 'energetic'
           should_change = True
       # if trying to be calm but feeling energetic
       elif target_mood in low_energy_moods and current_energy == 'energetic':
           suggested_mood = target_mood
           should_change = True
   
   print(f"should we change? {should_change}")
   print(f"suggested new mood: {suggested_mood}")
   
   return should_change, suggested_mood

# music reccomendations 
class MusicRecommendationEngine:
   def __init__(self):
       
       # keep track of what worked before from user 
       self.training_data = []
       self.interaction_history = []

   def prepare_training_data(self, data):
       
       # load up initial training data
       self.training_data = data

   def log_interaction(self, user_id, activity, genre, mood, emotion, playlist_uri, feedback_score):
       # remember how user felt about this playlist
       interaction = {
           'user_id': user_id,
           'activity': activity,
           'genre': genre,
           'mood': mood,
           'emotion': emotion,
           'playlist_uri': playlist_uri,
           'feedback_score': feedback_score, # did they like it or not
           'timestamp': time.time()
       }
       self.interaction_history.append(interaction)
       print(f"saved ur feedback: {interaction}")

# these are playlists we made already
def get_playlist_dict():
   return {
        ('study', 'classical', 'happy'): 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE',
        ('work', 'rock', 'focus'): 'spotify:playlist:37i9dQZF1DX9qNs32fujYe',
        ('exercise', 'pop', 'focus'): 'spotify:playlist:37i9dQZF1DX9qNs32fujYe',
       # we can add more later
    #    have in data_config 
   }

def get_training_data():
   # starter data to help recommendations
   return [
       {
           'user_id': 'default',
           'activity': 'exercise',
           'genre': 'pop',
           'mood': 'energetic',
           'emotion': 'happy',
           'playlist_uri': 'spotify:playlist:example1',
           'feedback_score': 1
       },
       # can add more examples later
   ]