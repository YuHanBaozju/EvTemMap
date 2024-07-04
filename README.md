# EvTemMap
Python implementation for "Temporal-Mapping Photography for Event Cameras" -ECCV2024

## Branch Information

- The basic method of EvTemMap (without de-degradation model) is located in the `EvTemMap_basic` branch.

## Overview

The EvTemMap method deployed in this branch converts raw files collected by AT-DVS into TemMat, and performs the most basic time-domain to grayscale-domain conversion, generating grayscale images containing noise degradation.

## Key Features

- **Raw to TemMat Conversion**: Transforms raw event data from AT-DVS into temporal matrices (TemMat).
- **Time to Grayscale Conversion**: Converts the temporal data into grayscale images, albeit with noise degradation.
- **Adjustable Bias Parameter**: The `EvTemMap.py` script includes a `bias` parameter which can be used to adjust the overall brightness of the grayscale images during visualization. Increasing the bias will result in brighter images.

## Requirements

To run the EvTemMap method, ensure you have the following dependencies installed:

- `numpy`
- `opencv-python`
- `metavision sdk` (Please follow the installation guide at [Prophesee Metavision Installation](https://docs.prophesee.ai/stable/installation/windows.html))

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/EvTemMap.git
    cd EvTemMap
    ```

2. Checkout to the `EvTemMap_basic` branch:
    ```bash
    git checkout EvTemMap_basic
    ```

3. Install the required dependencies:
    ```bash
    pip install numpy opencv-python
    ```

4. Follow the instructions in the [Prophesee Metavision Installation Guide](https://docs.prophesee.ai/stable/installation/windows.html) to install the Metavision SDK.

## Usage

To run the EvTemMap conversion:

1. Open the `EvTemMap.py` file.
2. Adjust the `bias` parameter as needed to achieve the desired brightness for your grayscale images.
3. Execute the script:
    ```bash
    python EvTemMap.py --input path_to_raw_file
    ```

## Example

Here is an example command to convert a raw file to a grayscale image:
```bash
python EvTemMap.py --input data/sample.raw --output results/sample_output.png --bias 0.5
