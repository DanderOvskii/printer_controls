import cv2
import time
import atexit
current_camera = 0
video = cv2.VideoCapture(current_camera, cv2.CAP_ANY)
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
atexit.register(lambda: video.release())
if not video.isOpened():
    print("Camera failed to open")
def video_stream():
    while(True):
        ret, frame = video.read()
        if not ret:
            print("failed to get frame")
            break
        else:
            ret,buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def switch_camera(index):
    global video, current_camera
    video.release()
    current_camera = index
    print("current cam",current_camera)
    video = cv2.VideoCapture(current_camera)
