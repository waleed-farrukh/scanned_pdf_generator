import numpy as np
import json
import pathlib
from collections import OrderedDict
from variant_generator.psf_blur import *


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() / ('config.json')
    else:
        json_file = pathlib.Path('variant_generator/resources')\
            .resolve() / ('config.json')
    return json_file


expected_result_from_apply = [
                       [
                        [[131, 131, 131],
                         [151, 151, 151],
                         [202, 202, 202]],
                        [[145, 145, 145],
                         [141, 141, 141],
                         [172, 172, 172]],
                        [[187, 187, 187],
                         [158, 158, 158],
                         [157, 157, 157]]
                       ], [
                            [[144, 144, 144],
                             [141, 141, 141],
                             [144, 144, 144]],
                            [[136, 136, 136],
                             [120, 120, 120],
                             [123, 123, 123]],
                            [[112, 112, 112],
                             [97,  97,  97],
                             [131, 131, 131]]
                          ], [
                                [[30, 30, 30],
                                 [15, 15, 15],
                                 [30, 30, 30]],
                                [[15, 15, 15],
                                 [1,  1,  1],
                                 [15, 15, 15]],
                                [[30, 30, 30],
                                 [15, 15, 15],
                                 [30, 30, 30]]
                             ], [
                                    [[201, 201, 201],
                                     [201, 201, 201],
                                     [201, 201, 201]],
                                    [[201, 201, 201],
                                     [201, 201, 201],
                                     [201, 201, 201]],
                                    [[201, 201, 201],
                                     [201, 201, 201],
                                     [202, 202, 202]]
                                ]
                          ]


def t_variant_psf_blur_apply_specific(img, config, background_path=None):
    if 'psf_blur' in config:
        psf_blur_params = config['psf_blur']
        psf_blur_generator = PSFBlur(psf_blur_params['psf_id_start'],
                                     psf_blur_params['psf_id_end'],
                                     psf_blur_params['psf_id_step'])
        image = psf_blur_generator.apply_specific(img, 1)\
            if psf_blur_params['apply'] else image
        return image


def t_variant_psf_blur_apply(img, config, background_path=None):
    if 'psf_blur' in config:
        psf_blur_params = config['psf_blur']
        psf_blur_generator = PSFBlur(psf_blur_params['psf_id_start'],
                                     psf_blur_params['psf_id_end'],
                                     psf_blur_params['psf_id_step'])
        image = psf_blur_generator.apply(img) \
            if psf_blur_params['apply'] else image
        return image


def test_variant_psf_blur():
    img = np.ones((3, 3, 3))
    json_file = path_decider()
    with open(json_file, 'r') as json_str:
            config = json.load(json_str, object_pairs_hook=OrderedDict)
    image = t_variant_psf_blur_apply_specific(img, config, None)
    result_from_apply_specific = np.ndarray.tolist(image)
    assert (result_from_apply_specific in expected_result_from_apply) == True, \
        "Variant Generator module PSF Blur's function \
        Apply_specific failed"
    img = np.ones((3, 3, 3))
    image = t_variant_psf_blur_apply(img, config, None)
    result_from_apply = np.ndarray.tolist(image)
    assert (result_from_apply in expected_result_from_apply) == True, \
        "Variant Generator module PSF Blur's function \
        Apply_specific failed"
