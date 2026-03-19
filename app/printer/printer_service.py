import threading 
import queue
import time
from .serial_manager import SerialManager
from .models.printer_state import PrinterState

class PrinterService:
    def __init__(self):
        self.serial_manager = SerialManager.get_instance()
        self.command_queue = queue.Queue()
        self.active_command = None
        self.state = PrinterState.IDLE
        self.last_response = []
        self._lock = threading.Lock()
        self.worker_thread = threading.Thread(target=self._worker,daemon=True)
        self.worker_thread.start()

    def enqueue_command(self,command):
        self.command_queue.put(command)
        self.command_queue.join()
        print("command queueu")
        return{"status":"queued","command":command}

    def _worker(self):
        while True:
            try:
                command = self.command_queue.get()
                if command is None:
                    continue
                self.active_command = command
                with self._lock:
                    response = self.serial_manager.send(command)
                    self.last_response = response.get("response",[])
                    if command =="M112":
                        self.state = PrinterState.ERROR
                    elif command =="G28" or command.startswith("G1"):
                        self.state = PrinterState.PRINTING
                    elif command =="M105":
                        pass

                    for line in self.last_response:
                        if line.startswith("ok") and self.active_command:
                            self.active_command = None
                            self.state = PrinterState.IDLE
                    print("State",self.state)
                    self.command_queue.task_done()
            except Exception as e:
                self.state = PrinterState.ERROR
                print("worker error:", e)
    def get_state(self):
        return{
            "state":self.state.value,
            "last_response":self.last_response
        }
