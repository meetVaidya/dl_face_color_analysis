import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color

def rgb_to_lab(rgb):
    rgb_color = sRGBColor(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    lab_color = convert_color(rgb_color, LabColor)
    return [lab_color.lab_l, lab_color.lab_a, lab_color.lab_b]

# Generate synthetic data (same as before)
np.random.seed(42)
n_samples = 1000

warm_samples = np.column_stack([
    np.random.uniform(50, 80, n_samples),
    np.random.uniform(5, 25, n_samples),
    np.random.uniform(10, 30, n_samples)
])

cool_samples = np.column_stack([
    np.random.uniform(50, 80, n_samples),
    np.random.uniform(-5, 15, n_samples),
    np.random.uniform(10, 30, n_samples)
])

X = np.vstack([warm_samples, cool_samples])
y = np.concatenate([np.ones(n_samples), np.zeros(n_samples)])

# Split the data and train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")

def extract_skin_color(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image. Please check the file path.")
    
    # Convert to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert to HSV color space
    image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    
    # Define range for skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create a mask
    mask = cv2.inRange(image_hsv, lower_skin, upper_skin)
    
    # Apply the mask
    skin = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)
    
    # Calculate the average color of the skin area
    total_color = np.sum(skin, axis=(0, 1))
    num_skin_pixels = np.count_nonzero(mask)
    
    if num_skin_pixels == 0:
        raise ValueError("No skin detected in the image.")
    
    average_color = total_color / num_skin_pixels
    
    return average_color.astype(int)

def predict_undertone(rgb):
    lab = rgb_to_lab(rgb)
    prediction = clf.predict([lab])[0]
    return "Warm" if prediction == 1 else "Cool"

def analyze_image(image_path):
    try:
        skin_color = extract_skin_color(image_path)
        undertone = predict_undertone(skin_color)
        print(f"Detected skin color (RGB): {skin_color}")
        print(f"Predicted undertone: {undertone}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
image_path = "face_3.png"
analyze_image(image_path)