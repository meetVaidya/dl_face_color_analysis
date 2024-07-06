import cv2
import numpy as np

def detect_face(image):
    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return faces

def extract_skin(image, face):
    (x, y, w, h) = face
    face_img = image[y:y+h, x:x+w]
    hsv_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv_img, lower_skin, upper_skin)
    skin = cv2.bitwise_and(face_img, face_img, mask=mask)
    
    # Show the image of the extracted skin
    # cv2.imshow('Skin', skin)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return skin

def analyze_undertone(skin):
    # Convert the skin region to the LAB color space
    lab_skin = cv2.cvtColor(skin, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_skin)
    
    # Compute the average color values
    avg_a = np.mean(a)
    avg_b = np.mean(b)
    
    # Determine the undertone based on average LAB values
    if avg_a > avg_b:
        undertone = "Warm Undertone"
    else:
        undertone = "Cool Undertone"
    
    # print("Analyzed Undertone:", undertone)
    return undertone

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
    image_path = 'face_2.png'  # Replace with your image path
    main(image_path)
