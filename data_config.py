# data_config.py


import pandas as pd

def get_training_data():
    """Returns the training data for the recommendation engine"""
    initial_training_data = pd.DataFrame({
        'activity': [
            # Study combinations
            'study', 'study', 'study', 'study',
            'study', 'study', 'study', 'study',
            'study', 'study', 'study', 'study',
            'study', 'study', 'study', 'study',
            'study', 'study', 'study', 'study',
            'study', 'study', 'study', 'study',
            # Work combinations
            'work', 'work', 'work', 'work',
            'work', 'work', 'work', 'work',
            'work', 'work', 'work', 'work',
            'work', 'work', 'work', 'work',
            'work', 'work', 'work', 'work',
            'work', 'work', 'work', 'work',
            # Exercise combinations
            'exercise', 'exercise', 'exercise', 'exercise',
            'exercise', 'exercise', 'exercise', 'exercise',
            'exercise', 'exercise', 'exercise', 'exercise',
            'exercise', 'exercise', 'exercise', 'exercise',
            'exercise', 'exercise', 'exercise', 'exercise',
            'exercise', 'exercise', 'exercise', 'exercise',
            # Relax combinations
            'relax', 'relax', 'relax', 'relax',
            'relax', 'relax', 'relax', 'relax',
            'relax', 'relax', 'relax', 'relax',
            'relax', 'relax', 'relax', 'relax',
            'relax', 'relax', 'relax', 'relax',
            'relax', 'relax', 'relax', 'relax'
        ],
        'genre': [
            # Study genres
            'classical', 'classical', 'classical', 'classical',
            'pop', 'pop', 'pop', 'pop',
            'rock', 'rock', 'rock', 'rock',
            'ambient', 'ambient', 'ambient', 'ambient',
            'electronic', 'electronic', 'electronic', 'electronic',
            'hiphop', 'hiphop', 'hiphop', 'hiphop',

            # Work genres (repeated pattern)
            'classical', 'classical', 'classical', 'classical',
            'pop', 'pop', 'pop', 'pop',
            'rock', 'rock', 'rock', 'rock',
            'ambient', 'ambient', 'ambient', 'ambient',
            'electronic', 'electronic', 'electronic', 'electronic',
            'hiphop', 'hiphop', 'hiphop', 'hiphop',

            # Exercise genres (repeated pattern)
            'classical', 'classical', 'classical', 'classical',
            'pop', 'pop', 'pop', 'pop',
            'rock', 'rock', 'rock', 'rock',
            'ambient', 'ambient', 'ambient', 'ambient',
            'electronic', 'electronic', 'electronic', 'electronic',
            'hiphop', 'hiphop', 'hiphop', 'hiphop',
            
            # Relax genres (repeated pattern)
            'classical', 'classical', 'classical', 'classical',
            'pop', 'pop', 'pop', 'pop',
            'rock', 'rock', 'rock', 'rock',
            'ambient', 'ambient', 'ambient', 'ambient',
            'electronic', 'electronic', 'electronic', 'electronic',
            'hiphop', 'hiphop', 'hiphop', 'hiphop'
        ],
        'mood': [
            # Repeated pattern for all activities
            'focus', 'happy', 'energetic', 'calm'
        ] * 24,  # Repeated for each activity-genre combination
        'emotion': [
            # Matching emotions for all combinations
            'neutral', 'happy', 'energetic', 'calm'
        ] * 24,  # Repeated for each activity-genre combination
        'playlist_uri': [
            # All playlist URIs from your dictionary
            # Study playlist URIs

            'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6', 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6', 'spotify:playlist:37i9dQZF1DX1BzILRveYHb', 'spotify:playlist:37i9dQZF1DX1FJijPQ3V4S', 'spotify:playlist:37i9dQZF1DX7gIoKXt0gmx',
            'spotify:playlist:37i9dQZF1DX9qNs32fujYe', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DWXNFSTtym834', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY', 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0', 'spotify:playlist:37i9dQZF1DXd9H78TKNPf0', 'spotify:playlist:37i9dQZF1DX4H7FFUM2osB',
            'spotify:playlist:37i9dQZF1DX3GJ1Bd5dVQL', 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq', 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX3rxVfibe1L0', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP', 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp',
            # Work playlist URIs (same pattern as study)

            'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6', 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6', 'spotify:playlist:37i9dQZF1DX1BzILRveYHb', 'spotify:playlist:37i9dQZF1DX1FJijPQ3V4S', 'spotify:playlist:37i9dQZF1DX7gIoKXt0gmx',
            'spotify:playlist:37i9dQZF1DX9qNs32fujYe', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DWXNFSTtym834', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY', 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0', 'spotify:playlist:37i9dQZF1DXd9H78TKNPf0', 'spotify:playlist:37i9dQZF1DX4H7FFUM2osB',
            'spotify:playlist:37i9dQZF1DX3GJ1Bd5dVQL', 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq', 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX3rxVfibe1L0', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP', 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp',
            # Exercise playlist URIs

            'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6', 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX9qNs32fujYe', 'spotify:playlist:37i9dQZF1DX1BzILRveYHb', 'spotify:playlist:37i9dQZF1DX1FJijPQ3V4S', 'spotify:playlist:37i9dQZF1DX7gIoKXt0gmx',
            'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX1s9knjP51Oa', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY', 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0', 'spotify:playlist:37i9dQZF1DXd9H78TKNPf0', 'spotify:playlist:37i9dQZF1DX4H7FFUM2osB',
            'spotify:playlist:37i9dQZF1DX3GJ1Bd5dVQL', 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq', 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE', 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp',
            # Relax playlist URIs

            'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6', 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6', 'spotify:playlist:37i9dQZF1DX1BzILRveYHb', 'spotify:playlist:37i9dQZF1DX1FJijPQ3V4S', 'spotify:playlist:37i9dQZF1DX7gIoKXt0gmx',
            'spotify:playlist:37i9dQZF1DX9qNs32fujYe', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DWXNFSTtym834', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY', 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0', 'spotify:playlist:37i9dQZF1DXd9H78TKNPf0', 'spotify:playlist:37i9dQZF1DX4H7FFUM2osB',
            'spotify:playlist:37i9dQZF1DX3GJ1Bd5dVQL', 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq', 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE', 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
            'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP', 'spotify:playlist:37i9dQZF1DWXRqgorJj26U', 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE', 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp'
        ]
    })
    return initial_training_data

def get_playlist_dict():
    """Returns the playlist dictionary"""
    return {
        # Study
        ('study', 'classical', 'focus'): 'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6',
        ('study', 'classical', 'happy'): 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE',
        ('study', 'classical', 'energetic'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('study', 'classical', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('study', 'pop', 'focus'): 'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6',
        ('study', 'pop', 'happy'): 'spotify:playlist:37i9dQZF1DX1BzILRveYHb',
        ('study', 'pop', 'energetic'): 'spotify:playlist:37i9dQZF1DX1FJijPQ3V4S',
        ('study', 'pop', 'calm'): 'spotify:playlist:37i9dQZF1DX7gIoKXt0gmx',
        ('study', 'rock', 'focus'): 'spotify:playlist:37i9dQZF1DX9qNs32fujYe',
        ('study', 'rock', 'happy'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('study', 'rock', 'energetic'): 'spotify:playlist:37i9dQZF1DWXNFSTtym834',
        ('study', 'rock', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('study', 'ambient', 'focus'): 'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY',
        ('study', 'ambient', 'happy'): 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
        ('study', 'ambient', 'energetic'): 'spotify:playlist:37i9dQZF1DXd9H78TKNPf0',
        ('study', 'ambient', 'calm'): 'spotify:playlist:37i9dQZF1DX4H7FFUM2osB',
        ('study', 'electronic', 'focus'): 'spotify:playlist:37i9dQZF1DX3GJ1Bd5dVQL',
        ('study', 'electronic', 'happy'): 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq',
        ('study', 'electronic', 'energetic'): 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE',
        ('study', 'electronic', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('study', 'hiphop', 'focus'): 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
        ('study', 'hiphop', 'happy'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('study', 'hiphop', 'energetic'): 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP',
        ('study', 'hiphop', 'calm'): 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp',

        # Work
        ('work', 'classical', 'focus'): 'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6',
        ('work', 'classical', 'happy'): 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE',
        ('work', 'classical', 'energetic'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('work', 'classical', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('work', 'pop', 'focus'): 'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6',
        ('work', 'pop', 'happy'): 'spotify:playlist:37i9dQZF1DX1BzILRveYHb',
        ('work', 'pop', 'energetic'): 'spotify:playlist:37i9dQZF1DX1FJijPQ3V4S',
        ('work', 'pop', 'calm'): 'spotify:playlist:37i9dQZF1DX7gIoKXt0gmx',
        ('work', 'rock', 'focus'): 'spotify:playlist:37i9dQZF1DX9qNs32fujYe',
        ('work', 'rock', 'happy'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('work', 'rock', 'energetic'): 'spotify:playlist:37i9dQZF1DWXNFSTtym834',
        ('work', 'rock', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('work', 'ambient', 'focus'): 'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY',
        ('work', 'ambient', 'happy'): 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
        ('work', 'ambient', 'energetic'): 'spotify:playlist:37i9dQZF1DXd9H78TKNPf0',
        ('work', 'ambient', 'calm'): 'spotify:playlist:37i9dQZF1DX4H7FFUM2osB',
        ('work', 'electronic', 'focus'): 'spotify:playlist:37i9dQZF1DX3GJ1Bd5dVQL',
        ('work', 'electronic', 'happy'): 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq',
        ('work', 'electronic', 'energetic'): 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE',
        ('work', 'electronic', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('work', 'hiphop', 'focus'): 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
        ('work', 'hiphop', 'happy'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('work', 'hiphop', 'energetic'): 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP',
        ('work', 'hiphop', 'calm'): 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp',

        # Exercise
        ('exercise', 'classical', 'focus'): 'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6',
        ('exercise', 'classical', 'happy'): 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE',
        ('exercise', 'classical', 'energetic'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('exercise', 'classical', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('exercise', 'pop', 'focus'): 'spotify:playlist:37i9dQZF1DX9qNs32fujYe',
        ('exercise', 'pop', 'happy'): 'spotify:playlist:37i9dQZF1DX1BzILRveYHb',
        ('exercise', 'pop', 'energetic'): 'spotify:playlist:37i9dQZF1DX1FJijPQ3V4S',
        ('exercise', 'pop', 'calm'): 'spotify:playlist:37i9dQZF1DX7gIoKXt0gmx',
        ('exercise', 'rock', 'focus'): 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP',
        ('exercise', 'rock', 'happy'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('exercise', 'rock', 'energetic'): 'spotify:playlist:37i9dQZF1DX1s9knjP51Oa',
        ('exercise', 'rock', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('exercise', 'ambient', 'focus'): 'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY',
        ('exercise', 'ambient', 'happy'): 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
        ('exercise', 'ambient', 'energetic'): 'spotify:playlist:37i9dQZF1DXd9H78TKNPf0',
        ('exercise', 'ambient', 'calm'): 'spotify:playlist:37i9dQZF1DX4H7FFUM2osB',
        ('exercise', 'electronic', 'focus'): 'spotify:playlist:37i9dQZF1DX3GJ1Bd5dVQL',
        ('exercise', 'electronic', 'happy'): 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq',
        ('exercise', 'electronic', 'energetic'): 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE',
        ('exercise', 'electronic', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('exercise', 'hiphop', 'focus'): 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP',
        ('exercise', 'hiphop', 'happy'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('exercise', 'hiphop', 'energetic'): 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE',
        ('exercise', 'hiphop', 'calm'): 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp',

    # Relax
        ('relax', 'classical', 'focus'): 'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6',
        ('relax', 'classical', 'happy'): 'spotify:playlist:37i9dQZF1DWUoZLzF1EkPE',
        ('relax', 'classical', 'energetic'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('relax', 'classical', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('relax', 'pop', 'focus'): 'spotify:playlist:37i9dQZF1DX8NTLI2TtZa6',
        ('relax', 'pop', 'happy'): 'spotify:playlist:37i9dQZF1DX1BzILRveYHb',
        ('relax', 'pop', 'energetic'): 'spotify:playlist:37i9dQZF1DX1FJijPQ3V4S',
        ('relax', 'pop', 'calm'): 'spotify:playlist:37i9dQZF1DX7gIoKXt0gmx',
        ('relax', 'rock', 'focus'): 'spotify:playlist:37i9dQZF1DX9qNs32fujYe',
        ('relax', 'rock', 'happy'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('relax', 'rock', 'energetic'): 'spotify:playlist:37i9dQZF1DWXNFSTtym834',
        ('relax', 'rock', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('relax', 'ambient', 'focus'): 'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY',
        ('relax', 'ambient', 'happy'): 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
        ('relax', 'ambient', 'energetic'): 'spotify:playlist:37i9dQZF1DXd9H78TKNPf0',
        ('relax', 'ambient', 'calm'): 'spotify:playlist:37i9dQZF1DX4H7FFUM2osB',
        ('relax', 'electronic', 'focus'): 'spotify:playlist:37i9dQZF1DX3GJ1Bd5dVQL',
        ('relax', 'electronic', 'happy'): 'spotify:playlist:37i9dQZF1DX6GwdWRQMQpq',
        ('relax', 'electronic', 'energetic'): 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE',
        ('relax', 'electronic', 'calm'): 'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
        ('relax', 'hiphop', 'focus'): 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP',
        ('relax', 'hiphop', 'happy'): 'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
        ('relax', 'hiphop', 'energetic'): 'spotify:playlist:37i9dQZF1DX0HRj9P7NxeE',
        ('relax', 'hiphop', 'calm'): 'spotify:playlist:37i9dQZF1DWZd79rJ6a7lp',

    }