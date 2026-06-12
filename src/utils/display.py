# display.py
# All Rich-based terminal formatting lives here.
# main.py stays clean — it calls these helpers and never touches Rich directly.

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich import box
from typing import List

console = Console()


def section_header(step: int, title: str) -> None:
    console.print()
    console.rule(f"[bold cyan]STEP {step} — {title}[/bold cyan]", style="cyan")


def print_results(lines: List[str]) -> None:
    for line in lines:
        console.print(f"  [dim]{line}[/dim]")


def print_machine_registered(machine_id: str, type_name: str) -> None:
    console.print(
        f"  [green][OK][/green]  Built & registered -> "
        f"[bold]{machine_id}[/bold]  ([italic]{type_name}[/italic])"
    )


def print_singleton_check(addr_a: int, addr_b: int, same: bool) -> None:
    console.print(f"  hub_a address : [yellow]{addr_a}[/yellow]")
    console.print(f"  hub_b address : [yellow]{addr_b}[/yellow]")
    if same:
        console.print("  [bold green][OK]  SAME object - Singleton confirmed.[/bold green]")
    else:
        console.print("  [bold red][FAIL]  DIFFERENT objects - Singleton broken![/bold red]")


def print_log_tail(entries: List[str]) -> None:
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column("entry", style="dim")
    for entry in entries:
        table.add_row(f"> {entry}")
    console.print(table)


def print_summary() -> None:
    body = (
        "[bold green][OK][/bold green]  Singleton      - FactoryMainframe (one instance enforced)\n"
        "[bold green][OK][/bold green]  Factory Method - MachineryFactory.create(config)\n"
        "[bold green][OK][/bold green]  Adapter        - HydraulicPressAdapter, AnalogFurnaceAdapter\n"
        "[bold green][OK][/bold green]  Facade         - Startup, Shutdown, EmergencyStop, FireDrill, Maintenance\n\n"
        "[bold blue]SOLID principles:[/bold blue]\n"
        "[bold green][OK][/bold green]  DIP  - FactoryMainframe imports only INetworkMachine\n"
        "[bold green][OK][/bold green]  SRP  - each class has exactly one job and one reason to change"
    )
    console.print(Panel(body, title="[bold]SIMULATION COMPLETE[/bold]", border_style="green"))
