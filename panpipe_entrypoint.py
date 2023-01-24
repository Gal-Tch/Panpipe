import bpy
import sys
import argparse
import os
import logging


dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from panpipe_utils import frequency_to_length, save_stl, BASE_FLUTE_HEIGHT
from flute_object_builder import FluteAdder

sys.argv = [__file__] + (sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else [])
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--sorted", action=argparse.BooleanOptionalAction, default=True, help="sort flutes by length")
    parser.add_argument("-f", "--freqs", nargs="+", type=float, help="frequencies to play: 440, 760.3...")
    parser.add_argument("-o", "--output", type=str, default="panpipe.stl", help="stl file output path ")
    parser.add_argument("-d", "--dimensions", type=float, default=None, help="the x,z dimensions in mm")

    return parser.parse_args()


def main(frequencies_to_play: list[float], result_file_path: str, flute_xz_dimensions: float = None):
    flute_lengths = list(map(frequency_to_length, frequencies_to_play))
    flute_xz_dimensions = flute_xz_dimensions or BASE_FLUTE_HEIGHT
    panpipe = None
    for i, flute_length in enumerate(flute_lengths):
        panpipe = FluteAdder(
            flute_number=i, flute_length=flute_lengths[i], xz_dimensions=flute_xz_dimensions, panpipe=panpipe
        ).add_flute_to_panpipe()

    save_stl(object_to_save=panpipe, filepath=result_file_path)


# [523.2511306, 587.32953583, 659.25511383, 698.45646287, 783.99087196, 880.0, 987.76660251]

if __name__ == "__main__":
    args = parse_args()
    sort_flutes = args.sorted
    frequencies_to_play = args.freqs
    output_path = args.output
    flute_dimensions = args.dimensions
    logger.info(f"{args=}")
    if sort_flutes:
        frequencies_to_play = sorted(frequencies_to_play, reverse=True)
    main(frequencies_to_play=frequencies_to_play, result_file_path=output_path, flute_xz_dimensions=flute_dimensions)
