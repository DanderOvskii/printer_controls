
import cv2
import time
import atexit
import threading

class Camera:
    def __init__(self, current_camera =1):
        self.current_camera = current_camera
        self.video = cv2.VideoCapture(current_camera, cv2.CAP_ANY)
        self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not self.video.isOpened():
            print("camera failed to open")

        self.frame = None
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._video_stream)
        self.thread.deamon = True
        self.thread.start()
        atexit.register(self.turn_off)

    def _video_stream(self):
        while True:
            with self.lock:
                if self.video is None:
                    continue
                ret, frame = self.video.read()
                if not ret:
                    print("failed to get frame")
                    continue
                self.frame = frame

    def get_frame(self):
        with self.lock:
            return self.frame

    def switch_camera(self,index):
        print("cameraswich")
        with self.lock:
            if self.video is not None:
                self.turn_off
            self.current_camera = index
            self.video = cv2.VideoCapture(self.current_camera,cv2.CAP_ANY)


    def turn_off(self):
        with self.lock:
            if self.video is not None:
                self.video.release()

camera = Camera()
def video_stream():
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue

        ret, buffer = cv2.imencode('.jpeg', frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-type: image/jpeg\r\n\r\n' +
               frame_bytes +
               b'\r\n')
