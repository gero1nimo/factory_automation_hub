from abc import ABC, abstractmethod

from src.interfaces.network_machine import INetworkMachine
from src.interfaces.machine_config import MachineConfig


class IMachineFactory(ABC):

    @abstractmethod
    def createMachine(self, machineType: str, config: MachineConfig) -> INetworkMachine: ...
