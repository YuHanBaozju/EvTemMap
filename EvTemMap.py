"""
This file implements the EvTemMap method for mapping time to grayscale.

Requirements:
- numpy
- opencv-python
- metavision sdk (please follow the installation guide at https://docs.prophesee.ai/stable/installation/windows.html)

@article{bao2024temporal,
  title={Temporal-Mapping Photography for Event Cameras},
  author={Bao, Yuhan and Sun, Lei and Ma, Yuqin and Wang, Kaiwei},
  journal={arXiv preprint arXiv:2403.06443},
  year={2024}
}

MIT License

Copyright (c) 2024 [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
from metavision_core.event_io import EventsIterator
import os
import cv2
import argparse

def get_TemMat(pic_events):
    pic = np.zeros((720, 1280), np.int32)
    for evs in pic_events:
        if evs["p"] == 1 and pic[evs["y"], evs["x"]] == 0:
            pic[evs["y"], evs["x"]] = evs["t"]
    return pic

def raw2npy(dataset):
    if not os.path.exists(dataset[:-4] + '/pic'):
        os.makedirs(dataset[:-4] + '/pic')

    mv_iterator = EventsIterator(input_path=dataset, delta_t=10 * 10e6)
    event_list = None
    for evs in mv_iterator:
        if event_list is None:
            event_list = evs
        else:
            event_list = np.append(event_list, evs, axis=0)

    np.save(dataset[:-4]+'/event.npy', event_list)
    return event_list

def time2gray(pic, open_time, bias=150e3):
    pic = pic.astype(np.float32)
    pic_avg = pic[np.nonzero(pic)].mean()
    pic_std = pic[np.nonzero(pic)].std()

    pic[np.where(pic == 0)] = np.nanmax(pic)

    # The hot pixel list of our EVK4 device. obtained by calibration.
    # hot pixel removal
    pic[64][413] = pic_avg
    pic[665][806] = pic_avg
    pic[137][1271] = pic_avg
    pic[236][1270] = pic_avg
    pic[236][1271] = pic_avg

    pic = pic - open_time + bias

    pic = pic / np.max(pic)

    # time-to-gray conversion

    pic = 1 / pic**2


    # Normalization and gamma adjustment for better visualization
    pic = (pic - np.min(pic)) / (np.max(pic) - np.min(pic))
    pic = pic**1.5

    return pic

def main(input_file, bias):
    event_npy = raw2npy(dataset=input_file)

    time_pic = get_TemMat(event_npy)
    np.save(input_file[:-4]+'/pic.npy', time_pic)
    time_pic = np.load(input_file[:-4]+'/pic.npy')

    img_pic = time2gray(time_pic, open_time=0, bias=bias)

    cv2.imwrite(input_file[:-4] + '/pic/pic.png', (img_pic*(2**16-1)).astype('uint16'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Metavision RAW file to NPY format and generate grayscale "
                                                 "images")
    parser.add_argument("--input", required=True, help="Input RAW file")
    parser.add_argument("--bias", type=float, default=150e3, help="Adjust the bias to adapt the visualization to "
                                                                  "different brightness scenes, and increase the bias"
                                                                  " to make the visualization brighter.")
    args = parser.parse_args()
    main(args.input, args.bias)
