# legacy_machines.py
# These two machines predate the factory network entirely.
# They have no idea what INetworkMachine is — they just expose
# whatever vendor API they shipped with back in the day.
# The adapter layer (in adapters.py) is what bridges the gap.

class LegacyHydraulicPress:
    """
    Old hydraulic press that runs off physical PLC toggle switches.
    It speaks its own proprietary command set — nothing standard about it.
    """

    def __init__(self, serial_number: str) -> None:
        self.serial_number = serial_number
        self._pressure_bar = 0
        self._valve_open   = False

    # ---- vendor PLC commands ----

    def plc_pressurize(self, bar: int = 150) -> str:
        self._pressure_bar = bar
        return (f"[HydraulicPress SN={self.serial_number}] "
                f"PLC: building pressure to {bar} bar.")

    def plc_release_pressure(self) -> str:
        self._pressure_bar = 0
        self._valve_open   = True
        return (f"[HydraulicPress SN={self.serial_number}] "
                f"PLC: pressure bled off, safety valve open.")

    def plc_vent_emergency(self) -> str:
        self._pressure_bar = 0
        self._valve_open   = True
        return (f"[HydraulicPress SN={self.serial_number}] "
                f"PLC EMERGENCY: hydraulic pressure dumped instantly!")

    def plc_read_gauge(self) -> str:
        valve = "OPEN" if self._valve_open else "CLOSED"
        return (f"[HydraulicPress SN={self.serial_number}] "
                f"Pressure gauge: {self._pressure_bar} bar | Valve: {valve}.")


class AnalogFurnace:
    """
    Industrial furnace wired to thermocouple relays — no network port anywhere.
    Commands go through physical relay switches, not software packets.
    """

    def __init__(self, furnace_tag: str) -> None:
        self.furnace_tag  = furnace_tag
        self._temp_celsius = 20
        self._vent_open    = False

    # ---- vendor relay commands ----

    def relay_ignite(self, target_temp: int = 900) -> str:
        self._temp_celsius = target_temp
        self._vent_open    = False
        return (f"[AnalogFurnace TAG={self.furnace_tag}] "
                f"Relay: burners lit, climbing to {target_temp} °C.")

    def relay_shutdown_burners(self) -> str:
        self._temp_celsius = 20
        return (f"[AnalogFurnace TAG={self.furnace_tag}] "
                f"Relay: burners off, temperature falling.")

    def relay_open_vents(self) -> str:
        self._vent_open = True
        return (f"[AnalogFurnace TAG={self.furnace_tag}] "
                f"Relay: vents open, heat escaping.")

    def relay_close_vents(self) -> str:
        self._vent_open = False
        return (f"[AnalogFurnace TAG={self.furnace_tag}] "
                f"Relay: vents sealed.")

    def relay_read_thermocouple(self) -> str:
        vents = "OPEN" if self._vent_open else "CLOSED"
        return (f"[AnalogFurnace TAG={self.furnace_tag}] "
                f"Thermocouple: {self._temp_celsius} °C | Vents: {vents}.")
