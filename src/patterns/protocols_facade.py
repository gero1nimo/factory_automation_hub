from __future__ import annotations

from src.interfaces.facade_interface import IProtocolFacade
from src.interfaces.machine_status import MachineStatus
from src.core.mainframe import FactoryMainframe
from src.machines.modern import RoboticArm, SmartConveyor, LaserCutter
from src.patterns.adapters import HydraulicPressAdapter, AnalogFurnaceAdapter


class OperationalFacade(IProtocolFacade):

    def __init__(self, mainframe: FactoryMainframe) -> None:
        self.mainframe = mainframe

    def executeProtocol(self, protocolName: str) -> None:
        protocols = {
            "emergency_stop": self.emergencyStop,
            "startup": self.startupSequence,
            "shutdown": self.shutdownSequence,
            "maintenance": self.maintenanceMode,
        }
        if protocolName not in protocols:
            raise ValueError(f"Unknown protocol: '{protocolName}'")
        protocols[protocolName]()

    def emergencyStop(self) -> None:
        machines = self.mainframe.getMachines()
        for m in machines:
            if isinstance(m, SmartConveyor):
                m.halt()
        for m in machines:
            if isinstance(m, AnalogFurnaceAdapter):
                m.openVents()
        for m in machines:
            if isinstance(m, RoboticArm):
                m.lockArm()
        for m in machines:
            if isinstance(m, LaserCutter):
                m.stop()
            elif isinstance(m, HydraulicPressAdapter):
                m.sendPLCCommand("EMERGENCY_VENT")
                m.stop()

    def startupSequence(self) -> None:
        order = (SmartConveyor, AnalogFurnaceAdapter, RoboticArm, LaserCutter, HydraulicPressAdapter)
        for machine_type in order:
            for m in self.mainframe.getMachines():
                if isinstance(m, machine_type):
                    m.start()

    def shutdownSequence(self) -> None:
        order = (HydraulicPressAdapter, LaserCutter, RoboticArm, AnalogFurnaceAdapter, SmartConveyor)
        for machine_type in order:
            for m in self.mainframe.getMachines():
                if isinstance(m, machine_type):
                    m.stop()

    def maintenanceMode(self) -> None:
        self.shutdownSequence()
        for m in self.mainframe.getMachines():
            m.status = MachineStatus.MAINTENANCE
