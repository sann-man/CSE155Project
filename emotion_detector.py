#  imports 
# Launches Webcam and detects emotion

# because certain emotions are only detected with dramatic expressions my plan 
# is to only register expressions when they pass a certain threshold (excluing nuetral)


# webacme is launched once user selects all required inputs
    # required inputs - genre and mood

# 


import cv2
from fer import FER
import numpy as np
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import queue

class EmotionDetector:
    def __init__(self):
        # Initialize the emotion detector
        self.emotion_detector = FER(mtcnn=True)
        
        # Initialize the GUI
        self.root = tk.Tk()
        self.root.title("Emotion Detection")
        self.root.geometry("800x600")
        
        # create frames
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.grid(row=0, column=0, padx=10, pady=5)
        
        self.info_frame = ttk.Frame(self.root)
        self.info_frame.grid(row=0, column=1, padx=10, pady=5)
        
        # create labels
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.grid(row=0, column=0)
        
        # emotion labels and progress bars
        self.emotion_bars = {}
        self.emotion_labels = {}
        self.setup_emotion_displays()
        
        # control buttons
        self.start_button = ttk.Button(self.info_frame, text="Start Detection", command=self.start_detection)
        self.start_button.grid(row=8, column=0, pady=5)
        
        self.stop_button = ttk.Button(self.info_frame, text="Stop Detection", command=self.stop_detection, state='disabled')
        self.stop_button.grid(row=9, column=0, pady=5)
        
        # status label
        self.status_label = ttk.Label(self.info_frame, text="Status: Ready")
        self.status_label.grid(row=10, column=0, pady=5)
        
        # initialize variables
        self.running = False
        self.camera = None
        self.detection_thread = None
        self.emotion_queue = queue.Queue()
        
    def setup_emotion_displays(self):
        """setup progress bars and labels for each emotion"""
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
        for idx, emotion in enumerate(emotions):
            # create label
            label = ttk.Label(self.info_frame, text=f"{emotion.capitalize()}:")
            label.grid(row=idx, column=0, pady=2)
            
            # create progress bar
            progress = ttk.Progressbar(self.info_frame, length=200, mode='determinate')
            progress.grid(row=idx, column=1, pady=2)
            
            # sstore references
            self.emotion_bars[emotion] = progress
            self.emotion_labels[emotion] = label
    
    def start_detection(self):
        """start the emotion detection process"""
        self.running = True
        self.camera = cv2.VideoCapture(0)
        
        # Update button states
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
        
        # Start detection thread
        self.detection_thread = threading.Thread(target=self.detection_loop)
        self.detection_thread.daemon = True
        self.detection_thread.start()
        
        # Start update loop
        self.update_frame()
        
    def stop_detection(self):
        """stop the emotion detection process"""
        self.running = False
        if self.camera is not None:
            self.camera.release()
        
        # Update button states
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'
        self.status_label['text'] = "Status: Stopped"
        
    def detection_loop(self):
        """main detection loop running in separate thread"""
        last_detection_time = 0
        detection_interval = 0.5  # Detect every 0.5 seconds
        
        while self.running:
            current_time = time.time()
            
            # Only perform detection every detection_interval seconds
            if current_time - last_detection_time >= detection_interval:
                ret, frame = self.camera.read()
                if ret:
                    try:
                        # Perform emotion detection
                        emotions = self.emotion_detector.detect_emotions(frame)
                        if emotions:  # If face detected
                            # Get emotions from the first face detected
                            emotion_values = emotions[0]['emotions']
                            # Convert values to percentages
                            emotion_percentages = {k: v * 100 for k, v in emotion_values.items()}
                            self.emotion_queue.put(emotion_percentages)
                        else:
                            self.emotion_queue.put(None)
                            
                        last_detection_time = current_time
                        
                    except Exception as e:
                        print(f"Detection error: {e}")
                        self.emotion_queue.put(None)
    
    def update_frame(self):
        """update the GUI with new frame and emotion data"""
        if self.running and self.camera is not None:
            # Get video frame
            ret, frame = self.camera.read()
            if ret:
                # Convert frame for display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)  # Mirror image
                
                # Resize frame
                height, width = frame.shape[:2]
                max_height = 400
                if height > max_height:
                    ratio = max_height / height
                    new_width = int(width * ratio)
                    frame = cv2.resize(frame, (new_width, max_height))
                
                # Convert to PhotoImage
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=image)
                self.video_label.configure(image=photo)
                self.video_label.image = photo
                
                # Update emotion data if available
                try:
                    while not self.emotion_queue.empty():
                        emotions = self.emotion_queue.get_nowait()
                        if emotions is not None:
                            self.update_emotion_displays(emotions)
                            self.status_label['text'] = "Status: Detecting emotions"
                        else:
                            self.status_label['text'] = "Status: No face detected"
                except queue.Empty:
                    pass
                
            # Schedule next update
            self.root.after(10, self.update_frame)
    
    def update_emotion_displays(self, emotions):
        """pdate the progress bars with new emotion values"""
        for emotion, value in emotions.items():
            if emotion in self.emotion_bars:
                self.emotion_bars[emotion]['value'] = value
                self.emotion_labels[emotion]['text'] = f"{emotion.capitalize()}: {value:.1f}%"
    
    def run(self):
        """start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    detector = EmotionDetector()
    detector.run()