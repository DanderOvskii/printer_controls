import cv2
import time
video = cv2.VideoCapture(0, cv2.CAP_ANY)
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def video_stream():
    while(True):
        time.sleep(0.05)
        ret, frame = video.read()
        if not ret:
            print("failed to get frame")
            break
        else:
            ret,buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')
