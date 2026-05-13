import cv2
import time
import atexit
import threading


class Camera:
    def __init__(self, current_camera=0):
        self.current_camera = current_camera
        self.lock = threading.Lock()
        self.running = True
        self.frame = None

        self.video = self._open_camera(current_camera)

        self.thread = threading.Thread(target=self._video_stream, daemon=True)
        self.thread.start()

        atexit.register(self.turn_off)

    def _open_camera(self, index):
        video = cv2.VideoCapture(index, cv2.CAP_ANY)

        if not video.isOpened():
            raise RuntimeError(f"Failed to open camera {index}")

        video.set(cv2.CAP_PROP_FOURCC,
                  cv2.VideoWriter_fourcc(*'MJPG'))
        video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        return video

    def _video_stream(self):
        while self.running:
            ret, frame = self.video.read()

            if ret:
                with self.lock:
                    self.frame = frame

            else:
                print("Failed to get frame")

            time.sleep(0.01)

    def get_frame(self):
        with self.lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def switch_camera(self, index):
        print(f"Switching to camera {index}")

        new_video = self._open_camera(index)

        with self.lock:
            old_video = self.video
            self.video = new_video
            self.current_camera = index

        old_video.release()

    def turn_off(self):
        self.running = False

        if self.thread.is_alive():
            self.thread.join(timeout=1)

        if self.video is not None:
            self.video.release()