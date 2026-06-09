# Project-4: Industrial Factory Automation Hub

## Overview

A central command software system for an industrial manufacturing plant. The hub coordinates network-enabled modern robotics alongside decades-old analog machinery, and exposes simple emergency and operational protocols to floor supervisors.

---

## Project Structure

```text
factory_hub/
├── driver.py                        # Simulation entry point
├── machines/
│   ├── interfaces.py                # INetworkMachine abstraction
│   ├── modern_machines.py           # RoboticArm, SmartConveyor, LaserCutter
│   └── legacy_machines.py           # LegacyHydraulicPress, AnalogFurnace
├── adapters/
│   └── adapters.py                  # HydraulicPressAdapter, AnalogFurnaceAdapter
├── patterns/
│   ├── factory.py                   # MachineryFactory (Factory Method)
│   └── mainframe.py                 # FactoryMainframe (Singleton)
└── protocols/
    └── protocols.py                 # ProtocolFacade (Facade)
```

---

## How to Run

```bash
python driver.py
```
