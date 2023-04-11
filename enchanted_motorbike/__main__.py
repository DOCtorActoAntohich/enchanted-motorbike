import argparse

from enchanted_motorbike.controller import run_controller
from enchanted_motorbike.manipulator import ManipulatorServer
from enchanted_motorbike.sensor import run_sensor


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="enchanted_motorbike", description="Run one of the sub-components"
    )

    modules_group = parser.add_mutually_exclusive_group(required=True)
    modules_group.add_argument("--controller", action="store_true")
    modules_group.add_argument("--manipulator", action="store_true")
    modules_group.add_argument("--sensor", action="store_true")

    args = parser.parse_args()

    if args.controller:
        run_controller()

    if args.manipulator:
        ManipulatorServer.run()

    if args.sensor:
        run_sensor()


if __name__ == "__main__":
    main()
