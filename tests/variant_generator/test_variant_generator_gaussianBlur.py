import numpy as np
import json
import pathlib
import importlib.util
from collections import OrderedDict
from variant_generator.gaussian_blur import *


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() / ('config.json')
    else:
        json_file = pathlib.Path('variant_generator/resources').resolve() /\
            ('config.json')
    return json_file


def test_gaussian_blur_packages_load():
    package_name = ['numpy', 'cv2']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s",
                                 not_installed)


expected_result_from_apply = [
                            [[[1.0, 1.0, 1.0],
                              [1.0, 1.0, 1.0],
                              [1.0, 1.0, 1.0]],
                             [[1.0, 1.0, 1.0],
                              [1.0, 1.0, 1.0],
                              [1.0, 1.0, 1.0]],
                             [[1.0, 1.0, 1.0],
                              [1.0, 1.0, 1.0],
                              [1.0, 1.0, 1.0]]],
                            [[[0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998],
                              [0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998],
                              [0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998]],
                             [[0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998],
                              [0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998],
                              [0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998]],
                             [[0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998],
                              [0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998],
                              [0.9999999999999998,
                               0.9999999999999998,
                               0.9999999999999998]]],
                            [[[0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999],
                              [0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999],
                              [0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999]],
                             [[0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999],
                              [0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999],
                              [0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999]],
                             [[0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999],
                              [0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999],
                              [0.9999999999999999,
                               0.9999999999999999,
                               0.9999999999999999]]]
                          ]


def t_variant_gaussian_blur_apply(image, config, background_path=None):
    gaussian_blur_params = config['gaussian_blur']
    gaussian_blur_generator = GaussianBlur(
                                        gaussian_blur_params['kernel_start'],
                                        gaussian_blur_params['kernel_end'],
                                        gaussian_blur_params['sigma_x_start'],
                                        gaussian_blur_params['sigma_x_end'],
                                        gaussian_blur_params['sigma_y_start'],
                                        gaussian_blur_params['sigma_y_end'])
    result_from_gaussian_blur = gaussian_blur_generator.apply(image)\
        if gaussian_blur_params['apply'] else image
    return result_from_gaussian_blur


def test_variant_gaussian_blur():
    json_file = path_decider()
    img = np.ones((3, 3, 3))
    with open(json_file, 'r') as json_str:
            config = json.load(json_str, object_pairs_hook=OrderedDict)
    image = t_variant_gaussian_blur_apply(img, config, None)
    result_from_apply = np.ndarray.tolist(image)
    assert (result_from_apply in expected_result_from_apply) == True, \
        "Variant Generator module Gaussian Blur's function Apply failed"
