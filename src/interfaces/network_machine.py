from abc import ABC, abstractmethod

from src.interfaces.machine_status import MachineStatus


class INetworkMachine(ABC):

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def getStatus(self) -> MachineStatus: ...

    @abstractmethod
    def getId(self) -> str: ...

    @abstractmethod
    def getType(self) -> str: ...
