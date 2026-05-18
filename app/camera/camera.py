
import cv2
import time
import atexit
import threading

class Camera:
    def __init__(self, current_camera =0):
        self.current_camera = current_camera

        self.video = None
        self.frame = None

        self.running = True

        self.lock = threading.Lock()
        self._open_camera(self.current_camera)

        self.thread = threading.Thread(target=self._video_stream)
        self.thread.daemon = True
        self.thread.start()

        atexit.register(self.turn_off)

    def _open_camera(self, index):
        if self.video is not None:
            self.video.release()

        self.video = cv2.VideoCapture(current_camera, cv2.CAP_ANY)

        self.video.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        time.sleep(0.5)
        if not self.video.isOpened():
            print(f"Failed to open camera {index}")
            self.video = None
            return False

        print(f"Camera {index} opened successfully")
        return True

    def _video_stream(self):
        while self.running:
            with self.lock:
                if self.video is None:
                    continue
                ret, frame = self.video.read()
                if not ret:
                    print("failed to get frame")
                    continue
                self.frame = frame
                time.sleep(0.01)

    def get_frame(self):
        with self.lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def switch_camera(self,index):
        print("cameraswich")
        with self.lock:
            success = self._open_camera(index)

            if success:
                self.current_camera = index
                self.frame = None
                print(f"Switched to camera {index}")
            else:
                print(f"Could not switch to camera {index}")


    def turn_off(self):
        self.running = False

        if self.thread.is_alive():
            self.thread.join(timeout=1)

        if self.video is not None:
            self.video.release()
        cv2.destroyAllWindows()


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
