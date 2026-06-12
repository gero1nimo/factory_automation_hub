# protocols_facade.py
# The Facade pattern lives here. Floor supervisors shouldn't need to know
# which machines to stop first or what order to open vents in —
# they just call emergency_stop() and everything happens correctly underneath.
# Each method below is one "protocol" that hides a multi-step operation
# behind a single function call. The facade talks to the mainframe only,
# never directly to individual machines.

from __future__ import annotations
from typing import List
from src.core.mainframe import FactoryMainframe


class ProtocolFacade:
    """
    Gives floor supervisors five simple commands that each trigger
    a coordinated sequence across all registered machines.
    The complexity of ordering, prioritisation, and status checks
    stays locked inside this class — callers see none of it.

    Available protocols:
        emergency_stop()       -- shut everything down right now
        startup_sequence()     -- bring machines online in a safe order
        shutdown_sequence()    -- power everything down gracefully
        fire_drill_protocol()  -- emergency stop plus floor evacuation status
        maintenance_mode()     -- shutdown plus a full diagnostic readout
    """

    def __init__(self, mainframe: FactoryMainframe) -> None:
        self._hub = mainframe   # all communication goes through the mainframe

    # ------------------------------------------------------------------
    # Protocol 1 — Emergency Stop
    # ------------------------------------------------------------------

    def emergency_stop(self) -> List[str]:
        """
        Stops the whole floor in a specific priority order:
          1. Conveyors first — stops material flow and prevents pile-ups
          2. Furnaces next  — burners off and vents open to release heat
          3. Robotic arms   — joints locked so nobody gets hit
          4. Laser cutters  — beams killed immediately
          5. Hydraulic presses — pressure vented last
        Any machine not caught by keyword matching gets stopped at the end.
        """
        output: List[str] = []
        output.append("=" * 60)
        output.append(">>> PROTOCOL: EMERGENCY STOP INITIATED <<<")
        output.append("=" * 60)

        stop_order   = ["Conveyor", "Furnace", "Arm", "Cutter", "Press"]
        already_done: set = set()

        for keyword in stop_order:
            for mid in self._hub.all_machine_ids():
                if keyword.lower() in mid.lower() and mid not in already_done:
                    output.append(f"  {self._hub.emergency_stop_machine(mid)}")
                    already_done.add(mid)

        # catch anything the keyword loop missed
        for mid in self._hub.all_machine_ids():
            if mid not in already_done:
                output.append(f"  {self._hub.emergency_stop_machine(mid)}")

        output.append(">>> ALL MACHINES HALTED. Alert safety officer. <<<")
        output.append("=" * 60)
        return output

    # ------------------------------------------------------------------
    # Protocol 2 — Startup Sequence
    # ------------------------------------------------------------------

    def startup_sequence(self) -> List[str]:
        """
        Brings machines online in a deliberate order:
          1. Conveyors first so the belt is moving before anything feeds it
          2. Furnaces next — they need warm-up time
          3. Robotic arms — calibrate once surroundings are stable
          4. Laser cutters — armed only after arms are clear
          5. Hydraulic presses — pressurised last
        """
        output: List[str] = []
        output.append("=" * 60)
        output.append(">>> PROTOCOL: STARTUP SEQUENCE INITIATED <<<")
        output.append("=" * 60)

        start_order   = ["Conveyor", "Furnace", "Arm", "Cutter", "Press"]
        already_done: set = set()

        for keyword in start_order:
            for mid in self._hub.all_machine_ids():
                if keyword.lower() in mid.lower() and mid not in already_done:
                    output.append(f"  {self._hub.activate_machine(mid)}")
                    already_done.add(mid)

        for mid in self._hub.all_machine_ids():
            if mid not in already_done:
                output.append(f"  {self._hub.activate_machine(mid)}")

        output.append(">>> Floor is live. All machines operational. <<<")
        output.append("=" * 60)
        return output

    # ------------------------------------------------------------------
    # Protocol 3 — Shutdown Sequence
    # ------------------------------------------------------------------

    def shutdown_sequence(self) -> List[str]:
        """
        Mirror of startup — machines go off in reverse priority order.
        Presses vent first, conveyors stop last.
        """
        output: List[str] = []
        output.append("=" * 60)
        output.append(">>> PROTOCOL: SHUTDOWN SEQUENCE INITIATED <<<")
        output.append("=" * 60)

        stop_order   = ["Press", "Cutter", "Arm", "Furnace", "Conveyor"]
        already_done: set = set()

        for keyword in stop_order:
            for mid in self._hub.all_machine_ids():
                if keyword.lower() in mid.lower() and mid not in already_done:
                    output.append(f"  {self._hub.deactivate_machine(mid)}")
                    already_done.add(mid)

        for mid in self._hub.all_machine_ids():
            if mid not in already_done:
                output.append(f"  {self._hub.deactivate_machine(mid)}")

        output.append(">>> Floor is down. Safe to leave the building. <<<")
        output.append("=" * 60)
        return output

    # ------------------------------------------------------------------
    # Protocol 4 — Fire Drill
    # ------------------------------------------------------------------

    def fire_drill_protocol(self) -> List[str]:
        """
        Emergency stop followed by a full status printout so the safety
        officer can confirm every machine is in a safe state before
        the building is evacuated.
        """
        output: List[str] = []
        output.append("=" * 60)
        output.append(">>> PROTOCOL: FIRE DRILL — EVACUATE FLOOR <<<")
        output.append("=" * 60)

        output.extend(self.emergency_stop())

        output.append("--- Confirming machine states post-halt ---")
        for line in self._hub.floor_status():
            output.append(f"  {line}")

        output.append(">>> Floor cleared. Proceed with evacuation. <<<")
        output.append("=" * 60)
        return output

    # ------------------------------------------------------------------
    # Protocol 5 — Maintenance Mode
    # ------------------------------------------------------------------

    def maintenance_mode(self) -> List[str]:
        """
        Runs a graceful shutdown and then prints a full diagnostic
        so the maintenance crew knows exactly what state each machine is in.
        """
        output: List[str] = []
        output.append("=" * 60)
        output.append(">>> PROTOCOL: MAINTENANCE MODE <<<")
        output.append("=" * 60)

        output.extend(self.shutdown_sequence())

        output.append("--- Full diagnostic for maintenance crew ---")
        for line in self._hub.floor_status():
            output.append(f"  {line}")

        output.append(">>> Machines ready for inspection. <<<")
        output.append("=" * 60)
        return output
