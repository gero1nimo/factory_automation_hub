from typing import Dict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

_STATUS_COLOURS = {
    "RUNNING": "bold green",
    "IDLE": "dim",
    "ERROR": "bold red",
    "MAINTENANCE": "yellow",
    "EMERGENCY_STOP": "bold red",
}


def section_header(step: int, title: str) -> None:
    console.print()
    console.rule(f"[bold cyan]STEP {step} - {title}[/bold cyan]", style="cyan")


def info(message: str) -> None:
    console.print(f"  {message}")


def success(message: str) -> None:
    console.print(f"  [green][OK][/green] {message}")


def print_singleton_check(addr_a: int, addr_b: int, same: bool) -> None:
    console.print(f"  getInstance() #1 : [yellow]{addr_a}[/yellow]")
    console.print(f"  getInstance() #2 : [yellow]{addr_b}[/yellow]")
    if same:
        console.print("  [bold green][OK]  SAME object - Singleton confirmed.[/bold green]")
    else:
        console.print("  [bold red][FAIL]  DIFFERENT objects - Singleton broken![/bold red]")


def print_machine_registered(machine_id: str, type_name: str, type_key: str) -> None:
    console.print(
        f"  [green][OK][/green]  built [bold]{machine_id:<14}[/bold] "
        f"([italic]{type_name}[/italic], type='{type_key}')"
    )


def status_table(title: str, status_map: Dict[str, str]) -> None:
    table = Table(title=title, box=box.SIMPLE_HEAVY, title_style="bold")
    table.add_column("Machine ID", style="bold")
    table.add_column("Status")
    for machine_id, status in status_map.items():
        colour = _STATUS_COLOURS.get(status, "white")
        table.add_row(machine_id, f"[{colour}]{status}[/{colour}]")
    console.print(table)


def print_summary() -> None:
    body = (
        "[bold green][OK][/bold green]  Singleton      - FactoryMainframe.getInstance() (one instance)\n"
        "[bold green][OK][/bold green]  Factory Method - MachineryFactory + PlantConfigReader + MachineConfig\n"
        "[bold green][OK][/bold green]  Adapter        - HydraulicPressAdapter / AnalogFurnaceAdapter via PLCController\n"
        "[bold green][OK][/bold green]  Facade         - OperationalFacade (startup, shutdown, emergencyStop, maintenance)\n\n"
        "[bold blue]SOLID principles:[/bold blue]\n"
        "[bold green][OK][/bold green]  DIP  - everything depends on INetworkMachine / IMachineFactory / IProtocolFacade\n"
        "[bold green][OK][/bold green]  SRP  - each class has exactly one job and one reason to change"
    )
    console.print(Panel(body, title="[bold]SIMULATION COMPLETE[/bold]", border_style="green"))
