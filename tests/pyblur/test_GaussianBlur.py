import importlib.util
import pytest
import numpy as np
from PIL import Image
from PIL import ImageFilter
from scipy.signal import convolve2d
from pyblur.GaussianBlur import *


def test_gaussian_blur_packages_load():
    package_name = ['numpy', 'PIL']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s", not_installed)


@pytest.mark.parametrize("test_input, expected", [
                        ("[0.5, 1, 1.5, 2, 2.5, 3, 3.5]",
                         gaussianbandwidths)])
def test_gaussian_bandwidths(test_input, expected):
    assert eval(test_input) == expected, \
        "Gaussian Blur parameter gaussianbandwidths failed"


def test_gaussian_blur_random_invalid_output_raises_flag():
    with pytest.raises(IOError):
        img = Image.open("test1").convert('L')
        arr = np.array(img)
        GaussianBlur_random(arr)


def test_gaussian_blur():
    img_array = np.ones((3, 3))
    img = Image.fromarray(img_array, 'RGB')
    expected_output = img.filter(ImageFilter.GaussianBlur(1.5))
    expected_output = list(expected_output.getdata())
    t = GaussianBlur(img, 1.5)
    result_from_gaussian_blur = list(t.getdata())
    assert expected_output == result_from_gaussian_blur, \
        "Gaussian Blur Function failed."
