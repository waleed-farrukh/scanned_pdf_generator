from variant_generator.main import generate_scanned_variant, generate_scanned_variant_multiple_page
from variant_generator.utils import read_config, imshow
import cv2
import click
import os, sys
from wand.image import Image as WandImage
from wand.color import Color
import numpy as np
from pkg_resources import resource_filename


@click.command()
@click.argument('inp', type=click.Path(exists=True))
@click.option('--config', '-c', default = resource_filename('config', 'config.json'), help='config file for variant parameters')
@click.option('--out', '-o', help='output image path')
@click.option('--background', '-b', help='(Optional) background image path or directory')
def run(inp, config, out = None, background = None):
    assert os.path.exists(inp)
    assert os.path.exists(config)
    config = read_config(config)
    image_name, ext = os.path.splitext(inp)

    image_list = generate_scanned_variant_multiple_page(inp, config, background)
    for i, output_image in enumerate(image_list):
        out_page = f"{os.path.basename(image_name)}_variant.jpg" if out is None else out

        out_page = f"{os.path.splitext(out_page)[0]}_{i}.jpg" if len(image_list) > 1 else out_page
        cv2.imwrite(out_page, output_image)



