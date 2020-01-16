import numpy as np
import json
import pathlib
import importlib.util
from collections import OrderedDict
from PIL import Image
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


def t_variant_gamma_spatial_apply(image, config, background_path=None):
    image = np.array(image)
    gamma_spatial_params = config['gamma_spatial']
    gamma_spatial_generator = GammaSpatial(
                                    gamma_spatial_params['gamma_start'],
                                    gamma_spatial_params['gamma_end'],
                                    gamma_spatial_params['gamma_step'],
                                    gamma_spatial_params['x_start'],
                                    gamma_spatial_params['x_end'],
                                    gamma_spatial_params['x_step'],
                                    gamma_spatial_params['y_start'],
                                    gamma_spatial_params['y_end'],
                                    gamma_spatial_params['y_step'])
    image = gamma_spatial_generator.apply(image)\
        if gamma_spatial_params['apply'] else image
    return image


def test_variant_gamma_spatial():
    json_file, image = path_decider()
    image = Image.open(image)
    with open(json_file, 'r') as json_str:
        config = json.load(json_str, object_pairs_hook=OrderedDict)
    image = t_variant_gamma_spatial_apply(image, config, None)
    assert (isinstance(image, np.ndarray) and image.ndim == 3) == True, \
        "Variant generator module gamma spatial's apply function failed"
