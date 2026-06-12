from __future__ import annotations

from typing import Dict, List, Optional

from src.interfaces.network_machine import INetworkMachine
from src.interfaces.factory_interface import IMachineFactory
from src.patterns.machinery_factory import MachineryFactory


class FactoryMainframe:

    _instance: Optional["FactoryMainframe"] = None

    def __new__(cls) -> "FactoryMainframe":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._machines: List[INetworkMachine] = []
        self._factory: IMachineFactory = MachineryFactory()
        self._initialized = True

    @classmethod
    def getInstance(cls) -> "FactoryMainframe":
        return cls()

    def registerMachine(self, machine: INetworkMachine) -> None:
        self._machines.append(machine)

    def removeMachine(self, machineId: str) -> None:
        self._machines = [m for m in self._machines if m.getId() != machineId]

    def getMachines(self) -> List[INetworkMachine]:
        return list(self._machines)

    def getMachineById(self, id: str) -> INetworkMachine:
        for machine in self._machines:
            if machine.getId() == id:
                return machine
        raise KeyError(f"No machine registered with id '{id}'.")

    def startAll(self) -> None:
        for machine in self._machines:
            machine.start()

    def stopAll(self) -> None:
        for machine in self._machines:
            machine.stop()

    def getSystemStatus(self) -> Dict[str, str]:
        return {m.getId(): m.getStatus().name for m in self._machines}

    def loadFromConfig(self, configFile: str) -> None:
        for machine in self._factory.createFromConfig(configFile):
            self.registerMachine(machine)
