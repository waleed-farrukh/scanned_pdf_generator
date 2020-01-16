import numpy as np
import json
import pathlib
import importlib.util
from collections import OrderedDict
from variant_generator.motion_blur import *


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() / ('config.json')
    else:
        json_file = pathlib.Path('variant_generator/resources')\
            .resolve() / ('config.json')
    return json_file


def test_motion_blur_packages_load():
    package_name = ['numpy', 'cv2']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s",
                                 not_installed)


def t_variant_motion_blur_apply(image, config, background_path=None):
    image = np.ones((3, 3, 3))
    motion_blur_params = config['motion_blur']
    motion_blur_generator = MotionBlur(motion_blur_params['dim'],
                                       motion_blur_params['angle_start'],
                                       motion_blur_params['angle_end'],
                                       motion_blur_params['angle_step'],
                                       motion_blur_params['linetype'])
    image = motion_blur_generator.apply(image) if\
        motion_blur_params['apply'] else image
    return image


def test_variant_motion_blur():
    img = np.ones((3, 3, 3))
    json_file = path_decider()
    with open(json_file, 'r') as json_str:
            config = json.load(json_str, object_pairs_hook=OrderedDict)
    image = t_variant_motion_blur_apply(img, config, None)
    result_from_apply = np.ndarray.tolist(image)
    assert (isinstance(image, np.ndarray) and image.ndim == 3) == True, \
        "Variant Generator module Motion Blur's apply function failed "
