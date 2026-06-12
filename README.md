# Industrial Factory Automation Hub

A central command software system for an industrial manufacturing plant. The hub coordinates network-enabled modern robotics alongside decades-old analog machinery, and exposes simple emergency and operational protocols to floor supervisors.

The implementation deliberately mirrors the UML class diagrams: class names, the `MachineStatus` enumeration, the `MachineConfig` value object, the `IMachineFactory` / `IProtocolFacade` interfaces, and the public method names (`start`, `stop`, `getStatus`, `getInstance`, `createMachine`, ...) all match the diagram one-to-one.

---

## Project Structure

```text
factory_automation_hub/
├── src/
│   ├── interfaces/                      # DIP abstractions + value objects
│   │   ├── network_machine.py           # «interface» INetworkMachine
│   │   ├── machine_status.py            # «enumeration» MachineStatus
│   │   ├── machine_config.py            # MachineConfig value object
│   │   ├── factory_interface.py         # «interface» IMachineFactory
│   │   └── facade_interface.py          # «interface» IProtocolFacade
│   ├── machines/
│   │   ├── modern.py                    # RoboticArm, SmartConveyor, LaserCutter
│   │   └── legacy.py                    # LegacyHydraulicPress, AnalogFurnace
│   ├── patterns/
│   │   ├── machinery_factory.py         # MachineryFactory + PlantConfigReader
│   │   ├── adapters.py                  # PLCController + the two adapters
│   │   └── protocols_facade.py          # OperationalFacade
│   ├── core/
│   │   └── mainframe.py                 # «Singleton» FactoryMainframe
│   └── utils/
│       └── display.py                   # Rich terminal formatting
├── data/
│   └── plant_config.json                # Machine fleet configuration
├── docs/                                # UML class diagrams (PDF / PNG)
├── main.py                              # Simulation entry point
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

The driver walks through all four patterns step by step and prints the floor status after each protocol.

---

## Design Patterns

### Singleton — `src/core/mainframe.py`

`FactoryMainframe` overrides `__new__` so only one instance ever exists; `getInstance()` is the intended access point and returns that shared object. This prevents two command centres from issuing conflicting commands. It owns the machine registry (`List[INetworkMachine]`) and an `IMachineFactory`.

### Factory Method — `src/patterns/machinery_factory.py`

`MachineryFactory` (implements `IMachineFactory`) is the **single construction point** for machines. `createMachine(machineType, config)` resolves a `MachineConfig` to the right concrete `INetworkMachine`; `createFromConfig(configFile)` builds the whole fleet. `PlantConfigReader` turns the JSON plant file into typed `MachineConfig` objects via `readConfig()` / `parseEntry()`.

### Adapter — `src/patterns/adapters.py`

`HydraulicPressAdapter` and `AnalogFurnaceAdapter` wrap the two legacy machines and implement `INetworkMachine`. Every call is forwarded through a `PLCController` (a simulated programmable logic controller) and translated into the legacy API. The mainframe calls `start()` / `stop()` and never learns about `activateManually()` or `ignite()`.

### Facade — `src/patterns/protocols_facade.py`

`OperationalFacade` (implements `IProtocolFacade`) gives supervisors one-call protocols. `executeProtocol(name)` dispatches to:

| Method | What it hides |
|---|---|
| `startupSequence()` | Ordered activation: conveyors → furnaces → arms → cutters → presses |
| `shutdownSequence()` | Reverse, graceful power-down |
| `emergencyStop()` | Halt conveyors → open furnace vents → lock arms → kill beams / vent presses |
| `maintenanceMode()` | Graceful shutdown, then flag every machine `MAINTENANCE` |

---

## SOLID Principles

### S — Single Responsibility
Each class has one reason to change: `INetworkMachine` owns the contract, `FactoryMainframe` owns the registry, `MachineryFactory` owns construction, `PlantConfigReader` owns config parsing, `OperationalFacade` owns protocol orchestration, `display.py` owns presentation.

### O — Open/Closed
A new machine type is added by extending `createMachine` (and the config file) — existing machines are untouched. A new protocol is a new method on the facade.

### L — Liskov Substitution
Every `RoboticArm`, `SmartConveyor`, `LaserCutter`, and adapter is fully substitutable wherever an `INetworkMachine` is expected; the mainframe drives them all through the same five methods.

### D — Dependency Inversion
`FactoryMainframe`, `MachineryFactory`, and `OperationalFacade` all depend on the abstractions in `src/interfaces/` (`INetworkMachine`, `IMachineFactory`, `IProtocolFacade`) — never on a concrete machine class.
