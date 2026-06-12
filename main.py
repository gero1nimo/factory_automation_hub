# main.py
# Simulation entry point. Runs through all four design patterns step by step.
# Machine config is loaded from data/plant_config.json.
# Run with:  python main.py

import json
import os

from src.core.mainframe import FactoryMainframe
from src.patterns.machinery_factory import MachineryFactory
from src.patterns.protocols_facade import ProtocolFacade
from src.utils.display import (
    console,
    section_header,
    print_machine_registered,
    print_singleton_check,
    print_results,
    print_log_tail,
    print_summary,
)

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data", "plant_config.json")


def _load_config() -> list:
    with open(_CONFIG_PATH) as f:
        return json.load(f)


def run_simulation() -> None:

    # ── STEP 1: Singleton ────────────────────────────────────────────────────
    section_header(1, "Singleton: FactoryMainframe")

    hub_a = FactoryMainframe()
    hub_b = FactoryMainframe()
    print_singleton_check(id(hub_a), id(hub_b), hub_a is hub_b)
    assert hub_a is hub_b, "FAIL — two separate mainframe instances exist!"
    mainframe = hub_a

    # ── STEP 2: Factory Method ───────────────────────────────────────────────
    section_header(2, "Factory Method: MachineryFactory")

    for cfg in _load_config():
        machine = MachineryFactory.create(cfg)
        mainframe.register_machine(machine)
        print_machine_registered(machine.machine_id, type(machine).__name__)

    console.print(f"\n  Total machines on floor: [bold]{len(mainframe.all_machine_ids())}[/bold]")

    # ── STEP 3: Adapter ──────────────────────────────────────────────────────
    section_header(3, "Adapter: Legacy machines via PLC / Relay adapters")

    legacy_ids = [mid for mid in mainframe.all_machine_ids() if "ADAPTER" in mid]
    console.print(
        "  The mainframe calls standard [italic]activate()[/italic] on legacy machines.\n"
        "  It has zero knowledge of [italic]plc_pressurize()[/italic] or [italic]relay_ignite()[/italic].\n"
    )
    for mid in legacy_ids:
        console.print(f"  {mainframe.activate_machine(mid)}")

    console.print("\n  [dim]Status back through the adapters:[/dim]")
    for mid in legacy_ids:
        console.print(f"  {mainframe.get_machine(mid).status_report()}")

    # ── STEP 4: Facade — startup ─────────────────────────────────────────────
    section_header(4, "Facade: Startup Sequence")

    facade = ProtocolFacade(mainframe)
    print_results(facade.startup_sequence())

    # ── STEP 5: Floor status ─────────────────────────────────────────────────
    section_header(5, "Floor Status Snapshot")

    for line in mainframe.floor_status():
        console.print(f"  {line}")

    # ── STEP 6: Facade — emergency stop ──────────────────────────────────────
    section_header(6, "Facade: Emergency Stop")

    print_results(facade.emergency_stop())

    # ── STEP 7: DIP ──────────────────────────────────────────────────────────
    section_header(7, "DIP: Mainframe talks through INetworkMachine only")

    console.print("  Bringing ARM-01 and CONV-01 back online individually.")
    console.print("  [dim]Mainframe holds Dict[str, INetworkMachine] — no concrete types.[/dim]\n")
    console.print(f"  {mainframe.activate_machine('ARM-01')}")
    console.print(f"  {mainframe.activate_machine('CONV-01')}")

    # ── STEP 8: Facade — fire drill ───────────────────────────────────────────
    section_header(8, "Facade: Fire Drill")

    print_results(facade.fire_drill_protocol())

    # ── STEP 9: Facade — maintenance mode ────────────────────────────────────
    section_header(9, "Facade: Maintenance Mode")

    print_results(facade.maintenance_mode())

    # ── STEP 10: Factory error handling ──────────────────────────────────────
    section_header(10, "Error Handling: unrecognised machine type")

    try:
        MachineryFactory.create({"type": "quantum_teleporter", "id": "QT-99"})
    except ValueError as err:
        console.print(f"  [red]Factory raised ValueError as expected:[/red]\n  -> {err}")

    # ── STEP 11: Audit log ────────────────────────────────────────────────────
    section_header(11, "Mainframe audit log (last 10 entries)")

    print_log_tail(mainframe.get_log()[-10:])

    # ── Summary ───────────────────────────────────────────────────────────────
    console.print()
    print_summary()


if __name__ == "__main__":
    run_simulation()
