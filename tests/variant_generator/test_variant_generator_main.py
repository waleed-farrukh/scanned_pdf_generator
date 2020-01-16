import os
import sys
import json
import pathlib
import numpy as np
from PIL import Image
from collections import OrderedDict
from variant_generator.main import _get_random_background_from_directory
from variant_generator.main import _get_random_background
from variant_generator.main import generate_scanned_variant_multiple_page


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


def background_dir_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        background_dir = pathlib.Path('resources').resolve() /\
            ('backgrounds')
    else:
        background_dir = pathlib.Path('variant_generator/resources/backgrounds')\
        .resolve()
    return background_dir


def test_get_random_background_from_directory():
    background_dir = background_dir_decider()
    background_dir = str(background_dir)
    result = _get_random_background_from_directory(background_dir)
    assert os.path.exists(result), \
        "Variant Generator module main's function\
         _get_random_background_from directory failed"


def test_get_random_background():
    result = _get_random_background()
    assert os.path.exists(result), \
        "Variant Generator module main's function\
        _get_random_background failed"


def test_generate_scanned_multi_page():
    json_file, background_path, image_path = path_decider()
    background_path = str(background_path)
    with open(json_file, 'r') as json_str:
        config = json.load(json_str, object_pairs_hook=OrderedDict)
    image_path = str(image_path)
    a = generate_scanned_variant_multiple_page(image_path,
                                               config,
                                               background_path)
    if not a:
        raise AssertionError("generate scanned multipage failed")
