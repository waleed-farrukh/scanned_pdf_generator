import numpy as np
import json
import pathlib
import importlib.util
from collections import OrderedDict
from variant_generator.noise import *


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() / ('config.json')
    else:
        json_file = pathlib.Path('variant_generator/resources')\
            .resolve() / ('config.json')
    return json_file


def test_psf_blur_packages_load():
    package_name = ['numpy']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages \
                                 failed to load: %s",
                                 not_installed)


def test_variant_noise_blur():
    img = np.ones((3, 3, 3))
    json_file = path_decider()
    with open(json_file, 'r') as json_str:
            config = json.load(json_str, object_pairs_hook=OrderedDict)
    image = np.ones((3, 3, 3))
    salt_pepper_params = config['salt_pepper']
    salt_pepper_generator = SaltPepperNoise(
                                            salt_pepper_params['salt_start'],
                                            salt_pepper_params['salt_end'],
                                            salt_pepper_params['salt_step'],
                                            salt_pepper_params['pepper_start'],
                                            salt_pepper_params['pepper_end'],
                                            salt_pepper_params['pepper_step']
                                          )
    image = salt_pepper_generator.apply(image)\
        if salt_pepper_params['apply'] else image
    assert (isinstance(image, np.ndarray) and image.ndim == 3) == True, \
        "Variant Generator module Noise Blur's apply function failed"
