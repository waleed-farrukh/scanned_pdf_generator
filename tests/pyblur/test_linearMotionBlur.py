import importlib.util
import pytest
import numpy as np
from PIL import Image
from scipy.signal import convolve2d
from pyblur.LinearMotionBlur import *


def test_box_blur_packages_load():
    package_name = ['numpy', 'PIL', 'scipy', 'math', 'skimage']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s", not_installed)


@pytest.mark.parametrize("test_input, expected", [
    ("[3, 5, 7, 9]", lineLengths)])
def test_line_lengths(test_input, expected):
    assert eval(test_input) == expected, \
        "Linear Motion Blur Parameter lineLength failed.Must be [3,5,7,9]"


@pytest.mark.parametrize("expected", [(lineTypes)])
def test_line_types(expected):
    a = ['full', 'right', 'left']
    assert a == expected, "Linear Motion Blur Parameter lineTypes failed.\
            Must be ['full', 'right', 'left']"


def test_linear_motion_blur_random_invalid_output_raises_flag():
    with pytest.raises(IOError):
        img = Image.open("test1.jpg").convert('L')
        arr = np.array(img)
        LinearMotionBlur_random(arr)


def test_linear_motion_blur():
    img = np.ones((3, 3, 3))
    kernel = np.zeros((3, 3), dtype=np.float32)
    convolved = np.zeros(img.shape, dtype=np.uint8)
    rr = [1, 0]
    cc = [1, 2]
    kernel[rr, cc] = 1
    normalization_factor = np.count_nonzero(kernel)
    kernel = kernel/normalization_factor
    for i in range(3):
        img_array = np.array(img[:, :, i], dtype="float32")
        convolved[:, :, i] = convolve2d(img_array, kernel,
                                        mode="same",
                                        fillvalue=255.0).astype("uint8")
    expected_output = convolved
    result_from_linear_motion_blur = LinearMotionBlur(img, 3, 45, 'right')
    assert (np.array_equal(result_from_linear_motion_blur, expected_output)) == True, \
        "Linear Motion Blur Function failed."
