from abc import ABC, abstractmethod


class IProtocolFacade(ABC):

    @abstractmethod
    def executeProtocol(self, protocolName: str) -> None: ...
