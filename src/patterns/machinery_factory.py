from __future__ import annotations

import json
from typing import List

from src.interfaces.factory_interface import IMachineFactory
from src.interfaces.network_machine import INetworkMachine
from src.interfaces.machine_config import MachineConfig
from src.machines.modern import RoboticArm, SmartConveyor, LaserCutter
from src.machines.legacy import LegacyHydraulicPress, AnalogFurnace
from src.patterns.adapters import HydraulicPressAdapter, AnalogFurnaceAdapter


class PlantConfigReader:

    def readConfig(self, filePath: str) -> List[MachineConfig]:
        with open(filePath, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return [self.parseEntry(entry) for entry in raw]

    def parseEntry(self, entry: dict) -> MachineConfig:
        return MachineConfig(
            machineType=entry["machineType"],
            machineId=entry["machineId"],
            parameters=entry.get("parameters", {}),
        )


class MachineryFactory(IMachineFactory):

    def __init__(self) -> None:
        self.configReader = PlantConfigReader()

    def createMachine(self, machineType: str, config: MachineConfig) -> INetworkMachine:
        params = config.parameters

        if machineType == "robotic_arm":
            return RoboticArm(armId=config.machineId)
        if machineType == "smart_conveyor":
            return SmartConveyor(conveyorId=config.machineId, speed=params.get("speed", 0.5))
        if machineType == "laser_cutter":
            return LaserCutter(cutterId=config.machineId, powerLevel=params.get("power", 200))
        if machineType == "hydraulic_press":
            return HydraulicPressAdapter(LegacyHydraulicPress(), config.machineId)
        if machineType == "analog_furnace":
            return AnalogFurnaceAdapter(AnalogFurnace(), config.machineId)

        raise ValueError(f"MachineryFactory: '{machineType}' is not a recognised machine type.")

    def createFromConfig(self, configFile: str) -> List[INetworkMachine]:
        configs = self.configReader.readConfig(configFile)
        return [self.createMachine(cfg.machineType, cfg) for cfg in configs]
