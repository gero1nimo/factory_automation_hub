from enum import Enum, auto


class MachineStatus(Enum):
    RUNNING = auto()
    IDLE = auto()
    ERROR = auto()
    MAINTENANCE = auto()
    EMERGENCY_STOP = auto()

    def __str__(self) -> str:
        return self.name
