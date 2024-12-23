from flask import Flask, Response, render_template, jsonify
import cv2
import os
import numpy as np
from datetime import datetime
from deepface import DeepFace  # Ensure you have the DeepFace library installed: pip install deepface
import time
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Folder paths
UPLOAD_FOLDER = "face"
SAVED_FACES_FOLDER = "face"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVED_FACES_FOLDER, exist_ok=True)

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Preload reference images
def load_reference_images(folder_path):
    reference_images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            reference_images.append(cv2.imread(img_path))
    return reference_images

reference_images = load_reference_images(SAVED_FACES_FOLDER)

camera = None  # Global camera object
verification_status = {"verified": False, "message": ""}  # Global verification state

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_stream', methods=['GET'])
def start_stream():
    global camera
    if not camera:
        camera = cv2.VideoCapture(0)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global camera
    if camera:
        camera.release()
        camera = None
    return "Stream stopped"

@app.route('/detect_face', methods=['POST'])
def detect_face_from_stream():
    global camera
    if not camera or not camera.isOpened():
        return jsonify({"status": "error", "message": "Camera is not active."})

    try:
        # Capture a single frame from the live feed
        success, frame = camera.read()
        if not success:
            return jsonify({"status": "error", "message": "Failed to capture frame."})

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            cropped_faces = []
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            for i, (x, y, w, h) in enumerate(faces):
                # Crop the detected face
                cropped_face = frame[y:y + h, x:x + w]
                cropped_filename = f"face_{i+1}_{timestamp}.jpg"
                cropped_filepath = os.path.join(UPLOAD_FOLDER, cropped_filename)

                # Save the cropped face
                cv2.imwrite(cropped_filepath, cropped_face)
                cropped_faces.append(cropped_filename)

            reference_images = load_reference_images(SAVED_FACES_FOLDER)
            return jsonify({
                "status": "success",
                "message": f"{len(faces)} face(s) detected and saved.",
                "faces": cropped_faces
            })
        else:
            return jsonify({"status": "success", "message": "No faces detected."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def generate_frames():
    global camera
    while camera and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            


net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000_fp16.caffemodel')


# Create a status dictionary for verification message
verification_status = {"message": "No face detected!"}

@app.route('/verify', methods=['POST'])
def verify_face():
    while True:
        try:
            # Extract the frame from the current camera feed
            if camera and camera.isOpened():
                success, frame = camera.read()
                if not success:
                    return jsonify({"error": "Failed to capture frame"}), 400
                # Get the frame dimensions
                height, width = frame.shape[:2]
                
                # Prepare the image for face detection
                blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)
                
                # Set the input to the network
                net.setInput(blob)
                
                # Run a forward pass to get face detections
                detections = net.forward()
                for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]

                    # If confidence is greater than the threshold (0.5)
                    if confidence > 0.5:
                        box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                        (startX, startY, endX, endY) = box.astype("int")

                        # Extract the detected face region
                        detected_face = frame[startY:endY, startX:endX]

                        # Compare the detected face with reference images
                        face_matched = False
                        for ref_img in reference_images:
                            result = DeepFace.verify(ref_img, detected_face, enforce_detection=False)
                            if result["verified"]:
                                face_matched = True
                                break
                        # Check if face matched
                        if not face_matched:
                            verification_status["message"] = "Unknown face detected! ALERT!"
                            return jsonify({"status": verification_status["message"]}), 200
                        
                        else:
                            verification_status["message"] = "Face matched!"
            # Sleep to avoid constant request overload
            time.sleep(0.5)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
            

if __name__ == "__main__":
    app.run(debug=True)
