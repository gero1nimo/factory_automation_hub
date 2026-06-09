# factory.py
# MachineryFactory is the only place in the whole project where
# machine objects get constructed. Everything else just calls create()
# and gets back an INetworkMachine — no constructors scattered around.
# To add a new machine type later, you add one entry here and nothing else changes.

from machines.interfaces    import INetworkMachine
from machines.modern_machines import RoboticArm, SmartConveyor, LaserCutter
from machines.legacy_machines import LegacyHydraulicPress, AnalogFurnace
from adapters.adapters        import HydraulicPressAdapter, AnalogFurnaceAdapter


class MachineryFactory:
    """
    Reads a plain config dict and hands back the right machine object.

    Supported 'type' values
    -----------------------
    robotic_arm      ->  RoboticArm
    smart_conveyor   ->  SmartConveyor
    laser_cutter     ->  LaserCutter
    hydraulic_press  ->  LegacyHydraulicPress tucked inside HydraulicPressAdapter
    analog_furnace   ->  AnalogFurnace tucked inside AnalogFurnaceAdapter
    """

    # maps the config string to the builder method responsible for that type
    _BUILDERS: dict = {}

    @classmethod
    def _load_builders(cls) -> None:
        if cls._BUILDERS:
            return   # already loaded, skip
        cls._BUILDERS = {
            "robotic_arm":     cls._build_robotic_arm,
            "smart_conveyor":  cls._build_smart_conveyor,
            "laser_cutter":    cls._build_laser_cutter,
            "hydraulic_press": cls._build_hydraulic_press,
            "analog_furnace":  cls._build_analog_furnace,
        }

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, config: dict) -> INetworkMachine:
        """
        Hand this method a config dict with at minimum 'type' and 'id' keys.
        It figures out which machine to build and returns it ready to register.

        Optional keys per type:
          speed  (float) -- belt speed in m/s for smart_conveyor
          power  (int)   -- wattage for laser_cutter
        """
        cls._load_builders()

        requested = config.get("type", "").lower()

        if requested not in cls._BUILDERS:
            raise ValueError(
                f"MachineryFactory: '{requested}' is not a recognised machine type. "
                f"Available options: {list(cls._BUILDERS.keys())}"
            )

        return cls._BUILDERS[requested](config)

    # ------------------------------------------------------------------
    # Individual builder methods
    # ------------------------------------------------------------------

    @staticmethod
    def _build_robotic_arm(cfg: dict) -> RoboticArm:
        return RoboticArm(unit_id=cfg["id"])

    @staticmethod
    def _build_smart_conveyor(cfg: dict) -> SmartConveyor:
        spd = cfg.get("speed", 0.5)
        return SmartConveyor(unit_id=cfg["id"], belt_speed_mps=spd)

    @staticmethod
    def _build_laser_cutter(cfg: dict) -> LaserCutter:
        pwr = cfg.get("power", 200)
        return LaserCutter(unit_id=cfg["id"], power_watts=pwr)

    @staticmethod
    def _build_hydraulic_press(cfg: dict) -> HydraulicPressAdapter:
        legacy_hw = LegacyHydraulicPress(serial_number=cfg["id"])
        return HydraulicPressAdapter(press=legacy_hw)

    @staticmethod
    def _build_analog_furnace(cfg: dict) -> AnalogFurnaceAdapter:
        legacy_hw = AnalogFurnace(furnace_tag=cfg["id"])
        return AnalogFurnaceAdapter(furnace=legacy_hw)
