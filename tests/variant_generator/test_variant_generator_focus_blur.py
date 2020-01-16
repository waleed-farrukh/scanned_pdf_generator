import numpy as np
import json
import pathlib
import importlib.util
from collections import OrderedDict
from variant_generator.out_of_focus_blur import *


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() / ('config.json')
    else:
        json_file = pathlib.Path('variant_generator/resources').resolve() /\
            ('config.json')
    return json_file


def test_focus_blur_packages_load():
    package_name = ['numpy']
    not_installed = []
    for package in package_name:
        spec = importlib.util.find_spec(package)
        if spec is None:
            not_installed.append(package)
    assert not_installed == [], ("Packages failed to load: %s",
                                 not_installed)


expected_result_from_apply = [
                            [[[221, 221, 221],
                              [221, 221, 221],
                              [221, 221, 221]],
                             [[221, 221, 221],
                              [221, 221, 221],
                              [221, 221, 221]],
                             [[221, 221, 221],
                              [221, 221, 221],
                              [221, 221, 221]]],
                            [[[158, 158, 158],
                              [146, 146, 146],
                              [158, 158, 158]],
                             [[146, 146, 146],
                              [146, 146, 146],
                              [146, 146, 146]],
                             [[158, 158, 158],
                              [146, 146, 146],
                              [158, 158, 158]]],
                            [[[102, 102, 102],
                              [51, 51, 51],
                              [102, 102, 102]],
                             [[51, 51, 51],
                              [1, 1, 1],
                              [51, 51, 51]],
                             [[102, 102, 102],
                              [51, 51, 51],
                              [102, 102, 102]]],
                            [[[204, 204, 204],
                              [204, 204, 204],
                              [204, 204, 204]],
                             [[204, 204, 204],
                              [204, 204, 204],
                              [204, 204, 204]],
                             [[204, 204, 204],
                              [204, 204, 204],
                              [204, 204, 204]]]]


def t_variant_focus_blur_apply(image, config, background_path=None):
    image = np.ones((3, 3, 3))
    focus_blur_params = config['focus_blur']
    focus_blur_generator = FocusBlur(focus_blur_params['dim'])
    image = focus_blur_generator.apply(image)\
        if focus_blur_params['apply'] else image
    return image


def test_variant_focus_blur():
    json_file = path_decider()
    img = np.ones((3, 3, 3))
    with open(json_file, 'r') as json_str:
            config = json.load(json_str, object_pairs_hook=OrderedDict)
    image = t_variant_focus_blur_apply(img, config, None)
    result_from_apply = np.ndarray.tolist(image)
    assert (result_from_apply in expected_result_from_apply) == True, "Variant\
        Generator module Focus Blur's function Apply failed"
