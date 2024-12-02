# not used in project just used this for setting up Webcam and getting understadning 

# emotion_detector.py


import cv2
from fer import FER
import threading
import time 

class EmotionDetector:
    def __init__(self):
        self.camera = None
        self.frame_counter = 0
        self.last_emotion = "No emotion detected"
        self.lock = threading.Lock()
        self.detector = FER(mtcnn=True)

    def get_camera(self):
        # initialize or get existing camera instance
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise RuntimeError("Unable to access the camera.")
        return self.camera

    def process_frame(self):
        # process video frame and detect emotions
        camera = self.get_camera()
        success, frame = camera.read()

        if success:
            frame = cv2.resize(frame, (640, 480))
            
            if self.frame_counter % 10 == 0:
                try:
                    emotions = self.detector.detect_emotions(frame)
                    if emotions:
                        emotion_data = emotions[0]['emotions']
                        strongest_emotion = max(emotion_data.items(), key=lambda x: x[1])
                        
                        with self.lock:
                            self.last_emotion = strongest_emotion[0]

                        text = f"Emotion: {strongest_emotion[0]} ({strongest_emotion[1]:.2f})"
                        cv2.putText(frame, text, (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                except Exception as e:
                    print(f"Error detecting emotions: {e}")

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            return frame_bytes
        return None

    def generate_frames(self):
        # generate camera frames for streaming
        while True:
            frame_bytes = self.process_frame()
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.1)
