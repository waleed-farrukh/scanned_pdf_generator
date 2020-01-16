import importlib.util
import pytest
import numpy as np
from PIL import Image
from scipy.signal import convolve2d
from pyblur.DefocusBlur import *


def test_defocus_blur_packages_load():
    package_name = ['numpy', 'PIL', 'scipy', 'skimage', 'math']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s", not_installed)


@pytest.mark.parametrize("test_input,expected", [
    ("[3, 5, 7, 9]", defocusKernelDims)])
def test_defocus_kernel_dims(test_input, expected):
    assert eval(test_input) == expected, \
        "Defocus Blur Parameter defocusKernelDims failed. Must be [3, 5, 7, 9]"


def test_defocus_blur_random_invalid_input_raises_flag():
    with pytest.raises(IOError):
        img = Image.open("test1.jpg").convert('L')
        arr = np.array(img)
        DefocusBlur_random(arr)


def test_defocus_blur():
    img = np.ones((3, 3, 3))
    kernel = [[0., 0.2, 0.], [0.2, 0.2, 0.2], [0., 0.2, 0.]]
    kernel = np.array(kernel)
    convolved = np.zeros(img.shape, dtype=np.uint8)
    for i in range(3):
        img_array = np.array(img[:, :, i], dtype="float32")
        convolved[:, :, i] = convolve2d(img_array,
                                        kernel,
                                        mode='same',
                                        fillvalue=255.0).astype("uint8")
    expected_output_defocus_blur = np.array(convolved)
    result_from_defocus_blur = DefocusBlur(img, 3)
    if(not np.array_equal(expected_output_defocus_blur, result_from_defocus_blur)):
        "Defocus Blur Function Failed"
