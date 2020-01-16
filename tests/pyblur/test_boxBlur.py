import importlib.util
import pytest
import numpy as np
from scipy.signal import convolve2d
from PIL import Image
from pyblur.BoxBlur import *


def test_box_blur_packages_load():
    package_name = ['numpy', 'PIL', 'scipy']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s", not_installed)


@pytest.mark.parametrize("test_input,expected", [
                        ("[3,5,7,9]", boxKernelDims)])
def test_box_kernel_dims(test_input, expected):
    assert eval(test_input) == expected, \
        "Box Blur Parameter boxKernelDims failed.Must be [3,5,7,9]"


def test_box_blur_random_invalid_output_raises_flag():
    with pytest.raises(IOError):
        img = Image.open("test1.jpg").convert('L')
        arr = np.array(img)
        BoxBlur_random(arr)


def test_box_blur():
    img_array = np.ones((3, 3))
    kernel = np.ones((3, 3), dtype=np.float32)
    normalization_factor = np.count_nonzero(kernel)
    kernel = kernel / normalization_factor
    expected_output = convolve2d(img_array, kernel, mode='same',
                                fillvalue=255.0).astype("uint8")
    flatten = lambda l: [item for sublist in l for item in sublist]
    expected_output = flatten(expected_output)
    t = BoxBlur(img_array, 3)
    result_from_box_blur = list(t.getdata())
    assert result_from_box_blur == expected_output, "BoxBlur Function failed."
