# mainframe.py
# The FactoryMainframe is the single coordination point for the whole floor.
# We use the Singleton pattern here because having two mainframes running
# at the same time would cause chaos — machines could get conflicting commands.
# The mainframe only knows about INetworkMachine, never about concrete types,
# which keeps the Dependency Inversion Principle intact throughout.

from __future__ import annotations
from typing import Dict, List, Optional
from machines.interfaces import INetworkMachine


class FactoryMainframe:
    """
    One and only one instance of this class can exist at any point.
    Its job is to keep a registry of all floor machines and route
    high-level commands to them. It does NOT know how any individual
    machine works internally — that is each machine's own business (SRP).
    """

    _instance: Optional[FactoryMainframe] = None

    # ------------------------------------------------------------------
    # Singleton gate — intercepts construction
    # ------------------------------------------------------------------

    def __new__(cls) -> FactoryMainframe:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._ready = False   # flag so __init__ only runs once
        return cls._instance

    def __init__(self) -> None:
        if self._ready:
            return   # already set up on a previous call, do nothing
        self._floor: Dict[str, INetworkMachine] = {}
        self._event_log: List[str] = []
        self._ready = True
        self._log("FactoryMainframe booted. Waiting for machine registrations.")

    # ------------------------------------------------------------------
    # Machine registry management
    # ------------------------------------------------------------------

    def register_machine(self, machine: INetworkMachine) -> None:
        """Add a machine to the floor so the mainframe can talk to it."""
        self._floor[machine.machine_id] = machine
        self._log(f"Registered machine: {machine.machine_id}")

    def unregister_machine(self, machine_id: str) -> None:
        """Pull a machine off the floor registry."""
        if machine_id in self._floor:
            del self._floor[machine_id]
            self._log(f"Removed machine: {machine_id}")

    def get_machine(self, machine_id: str) -> INetworkMachine:
        if machine_id not in self._floor:
            raise KeyError(f"No machine found with id '{machine_id}'.")
        return self._floor[machine_id]

    def all_machine_ids(self) -> List[str]:
        return list(self._floor.keys())

    # ------------------------------------------------------------------
    # Command routing — mainframe delegates, never does the work itself
    # ------------------------------------------------------------------

    def activate_machine(self, machine_id: str) -> str:
        msg = self._floor[machine_id].activate()
        self._log(msg)
        return msg

    def deactivate_machine(self, machine_id: str) -> str:
        msg = self._floor[machine_id].deactivate()
        self._log(msg)
        return msg

    def emergency_stop_machine(self, machine_id: str) -> str:
        msg = self._floor[machine_id].emergency_stop()
        self._log(msg)
        return msg

    def floor_status(self) -> List[str]:
        """Collect a status line from every machine currently registered."""
        snapshot = [m.status_report() for m in self._floor.values()]
        for line in snapshot:
            self._log(line)
        return snapshot

    # ------------------------------------------------------------------
    # Internal event log
    # ------------------------------------------------------------------

    def _log(self, message: str) -> None:
        self._event_log.append(message)

    def get_log(self) -> List[str]:
        return list(self._event_log)

    # ------------------------------------------------------------------
    # Test helper — resets the singleton between unit tests
    # ------------------------------------------------------------------

    @classmethod
    def _reset_for_testing(cls) -> None:
        """Only call this from test code — never in production."""
        cls._instance = None
