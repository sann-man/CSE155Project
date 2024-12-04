# not used in project just used this for setting up Webcam and getting understadning 

# emotion_detector.py -> app.py 


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

    # open camera 
    def get_camera(self):
        if self.camera is None:
            for index in range(4):  # try first 4 camera indexes
                self.camera = cv2.VideoCapture(index)
                if self.camera.isOpened():
                    print(f"Successfully connected to camera {index}")
                    return self.camera
                self.camera.release()
                
            raise RuntimeError("No accessible camera found. Check camera connection and permissions")
        return self.camera


    def process_frame(self):
        # process video frame and detect emotions
        # get camera 
        camera = self.get_camera()
        success, frame = camera.read()


        if success:
            frame = cv2.resize(frame, (640, 480))
            
            # only process everyth 10th frame (helps with cpu load )
            if self.frame_counter % 10 == 0:
                try:
                    emotions = self.detector.detect_emotions(frame)
                    if emotions:
                        emotion_data = emotions[0]['emotions']
                        # finds the dominant emotion in dictionary (turns to tuples and measures MAX emotion probability )
                        strongest_emotion = max(emotion_data.items(), key=lambda x: x[1])
                        
                        # added becasue some times was getting two emotions at the same time 
                        # causing an error 
                        with self.lock:
                            self.last_emotion = strongest_emotion[0]

                        # add text to frame 
                        text = f"Emotion: {strongest_emotion[0]} ({strongest_emotion[1]:.2f})"
                        cv2.putText(frame, text, (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                except Exception as e:
                    print(f"Error detecting emotions: {e}")

                # return picture as bytes 
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
            time.sleep(0.1) #also helps with cpu usage 
