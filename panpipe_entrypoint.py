import bpy
import sys
import argparse
import os
import logging


dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from panpipe_utils import save_stl, BASE_FLUTE_HEIGHT
from flute_object_builder import FluteAdder

logger = logging.getLogger(__name__)

FLUTE_LENGTH_KEY = "flute_length"
HOLES_KEY = "holes"


def convert_flute_argument_to_dict(flute_argument: str) -> dict:
    flute_parts = flute_argument.split(":", maxsplit=1)
    flute_length = float(flute_parts[0])
    holes_str = flute_parts[1].split(":") if len(flute_parts) > 1 else []
    holes = list(map(float, holes_str))
    return {FLUTE_LENGTH_KEY: flute_length, HOLES_KEY: holes}


def convert_flute_arguments_to_dicts(flute_arguments: list[str]) -> list[dict]:
    return list(map(convert_flute_argument_to_dict, flute_arguments))


def parse_args():
    sys.argv = [__file__] + (sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else [])
    parser = argparse.ArgumentParser()

    parser.add_argument("--sorted", action=argparse.BooleanOptionalAction, default=True, help="sort flutes by length")
    parser.add_argument(
        "-f",
        "--flutes",
        required=True,
        nargs="+",
        type=str,
        help="flutes in the following format <flute_length>:<flute_first_hole_location>:<flute_second_hole_location>... Example: 190:70 120:50",
    )
    parser.add_argument(
        "-o", "--output", type=str, default="panpipe.stl", help="stl file output path. Default panpipe.stl"
    )
    parser.add_argument("-d", "--dimensions", type=float, default=20, help="the x,z dimensions in mm. Default 20")

    return parser.parse_args()


def main(flutes_to_create: list[dict], result_file_path: str, flute_xz_dimensions: float = None):
    flute_xz_dimensions = flute_xz_dimensions or BASE_FLUTE_HEIGHT
    panpipe = None
    for i, flute_to_create in enumerate(flutes_to_create):
        panpipe = FluteAdder(
            flute_number=i,
            flute_length=flute_to_create[FLUTE_LENGTH_KEY],
            xz_dimensions=flute_xz_dimensions,
            holes=flute_to_create[HOLES_KEY],
            panpipe=panpipe,
        ).add_flute_to_panpipe()

    save_stl(object_to_save=panpipe, filepath=result_file_path)


# [523.2511306, 587.32953583, 659.25511383, 698.45646287, 783.99087196, 880.0, 987.76660251]

if __name__ == "__main__":
    args = parse_args()
    sort_flutes = args.sorted
    output_path = args.output
    flute_dimensions = args.dimensions
    flutes = convert_flute_arguments_to_dicts(args.flutes)
    logger.info(f"Starting to create panpipe with {args=}")
    if sort_flutes:
        flutes.sort(reverse=True, key=lambda flute_dict: flute_dict[FLUTE_LENGTH_KEY])
    main(flutes_to_create=flutes, result_file_path=output_path, flute_xz_dimensions=flute_dimensions)
