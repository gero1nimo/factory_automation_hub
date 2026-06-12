from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MachineConfig:
    machineType: str
    machineId: str
    parameters: dict = field(default_factory=dict)
