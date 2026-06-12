from __future__ import annotations

from typing import Optional

from src.interfaces.network_machine import INetworkMachine
from src.interfaces.machine_status import MachineStatus
from src.machines.legacy import LegacyHydraulicPress, AnalogFurnace


class PLCController:

    def __init__(self, controllerId: str, protocol: str = "MODBUS") -> None:
        self.controllerId = controllerId
        self.protocol = protocol
        self._connected = False
        self._lastResponse = ""

    def connect(self) -> None:
        self._connected = True
        self._lastResponse = f"{self.controllerId}: link up over {self.protocol}"

    def disconnect(self) -> None:
        self._connected = False
        self._lastResponse = f"{self.controllerId}: link down"

    def sendCommand(self, command: str) -> bool:
        if not self._connected:
            self._lastResponse = f"{self.controllerId}: DROPPED '{command}' (offline)"
            return False
        self._lastResponse = f"{self.controllerId}: ACK '{command}'"
        return True

    def getResponse(self) -> str:
        return self._lastResponse

    def isConnected(self) -> bool:
        return self._connected


class HydraulicPressAdapter(INetworkMachine):

    def __init__(self, press: LegacyHydraulicPress, machineId: str,
                 plcController: Optional[PLCController] = None) -> None:
        self.machineId = machineId
        self.press = press
        self.plcController = plcController or PLCController(f"PLC-{machineId}")
        self.status = MachineStatus.IDLE

    def start(self) -> None:
        self.plcController.connect()
        self.plcController.sendCommand("PRESSURIZE 150")
        self.press.activateManually()
        self.press.setPressure(150.0)
        self.status = MachineStatus.RUNNING

    def stop(self) -> None:
        self.plcController.sendCommand("RELEASE")
        self.press.deactivateManually()
        self.plcController.disconnect()
        self.status = MachineStatus.IDLE

    def getStatus(self) -> MachineStatus:
        return self.status

    def getId(self) -> str:
        return self.machineId

    def getType(self) -> str:
        return "hydraulic_press"

    def sendPLCCommand(self, cmd: str) -> bool:
        return self.plcController.sendCommand(cmd)


class AnalogFurnaceAdapter(INetworkMachine):

    def __init__(self, furnace: AnalogFurnace, machineId: str,
                 plcController: Optional[PLCController] = None) -> None:
        self.machineId = machineId
        self.furnace = furnace
        self.plcController = plcController or PLCController(f"PLC-{machineId}")
        self.status = MachineStatus.IDLE

    def start(self) -> None:
        self.plcController.connect()
        self.plcController.sendCommand("IGNITE 900")
        self.furnace.closeVents()
        self.furnace.ignite()
        self.status = MachineStatus.RUNNING

    def stop(self) -> None:
        self.plcController.sendCommand("SHUTDOWN")
        self.furnace.extinguish()
        self.furnace.openVents()
        self.plcController.disconnect()
        self.status = MachineStatus.IDLE

    def getStatus(self) -> MachineStatus:
        return self.status

    def getId(self) -> str:
        return self.machineId

    def getType(self) -> str:
        return "analog_furnace"

    def openVents(self) -> None:
        self.plcController.sendCommand("OPEN_VENTS")
        self.furnace.openVents()
        self.status = MachineStatus.EMERGENCY_STOP

    def sendPLCCommand(self, cmd: str) -> bool:
        return self.plcController.sendCommand(cmd)
