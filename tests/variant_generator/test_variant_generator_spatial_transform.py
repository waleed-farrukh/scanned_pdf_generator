import numpy as np
import json
import pathlib
from collections import OrderedDict
import importlib.util
from variant_generator.spatial_transformer import *


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() /\
            ('config.json')
    else:
        json_file = pathlib.Path('variant_generator/resources')\
            .resolve() / ('config.json')
    return json_file


def test_focus_blur_packages_load():
    package_name = ['numpy', 'cv2']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s", not_installed)


def t_variant_spatial_transformer_apply(image, config, background_path=None):
        rotation_transform_params = config['rotation']
        rotation_transformer = Rotation(rotation_transform_params[
                                            'rotation_angle_start'],
                                        rotation_transform_params[
                                            'rotation_angle_end'],
                                        rotation_transform_params[
                                            'rotation_angle_step']
                                        ) if rotation_transform_params[
                                        'apply'] else None
        perspective_transform_params = config['perspective']
        perspective_transformer = Perspective(perspective_transform_params[
                                                'perspective_x_start'],
                                              perspective_transform_params[
                                                'perspective_x_end'],
                                              perspective_transform_params[
                                                'perspective_y_start'],
                                              perspective_transform_params[
                                                'perspective_y_end']
                                              ) if(perspective_transform_params
                                                   ['apply']) else None
        spatial_transformer = SpatialTransformer(rotation_transformer,
                                                 perspective_transformer)
        image, reference = spatial_transformer.apply(image)
        return image


def test_variant_focus_blur():
    img = np.ones((3, 3, 3))
    json_file = path_decider()
    with open(json_file, 'r') as json_str:
            config = json.load(json_str, object_pairs_hook=OrderedDict)
    image = t_variant_spatial_transformer_apply(img, config, None)
    assert (isinstance(image, np.ndarray) and image.ndim == 3) == True, \
        "Variant Generator module Motion Blur's apply function failed " 
