import os

from src.core.mainframe import FactoryMainframe
from src.patterns.protocols_facade import OperationalFacade
from src.patterns.machinery_factory import MachineryFactory
from src.interfaces.machine_config import MachineConfig
from src.interfaces.network_machine import INetworkMachine
from src.patterns.adapters import HydraulicPressAdapter, AnalogFurnaceAdapter
from src.utils import display

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data", "plant_config.json")


def run_simulation() -> None:

    display.section_header(1, "Singleton: FactoryMainframe.getInstance()")
    hub_a = FactoryMainframe.getInstance()
    hub_b = FactoryMainframe.getInstance()
    display.print_singleton_check(id(hub_a), id(hub_b), hub_a is hub_b)
    assert hub_a is hub_b
    mainframe = hub_a

    display.section_header(2, "Factory Method: loadFromConfig()")
    mainframe.loadFromConfig(_CONFIG_PATH)
    for machine in mainframe.getMachines():
        display.print_machine_registered(
            machine.getId(), type(machine).__name__, machine.getType()
        )
    display.success(
        f"{len(mainframe.getMachines())} machines built from "
        f"{os.path.basename(_CONFIG_PATH)} via PlantConfigReader."
    )

    display.section_header(3, "Adapter: Legacy machines via PLCController")
    display.info("Mainframe calls start()/stop(); the adapter translates to the legacy PLC API.\n")
    for machine in mainframe.getMachines():
        if isinstance(machine, (HydraulicPressAdapter, AnalogFurnaceAdapter)):
            machine.start()
            legacy = getattr(machine, "press", None) or getattr(machine, "furnace")
            display.info(
                f"{machine.getId():<14} PLC[{machine.plcController.protocol}] "
                f"-> {machine.plcController.getResponse()}"
            )
            display.info(f"{'':<14} raw legacy state -> {legacy.getAnalogStatus()}")

    display.section_header(4, "Facade: OperationalFacade.startupSequence()")
    facade = OperationalFacade(mainframe)
    facade.startupSequence()
    display.success("Startup protocol complete.")
    display.status_table("Floor status after startup", mainframe.getSystemStatus())

    display.section_header(5, "Facade: executeProtocol('emergency_stop')")
    facade.executeProtocol("emergency_stop")
    display.status_table("Floor status after emergency stop", mainframe.getSystemStatus())

    display.section_header(6, "DIP: mainframe depends only on INetworkMachine")
    arm = mainframe.getMachineById("ARM-01")
    display.info(
        f"ARM-01 is a {type(arm).__name__}, but the hub holds it as "
        f"INetworkMachine: {isinstance(arm, INetworkMachine)}"
    )
    arm.start()
    display.info(f"ARM-01 restarted individually -> {arm.getStatus().name}")

    display.section_header(7, "Facade: OperationalFacade.maintenanceMode()")
    facade.maintenanceMode()
    display.status_table("Floor status in maintenance", mainframe.getSystemStatus())

    display.section_header(8, "Error Handling: unrecognised machine type")
    try:
        MachineryFactory().createMachine(
            "quantum_teleporter", MachineConfig("quantum_teleporter", "QT-99")
        )
    except ValueError as err:
        display.success(f"ValueError raised as expected -> {err}")

    display.console.print()
    display.print_summary()


if __name__ == "__main__":
    run_simulation()
