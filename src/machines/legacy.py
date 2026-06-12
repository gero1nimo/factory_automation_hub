class LegacyHydraulicPress:

    def __init__(self) -> None:
        self.pressureLevel = 0.0
        self.isActive = False

    def activateManually(self) -> None:
        self.isActive = True
        if self.pressureLevel == 0.0:
            self.pressureLevel = 150.0

    def deactivateManually(self) -> None:
        self.isActive = False
        self.pressureLevel = 0.0

    def setPressure(self, level: float) -> None:
        self.pressureLevel = level

    def getAnalogStatus(self) -> str:
        state = "ACTIVE" if self.isActive else "OFF"
        return f"HydraulicPress [{state}] pressure={self.pressureLevel} bar"


class AnalogFurnace:

    def __init__(self) -> None:
        self.temperature = 20.0
        self.isVentOpen = False
        self.isIgnited = False

    def ignite(self) -> None:
        self.isIgnited = True
        self.isVentOpen = False
        self.temperature = 900.0

    def extinguish(self) -> None:
        self.isIgnited = False
        self.temperature = 20.0

    def openVents(self) -> None:
        self.isVentOpen = True

    def closeVents(self) -> None:
        self.isVentOpen = False

    def getAnalogStatus(self) -> str:
        ignition = "LIT" if self.isIgnited else "COLD"
        vent = "OPEN" if self.isVentOpen else "CLOSED"
        return f"AnalogFurnace [{ignition}] temp={self.temperature}C vents={vent}"
