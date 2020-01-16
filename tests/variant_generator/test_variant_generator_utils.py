import numpy as np
import pathlib
from PIL import Image
from variant_generator.utils import *


def path_decider():
    if(pathlib.Path().resolve().name == 'variant_generator'):
        json_file = pathlib.Path('resources').resolve() / ('config.json')
        image = pathlib.Path('resources').resolve() / ('Datev_variant.jpg')
    else:
        json_file = pathlib.Path('variant_generator/resources')\
            .resolve() / ('config.json')
        image = pathlib.Path('variant_generator/resources')\
            .resolve() / ('Datev_variant.jpg')
    return json_file, image


def test_imshow():
    json_file, image = path_decider()
    image = Image.open(image)
    image = np.array(image)
    result = imshow(image)
    if not result:
        print('imshow failed')


def test_read_config():
    json_file, image = path_decider()
    config = read_config(json_file)
    if not config:
        print("utils module's read config function failed")


def test_read_image():
    json_file, image = path_decider()
    image_list = []
    image = str(image)
    image_list = read_image(image)
    if not image_list:
        raise AssertionError("utils module's read image function failed")
