# Industrial Factory Automation Hub

A central command software system for an industrial manufacturing plant. The hub coordinates network-enabled modern robotics alongside decades-old analog machinery, and exposes simple emergency and operational protocols to floor supervisors.

---

## Project Structure

```text
factory_automation_hub/
├── src/
│   ├── core/
│   │   └── mainframe.py              # Singleton: FactoryMainframe
│   ├── interfaces/
│   │   └── network_machine.py        # DIP: INetworkMachine (abc)
│   ├── machines/
│   │   ├── modern.py                 # RoboticArm, SmartConveyor, LaserCutter
│   │   └── legacy.py                 # LegacyHydraulicPress, AnalogFurnace
│   ├── patterns/
│   │   ├── machinery_factory.py      # Factory Method
│   │   ├── adapters.py               # Adapter
│   │   └── protocols_facade.py       # Facade
│   └── utils/
│       └── display.py                # Rich terminal formatting
├── data/
│   └── plant_config.json             # Machine fleet configuration
├── docs/
│   └── UML_Class_Diagram.puml        # PlantUML source — render to PNG
├── main.py                           # Simulation entry point
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

---

## Design Patterns

### Singleton — `src/core/mainframe.py`

`FactoryMainframe` overrides `__new__` to ensure only one instance ever exists. A second call to `FactoryMainframe()` returns the exact same object. This prevents two command centres from issuing conflicting commands to the same floor.

### Factory Method — `src/patterns/machinery_factory.py`

`MachineryFactory.create(config)` is the **single construction point** for all machine objects. Callers pass a plain dict with `type` and `id` keys; the factory resolves which concrete class to build and returns an `INetworkMachine`. Adding a new machine type requires touching only the `_BUILDERS` dict — nothing else changes.

### Adapter — `src/patterns/adapters.py`

`HydraulicPressAdapter` and `AnalogFurnaceAdapter` wrap the two legacy machines (`LegacyHydraulicPress`, `AnalogFurnace`) so the mainframe can treat them as `INetworkMachine`. The mainframe calls `activate()` / `emergency_stop()` and never learns about `plc_pressurize()` or `relay_ignite()`.

### Facade — `src/patterns/protocols_facade.py`

`ProtocolFacade` gives floor supervisors five plain commands:

| Method | What it hides |
|---|---|
| `startup_sequence()` | Ordered activation: conveyors → furnaces → arms → cutters → presses |
| `shutdown_sequence()` | Reverse shutdown: presses → cutters → arms → furnaces → conveyors |
| `emergency_stop()` | Priority stop with keyword-based ordering |
| `fire_drill_protocol()` | Emergency stop + full status readout |
| `maintenance_mode()` | Graceful shutdown + full diagnostic |

---

## SOLID Principles

### S — Single Responsibility Principle

Every class has exactly one reason to change:

- `INetworkMachine` — owns only the machine contract (`src/interfaces/network_machine.py`)
- `FactoryMainframe` — owns only registry management and command routing (`src/core/mainframe.py`)
- `MachineryFactory` — owns only object construction (`src/patterns/machinery_factory.py`)
- `ProtocolFacade` — owns only multi-step protocol orchestration (`src/patterns/protocols_facade.py`)
- `display.py` — owns only terminal formatting (`src/utils/display.py`)

### O — Open/Closed Principle

`MachineryFactory._BUILDERS` is a dict that can be extended with new machine types without modifying any existing builder method — open for extension, closed for modification. Similarly, adding a new protocol to `ProtocolFacade` leaves all existing protocols untouched.

### D — Dependency Inversion Principle

`FactoryMainframe` holds `Dict[str, INetworkMachine]` and calls only abstract methods defined in `src/interfaces/network_machine.py`. It depends on the **abstraction**, never on `RoboticArm`, `HydraulicPressAdapter`, or any other concrete class. `ProtocolFacade` follows the same rule — it only talks to the mainframe, never to individual machines directly.
