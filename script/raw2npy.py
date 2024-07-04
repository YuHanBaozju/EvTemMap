"""
Metavision RAW to Slice NPY including gray scale picture and moving events.
"""
import numpy as np
from metavision_core.event_io import EventsIterator
import os
import argparse


def raw2npy(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    mv_iterator = EventsIterator(input_path=input_file, delta_t=10 * 10e6)
    event_list = None
    for evs in mv_iterator:
        if event_list is None:
            event_list = evs
        else:
            event_list = np.append(event_list, evs, axis=0)


    np.save(os.path.join(output_dir, 'event.npy'), event_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Metavision RAW file to NPY format")
    parser.add_argument("--input", required=True, help="Input RAW file")
    parser.add_argument("--output", required=True, help="Output directory")

    args = parser.parse_args()

    raw2npy(input_file=args.input, output_dir=args.output)
