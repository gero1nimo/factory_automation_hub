# network_machine.py
# Holds the shared contract that every machine on the floor must follow.
# Whether a machine is brand new and networked or a 30-year-old analog unit
# wrapped in an adapter, the mainframe only ever talks to this interface.
# This is the backbone of the Dependency Inversion Principle in our design.

from abc import ABC, abstractmethod


class INetworkMachine(ABC):
    """
    Every machine registered on the factory floor implements this.
    Modern machines do it directly; legacy machines go through an adapter
    that handles the translation behind the scenes.
    """

    @abstractmethod
    def activate(self) -> str:
        """Bring this machine up to a working state."""

    @abstractmethod
    def deactivate(self) -> str:
        """Power the machine down in a controlled way."""

    @abstractmethod
    def emergency_stop(self) -> str:
        """Cut all activity immediately — used when something goes wrong."""

    @abstractmethod
    def status_report(self) -> str:
        """Give back a short plain-English status line."""

    @property
    @abstractmethod
    def machine_id(self) -> str:
        """Each machine needs a unique tag so the mainframe can track it."""
