import cv2
import numpy as np

def detect_face(image):
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces

def extract_skin(image, face):
    (x, y, w, h) = face
    face_img = image[y:y+h, x:x+w]
    hsv_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv_img, lower_skin, upper_skin)
    skin = cv2.bitwise_and(face_img, face_img, mask=mask)
    return skin

def analyze_undertone(skin):
    # Convert the skin region to the LAB color space
    # Convert the skin region to a different color space
    # For example, you can try converting to the RGB color space
    rgb_skin = cv2.cvtColor(skin, cv2.COLOR_BGR2RGB)
    r, g, b = cv2.split(rgb_skin)
    
    # Compute the average color values
    avg_r = np.mean(r)
    avg_g = np.mean(g)
    avg_b = np.mean(b)
    
    # Determine the undertone based on average LAB values
    if avg_b > avg_r and avg_b > avg_g:
        return "Cool Undertone"
    else:
        return "Warm Undertone"

def main(image_path):
    image = cv2.imread(image_path)
    faces = detect_face(image)
    
    if len(faces) == 0:
        print("No face detected.")
        return
    
    for face in faces:
        skin = extract_skin(image, face)
        undertone = analyze_undertone(skin)
        print(f"Detected Undertone: {undertone}")

if __name__ == "__main__":
    image_path = 'face_3.png'  # Replace with your image path
    main(image_path)
