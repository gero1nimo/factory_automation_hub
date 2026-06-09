# driver.py
# Entry point for the factory automation simulation.
# Runs through all four design patterns step by step and prints
# the output so you can see exactly what each one does.
#
# Run with:  python driver.py

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from patterns.mainframe   import FactoryMainframe
from patterns.factory     import MachineryFactory
from protocols.protocols  import ProtocolFacade


# ── formatting helpers ──────────────────────────────────────────────────────

THIN_LINE  = "─" * 65
THICK_LINE = "═" * 65

def section_header(title: str) -> None:
    print(f"\n{THICK_LINE}")
    print(f"  {title}")
    print(THICK_LINE)

def sub_header(label: str) -> None:
    print(f"\n{THIN_LINE}")
    print(f"  {label}")
    print(THIN_LINE)

def dump(lines: list) -> None:
    for ln in lines:
        print(ln)


# ── plant config — simulates reading from a file ────────────────────────────
# In a real deployment this would be loaded from JSON or a database.
# Here we hard-code it so the simulation is self-contained.

PLANT_CONFIG = [
    {"type": "robotic_arm",     "id": "ARM-01"},
    {"type": "robotic_arm",     "id": "ARM-02"},
    {"type": "smart_conveyor",  "id": "CONV-01", "speed": 0.8},
    {"type": "smart_conveyor",  "id": "CONV-02", "speed": 0.4},
    {"type": "laser_cutter",    "id": "LASER-01", "power": 350},
    {"type": "hydraulic_press", "id": "PRESS-SN7741"},
    {"type": "analog_furnace",  "id": "FURN-TAG-A3"},
]


# ── simulation ───────────────────────────────────────────────────────────────

def run_simulation() -> None:

    # ── STEP 1: Singleton verification ──────────────────────────────────────
    section_header("STEP 1 — Singleton: FactoryMainframe")

    hub_a = FactoryMainframe()
    hub_b = FactoryMainframe()

    print(f"  hub_a memory address : {id(hub_a)}")
    print(f"  hub_b memory address : {id(hub_b)}")
    print(f"  Same object?         : {hub_a is hub_b}")

    assert hub_a is hub_b, "FAIL — two separate mainframe instances exist!"
    print("  ✔  Singleton confirmed: only one FactoryMainframe in memory.")

    mainframe = hub_a

    # ── STEP 2: Factory Method — spawn all machines from config ─────────────
    section_header("STEP 2 — Factory Method: MachineryFactory")

    for cfg in PLANT_CONFIG:
        m = MachineryFactory.create(cfg)
        mainframe.register_machine(m)
        print(f"  Built & registered  →  {m.machine_id}  ({type(m).__name__})")

    print(f"\n  Total machines on floor: {len(mainframe.all_machine_ids())}")

    # ── STEP 3: Adapter — legacy machines exposed as INetworkMachine ─────────
    section_header("STEP 3 — Adapter: Legacy machines via PLC / Relay adapters")

    legacy_ids = [mid for mid in mainframe.all_machine_ids() if "ADAPTER" in mid]

    print("  The mainframe calls standard activate() on legacy machines.")
    print("  It has zero knowledge of plc_pressurize() or relay_ignite().\n")

    for mid in legacy_ids:
        print(f"  {mainframe.activate_machine(mid)}")

    print("\n  Reading status back through the adapters:")
    for mid in legacy_ids:
        print(f"  {mainframe.get_machine(mid).status_report()}")

    # ── STEP 4: Facade — startup sequence ────────────────────────────────────
    section_header("STEP 4 — Facade: Startup Sequence protocol")

    facade = ProtocolFacade(mainframe)
    dump(facade.startup_sequence())

    # ── STEP 5: Floor status snapshot ────────────────────────────────────────
    section_header("STEP 5 — Floor Status Snapshot")

    sub_header("All machines reporting in:")
    for line in mainframe.floor_status():
        print(f"  {line}")

    # ── STEP 6: Facade — emergency stop ──────────────────────────────────────
    section_header("STEP 6 — Facade: Emergency Stop protocol")

    dump(facade.emergency_stop())

    # ── STEP 7: DIP — mainframe only knows INetworkMachine ───────────────────
    section_header("STEP 7 — DIP: Mainframe talks through INetworkMachine only")

    print("  Bringing ARM-01 and CONV-01 back online individually.")
    print("  Mainframe holds Dict[str, INetworkMachine] — no concrete types.\n")
    print(f"  {mainframe.activate_machine('ARM-01')}")
    print(f"  {mainframe.activate_machine('CONV-01')}")

    # ── STEP 8: Facade — fire drill ───────────────────────────────────────────
    section_header("STEP 8 — Facade: Fire Drill protocol")

    dump(facade.fire_drill_protocol())

    # ── STEP 9: Facade — maintenance mode ────────────────────────────────────
    section_header("STEP 9 — Facade: Maintenance Mode protocol")

    dump(facade.maintenance_mode())

    # ── STEP 10: Factory error handling ──────────────────────────────────────
    section_header("STEP 10 — Error Handling: unrecognised machine type")

    try:
        MachineryFactory.create({"type": "quantum_teleporter", "id": "QT-99"})
    except ValueError as err:
        print(f"  Factory raised ValueError as expected:\n  → {err}")

    # ── STEP 11: Audit log tail ───────────────────────────────────────────────
    section_header("STEP 11 — Mainframe audit log (last 10 entries)")

    for entry in mainframe.get_log()[-10:]:
        print(f"  LOG ▸ {entry}")

    # ── Summary ───────────────────────────────────────────────────────────────
    section_header("SIMULATION COMPLETE")
    print("  Patterns demonstrated:")
    print("    ✔  Singleton      — FactoryMainframe (one instance enforced)")
    print("    ✔  Factory Method — MachineryFactory.create(config)")
    print("    ✔  Adapter        — HydraulicPressAdapter, AnalogFurnaceAdapter")
    print("    ✔  Facade         — Startup, Shutdown, EmergencyStop, FireDrill, Maintenance")
    print()
    print("  SOLID principles:")
    print("    ✔  DIP  — FactoryMainframe imports only INetworkMachine")
    print("    ✔  SRP  — each class has exactly one job and one reason to change")
    print(THICK_LINE)


if __name__ == "__main__":
    run_simulation()
