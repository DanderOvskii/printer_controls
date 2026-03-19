from enum import Enum
class PrinterState(Enum):
    DISCONNECTED = "DISCONNECTED"
    IDLE = "IDLE"
    PRINTING = "PRINTING"
    PAUSED = "PAUSED"
    ERROR = "ERROR"
