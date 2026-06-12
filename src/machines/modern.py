# modern.py
# The three networked machines that live on the factory floor.
# Each one only worries about its own state and behavior — the mainframe
# tells them what to do, but they decide how to do it internally.
# All three implement INetworkMachine so the mainframe treats them uniformly.

from src.interfaces.network_machine import INetworkMachine


class RoboticArm(INetworkMachine):
    """A six-axis robotic arm that handles pick-and-place operations."""

    def __init__(self, unit_id: str) -> None:
        self._id       = unit_id
        self._active   = False
        self._locked   = False   # goes True on an emergency stop

    @property
    def machine_id(self) -> str:
        return self._id

    def activate(self) -> str:
        self._active = True
        self._locked = False
        return f"[RoboticArm {self._id}] Joints homed and calibrated — ready for work."

    def deactivate(self) -> str:
        self._active = False
        return f"[RoboticArm {self._id}] Moved to home position, motors disengaged."

    def emergency_stop(self) -> str:
        self._active = False
        self._locked = True
        return f"[RoboticArm {self._id}] EMERGENCY LOCK — all joints frozen in place."

    def status_report(self) -> str:
        if self._locked:
            state = "LOCKED"
        elif self._active:
            state = "RUNNING"
        else:
            state = "IDLE"
        return f"[RoboticArm {self._id}] Current state: {state}"


class SmartConveyor(INetworkMachine):
    """Belt conveyor with software-controlled variable speed."""

    def __init__(self, unit_id: str, belt_speed_mps: float = 0.5) -> None:
        self._id      = unit_id
        self._speed   = belt_speed_mps
        self._running = False

    @property
    def machine_id(self) -> str:
        return self._id

    def activate(self) -> str:
        self._running = True
        return f"[SmartConveyor {self._id}] Belt moving at {self._speed} m/s."

    def deactivate(self) -> str:
        self._running = False
        return f"[SmartConveyor {self._id}] Belt slowed and stopped safely."

    def emergency_stop(self) -> str:
        self._running = False
        return f"[SmartConveyor {self._id}] EMERGENCY STOP — belt cut immediately."

    def status_report(self) -> str:
        state = f"MOVING @ {self._speed} m/s" if self._running else "STOPPED"
        return f"[SmartConveyor {self._id}] Current state: {state}"


class LaserCutter(INetworkMachine):
    """CNC laser cutter with programmable power output."""

    def __init__(self, unit_id: str, power_watts: int = 200) -> None:
        self._id      = unit_id
        self._power   = power_watts
        self._beam_on = False

    @property
    def machine_id(self) -> str:
        return self._id

    def activate(self) -> str:
        self._beam_on = True
        return f"[LaserCutter {self._id}] Beam live at {self._power} W — interlocks verified."

    def deactivate(self) -> str:
        self._beam_on = False
        return f"[LaserCutter {self._id}] Beam off, shutter closed, fans running."

    def emergency_stop(self) -> str:
        self._beam_on = False
        return f"[LaserCutter {self._id}] EMERGENCY STOP — beam killed, shutter down."

    def status_report(self) -> str:
        state = f"BEAM ACTIVE @ {self._power} W" if self._beam_on else "STANDBY"
        return f"[LaserCutter {self._id}] Current state: {state}"
