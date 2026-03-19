import cv2

cap = cv2.VideoCapture(0, cv2.CAP_ANY)
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

ret, frame = cap.read()
if ret:
    cv2.imwrite("test.jpg", frame)
    print("Frame captured")
else:
    print("Failed to capture frame")
cap.release()
