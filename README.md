
🚀 Overview

Intelli Cam is an advanced AI application designed to enhance security through real-time detection of unknown persons in video streams. Utilizing cutting-edge technologies such as OpenCV, Flask, and DeepFace, Intelli Cam provides a seamless experience for live video monitoring and facial recognition.

🌟 Features

Live Video Streaming: Initiate and control video streams directly from an intuitive web interface.

Face Detection: Detect and save cropped face images from video streams.

Facial Verification: Match detected faces against a stored database and raise alerts for unidentified individuals.

Web-Based Interface: User-friendly and responsive interface for hassle-free operation.

🛠️ Installation

Prerequisites

Ensure you have the following installed:

Python (Version 3.7 or higher)

Libraries:

Flask

OpenCV (cv2)

DeepFace

NumPy

Setup Steps

Clone the Repository:

git clone https://github.com/username/intelli-cam.git
cd intelli-cam

Install Dependencies:

pip install -r requirements.txt

Prepare Reference Images:
Add images of known individuals to the face/ directory for recognition.

Run the Application:

python app.py

Access the Application:
Open your browser and navigate to http://127.0.0.1:5000.

📂 Project Structure

app.py: Backend logic and Flask routes.

index.html: Frontend HTML for the web interface.

script.js: JavaScript to handle user actions and backend communication.

face/: Directory for storing known face images.

detected_faces/: Directory for saving detected face images.

requirements.txt: List of required Python libraries.

🎯 How to Use

Start the Application:
Run python app.py in the terminal.

Open the Interface:
Navigate to http://127.0.0.1:5000 in your web browser.

Interact with Features:

Start/stop live video streams.

Detect and save faces.

Verify faces against the saved database.

Receive alerts for unknown individuals.

🚧 Future Enhancements

Cloud Integration: Enable storing and retrieving face datasets from cloud platforms.

IP Camera Support: Expand compatibility to include IP-based cameras.

Real-Time Notifications: Add email and SMS alert functionality.

Enhanced UI: Introduce a modern and responsive design.

📜 License

This project is licensed under the MIT License. For more details, refer to the LICENSE file.

🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

📧 Contact

For inquiries or support, reach out at your-email@example.com.
