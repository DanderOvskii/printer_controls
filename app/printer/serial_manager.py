import serial
import time
import threading

PORT = "/dev/ttyUSB0"
BAUDRATE = 115200

class SerialManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.serial = None
        self._connect()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = SerialManager()
        return cls._instance

    def _connect(self):
        try:
            self.serial = serial.Serial(PORT,BAUDRATE, timeout=2)
            time.sleep(2)
            self.serial.reset_input_buffer()
        except Exception as e:
            print("serial connection error",e)
            self.serial = None

    def send(self,command):
        if not self.serial or not self.serial.is_open:
            return{"error":"printer not connected"}
        self.serial.write((command + "\n").encode())
        time.sleep(0.1)
        responses = []
        while self.serial.in_waiting:
            responses.append(self.serial.readline().decode(errors="ignore").strip())
        return {"response": responses}

