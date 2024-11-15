from flask import Flask, render_template, Response
import cv2
from fer import FER
import time

# Create Flask app
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Initialize the emotion detector
detector = FER(mtcnn=True)

# Initialize global variables
camera = None
last_emotion = "No emotion detected"

def get_camera():
    """Get or create camera instance"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)  # 0 is usually the built-in webcam
    return camera

def process_frame():
    """Get a frame from the camera and process it"""
    camera = get_camera()
    success, frame = camera.read()
    
    if success:
        # Try to detect emotions in the frame
        try:
            # Only detect emotions every few frames to improve performance
            emotions = detector.detect_emotions(frame)
            if emotions:  # If a face was detected
                # Get the strongest emotion
                emotion_data = emotions[0]['emotions']
                strongest_emotion = max(emotion_data.items(), key=lambda x: x[1])[0]
                
                # Draw the emotion text on the frame
                cv2.putText(frame, 
                          f"Emotion: {strongest_emotion}", 
                          (10, 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 
                          1, 
                          (0, 255, 0), 
                          2)
                
                global last_emotion
                last_emotion = strongest_emotion
        
        except Exception as e:
            print(f"Error detecting emotions: {e}")
        
        # Convert the frame to jpg format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        return frame_bytes

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
    return {'emotion': last_emotion}


if __name__ == '__main__':
    app.run(debug=True)