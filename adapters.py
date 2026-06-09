# adapters.py
# This is where the Adapter pattern lives.
# The two legacy machines have their own weird vendor commands that nothing
# else in our system understands. These adapter classes sit in between —
# they look like INetworkMachine to the mainframe, but they quietly
# translate each call into whatever the old hardware actually needs.
# Think of it like a power plug converter: same electricity, different socket.

from machines.interfaces import INetworkMachine
from machines.legacy_machines import LegacyHydraulicPress, AnalogFurnace


class HydraulicPressAdapter(INetworkMachine):
    """
    Wraps the old hydraulic press so the mainframe can treat it
    like any other networked machine. Internally this acts as a
    simulated PLC controller that forwards translated commands.
    """

    def __init__(self, press: LegacyHydraulicPress) -> None:
        self._press  = press    # the actual legacy hardware object
        self._online = False

    @property
    def machine_id(self) -> str:
        return f"ADAPTER-HydPress-{self._press.serial_number}"

    def activate(self) -> str:
        self._online = True
        raw = self._press.plc_pressurize(bar=150)
        return f"[PLC Adapter] activate → {raw}"

    def deactivate(self) -> str:
        self._online = False
        raw = self._press.plc_release_pressure()
        return f"[PLC Adapter] deactivate → {raw}"

    def emergency_stop(self) -> str:
        self._online = False
        raw = self._press.plc_vent_emergency()
        return f"[PLC Adapter] emergency_stop → {raw}"

    def status_report(self) -> str:
        gauge      = self._press.plc_read_gauge()
        connection = "ONLINE" if self._online else "OFFLINE"
        return f"[PLC Adapter | {connection}] {gauge}"


class AnalogFurnaceAdapter(INetworkMachine):
    """
    Wraps the analog furnace behind a simulated relay controller.
    From the mainframe's perspective this is just another INetworkMachine —
    the messy relay commands stay hidden inside this class.
    """

    def __init__(self, furnace: AnalogFurnace) -> None:
        self._furnace = furnace  # actual legacy hardware object
        self._online  = False

    @property
    def machine_id(self) -> str:
        return f"ADAPTER-Furnace-{self._furnace.furnace_tag}"

    def activate(self) -> str:
        self._online = True
        ignite = self._furnace.relay_ignite(target_temp=900)
        seal   = self._furnace.relay_close_vents()
        return f"[Relay Adapter] activate → {ignite} | {seal}"

    def deactivate(self) -> str:
        self._online  = False
        burners_off   = self._furnace.relay_shutdown_burners()
        open_vents    = self._furnace.relay_open_vents()
        return f"[Relay Adapter] deactivate → {burners_off} | {open_vents}"

    def emergency_stop(self) -> str:
        self._online  = False
        burners_off   = self._furnace.relay_shutdown_burners()
        open_vents    = self._furnace.relay_open_vents()
        return f"[Relay Adapter] emergency_stop → {burners_off} | {open_vents}"

    def status_report(self) -> str:
        reading    = self._furnace.relay_read_thermocouple()
        connection = "ONLINE" if self._online else "OFFLINE"
        return f"[Relay Adapter | {connection}] {reading}"
