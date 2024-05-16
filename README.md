# picasso

A simple python implementation of the below paper for the linear unmixing of spectrally overlapping signal.

[PICASSO allows ultra-multiplexed fluorescence imaging of spatially overlapping proteins without reference spectra measurements](https://www.nature.com/articles/s41467-022-30168-z)

## Installation ##

1. Create a Conda environment with Python 3.9.x.
2. Install Poetry `pip install poetry`.
3. Then simply run `poetry install` inside the project folder.

## How to ##

### Prerequisites ###

* Any number of sequences with overlapping spectra. Ideally, one sequence per laser line. These need to be provided as multichannel stacks, either in 2D or 3D.
* Optionally, cropped versions of the same sequence multichannel stacks, which need to be in 2D. These can also be substituted by or enriched with reference spectral data. These can be used to deduce the unmixing parameters from, because the full-size images can take a long time to calculate.

### Unmixing ###

Open `src/start3D-flex.py` and set the following variables to their appropriate values:
* `rawImages`: List of filenames of the full-size sequences.
* `ds`: Downscaling factor. 4 is the default.
* `useCrop`: Boolean value which dictates whether cropped images will be used to 
* `outputCrop`: Boolean value which dictates whether cropped images are also written to file after unmixing.
* `cropImages`: Same as `rawImages`, but for the cropped images.

## Notes
Images to be unmixed should be smoothed or downsampled to prevent poor performance. Right now the inputs to the functions are assuming CYX format, with the unmixing occurring along the C axis, but this can be extended to specify an arbitrary axis.

## Original repository
https://github.com/biomicrodev/picasso