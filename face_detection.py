import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

image = cv2.imread('download.jpeg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

for (x, y, w, h) in faces:
    face_image = image[y:y+h, x:x+w]
    cv2.imwrite('face_crop.jpg', face_image)

cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()