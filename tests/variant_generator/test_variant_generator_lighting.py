import numpy as np
import json
import pathlib
import importlib.util
from PIL import Image
from collections import OrderedDict
from variant_generator.lighting_variation import *


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() / ('config.json')
        image = pathlib.Path('resources').resolve() / ('Datev_variant.jpg')
    else:
        json_file = pathlib.Path('variant_generator/resources').resolve() /\
            ('config.json')
        image = pathlib.Path('variant_generator/resources').resolve() /\
            ('Datev_variant.jpg')
    return json_file, image


def test_lighting_packages_load():
    package_name = ['numpy', 'cv2']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s",
                                 not_installed)


def t_variant_lighting_apply(image, config, background_path=None):
    image = np.array(image)
    brightness_change_params = config['brightness_change']
    brightness_change_generator = BrightnessChange(
                                 brightness_change_params[
                                     'brightness_change_start'],
                                 brightness_change_params[
                                     'brightness_change_end'],
                                 brightness_change_params[
                                     'brightness_change_step'])
    image = brightness_change_generator.apply(image)\
        if brightness_change_params['apply'] else image
    return image


def test_variant_lighting():
    json_file, image = path_decider()
    image = Image.open(image)
    with open(json_file, 'r') as json_str:
            config = json.load(json_str, object_pairs_hook=OrderedDict)
    image = t_variant_lighting_apply(image, config, None)
    assert (isinstance(image, np.ndarray) and image.ndim == 3) == True, \
        "Variant Generator module Lighting Variation's apply function failed "
