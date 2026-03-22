
import cv2
import time
import atexit
import threading

current_camera = 0
video_lock = threading.Lock()
video = cv2.VideoCapture(current_camera, cv2.CAP_ANY)
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
atexit.register(lambda: video.release())
if not video.isOpened():
    print("Camera failed to open")

def video_stream():
    global video
    while True:
        with video_lock:
            ret, frame = video.read()
            if not ret:
                print("failed to get frame")
                break
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def switch_camera(index):
    print("cameraswich")
    global video, current_camera
    with video_lock:
        video.release()
        current_camera = index
        print("current cam", current_camera)
        video = cv2.VideoCapture(current_camera)

