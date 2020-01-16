import os
import sys
import pytest
import json
import pathlib
from PIL import Image
from collections import OrderedDict
from variant_generator.spatial_transformer import *
from variant_generator.background import *
from variant_generator.main import _get_random_background
from variant_generator.main import _get_random_background_from_directory


expected_output = [[[52, 64, 92], [52, 64, 92], [52, 64, 92]],
                   [[52, 64, 92], [52, 64, 92], [52, 64, 92]],
                   [[52, 64, 92], [52, 64, 92], [52, 64, 92]]]


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() / ('config.json')
        background = pathlib.Path('resources').resolve() /\
            ('backgrounds/brown.jpg')
        image = pathlib.Path('resources').resolve() / ('Datev_variant.jpg')
    else:
        json_file = pathlib.Path('variant_generator/resources').resolve() /\
            ('config.json')
        background = pathlib.Path('variant_generator/resources').resolve() /\
            ('backgrounds/brown.jpg')
        image = pathlib.Path('variant_generator/resources').resolve() /\
            ('Datev_variant.jpg')
    return json_file, background, image


def t_background():
    json_file, background_path, image = path_decider()
    image = Image.open(image)
    image = np.array(image)
    background_path = str(background_path)
    with open(json_file, 'r') as json_str:
        config = json.load(json_str, object_pairs_hook=OrderedDict)
    if 'rotation' in config and 'perspective' in config:
        rotation_transform_params = config['rotation']
        rotation_transformer = Rotation(
                            rotation_transform_params['rotation_angle_start'],
                            rotation_transform_params['rotation_angle_end'],
                            rotation_transform_params['rotation_angle_step'])\
            if rotation_transform_params['apply'] else None
        perspective_transform_params = config['perspective']
        perspective_transformer = Perspective(
                        perspective_transform_params['perspective_x_start'],
                        perspective_transform_params['perspective_x_end'],
                        perspective_transform_params['perspective_y_start'],
                        perspective_transform_params['perspective_y_end'])\
            if perspective_transform_params['apply'] else None
        spatial_transformer = SpatialTransformer(
                        rotation_transformer,
                        perspective_transformer)
        image, reference = spatial_transformer.apply(image)
    if 'background' in config:
        background_params = config['background']
        if background_params['apply']:
            if background_path is None:
                background_path = _get_random_background()
            elif os.path.isdir(background_path):
                background_path = _get_random_background_from_directory(
                                    background_path)
            if os.path.exists(background_path):
                background = cv2.imread(background_path)
            else:
                sys.exit("Input background file does not exist.")
            background_transformer = Background(background,
                                                background_params['zoom'])
            image = background_transformer.apply(image, reference)
            background_result = image[:3, :3, :3]
    return background_result


@pytest.mark.parametrize("expectedOutput", [expected_output])
def test_background(expectedOutput):
    result_from_background = t_background()
    expectedOutput = (np.array(expectedOutput))
    assert np.array_equal(result_from_background, expectedOutput), \
        "Variant Generation module Background failed."
