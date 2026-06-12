from __future__ import annotations

from typing import List

from src.interfaces.network_machine import INetworkMachine
from src.interfaces.machine_status import MachineStatus


class RoboticArm(INetworkMachine):

    def __init__(self, armId: str) -> None:
        self.armId = armId
        self.jointAngles: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.isLocked = False
        self.status = MachineStatus.IDLE

    def start(self) -> None:
        self.isLocked = False
        self.status = MachineStatus.RUNNING

    def stop(self) -> None:
        self.status = MachineStatus.IDLE

    def getStatus(self) -> MachineStatus:
        return self.status

    def getId(self) -> str:
        return self.armId

    def getType(self) -> str:
        return "robotic_arm"

    def lockArm(self) -> None:
        self.isLocked = True
        self.status = MachineStatus.EMERGENCY_STOP

    def unlockArm(self) -> None:
        self.isLocked = False
        self.status = MachineStatus.IDLE

    def moveToPosition(self, angles: List[float]) -> None:
        if self.isLocked or self.status is not MachineStatus.RUNNING:
            raise RuntimeError(f"{self.armId} cannot move (locked or not running).")
        self.jointAngles = list(angles)


class SmartConveyor(INetworkMachine):

    def __init__(self, conveyorId: str, speed: float = 0.5) -> None:
        self.conveyorId = conveyorId
        self.speed = speed
        self.isRunning = False
        self.status = MachineStatus.IDLE

    def start(self) -> None:
        self.isRunning = True
        self.status = MachineStatus.RUNNING

    def stop(self) -> None:
        self.isRunning = False
        self.status = MachineStatus.IDLE

    def getStatus(self) -> MachineStatus:
        return self.status

    def getId(self) -> str:
        return self.conveyorId

    def getType(self) -> str:
        return "smart_conveyor"

    def halt(self) -> None:
        self.isRunning = False
        self.status = MachineStatus.EMERGENCY_STOP

    def setSpeed(self, speed: float) -> None:
        self.speed = speed


class LaserCutter(INetworkMachine):

    def __init__(self, cutterId: str, powerLevel: float = 200.0) -> None:
        self.cutterId = cutterId
        self.powerLevel = powerLevel
        self.isActive = False
        self.status = MachineStatus.IDLE

    def start(self) -> None:
        self.isActive = True
        self.status = MachineStatus.RUNNING

    def stop(self) -> None:
        self.isActive = False
        self.status = MachineStatus.IDLE

    def getStatus(self) -> MachineStatus:
        return self.status

    def getId(self) -> str:
        return self.cutterId

    def getType(self) -> str:
        return "laser_cutter"

    def setPowerLevel(self, level: float) -> None:
        self.powerLevel = level

    def cut(self, pattern: str) -> None:
        if not self.isActive:
            raise RuntimeError(f"{self.cutterId} cannot cut while inactive.")
