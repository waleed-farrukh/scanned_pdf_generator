
import importlib.util
import pytest
import pickle
import numpy as np
from PIL import Image
from PIL import ImageFilter
from scipy.signal import convolve2d
from pyblur.PsfBlur import *


def test_psf_blur_packages_load():
    package_name = ['numpy', 'PIL', 'scipy', 'pickle']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s", not_installed)


def test_psf_dictionary():
    assert psfDictionary != 0, \
        "PSF Blur component psfDictionary failed"


def test_psf_blur():
    img = np.ones((3, 3, 3))
    kernel = psfDictionary[1]
    convolved = np.zeros(img.shape, dtype=np.uint8)
    for i in range(3):
        img_array = np.array(img[:, :, i], dtype="float32")
        convolved[:, :, i] = convolve2d(img_array, kernel,
                                        mode="same",
                                        fillvalue=255.0).astype("uint8")
    expected_output_psf_blur = convolved
    result_from_psf_blur = PsfBlur(img, 1)
    assert (np.array_equal(expected_output_psf_blur, result_from_psf_blur)) == True, \
        "PSF Blur failed."
