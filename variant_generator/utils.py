import json
import matplotlib.pyplot as plt
from cv2 import cvtColor, COLOR_BGR2RGB, imdecode, IMREAD_COLOR, imread
from collections import OrderedDict
import numpy as np
import warnings
import os
from wand.image import Image as WandImage
from wand.color import Color
import sys


# Creates a figure to show image.
def imshow(img, title=None, size=(80,12)):
    plt.figure(figsize=size)
    plt.title(title)
    if img.ndim == 3:
        cv_rgb = cvtColor(img, COLOR_BGR2RGB)
        plt.imshow(cv_rgb)
    else:
        plt.imshow(img,cmap='gray')
    plt.pause(1.0)  # pause a bit so that plots are updated."


# Converts a config .json file to OrderedDict()
# @Input:   jsonfile: input config json file
# @Out:     config in OrderedDict()
def read_config(jsonfile):
    with open(jsonfile, 'r') as json_str:
        config = json.load(json_str, object_pairs_hook=OrderedDict)
        if not 'motion_blur' in config: warnings.warn("Motion Blur params missing.")
        if not 'gaussian_blur' in config: warnings.warn("Gaussian Blur params missing")
        if not 'focus_blur' in config: warnings.warn("Focus Blur params missing.")
        if not 'psf_blur' in config: warnings.warn("PSF Blur params missing.")
        if not 'salt_pepper' in  config: warnings.warn("Salt & Pepper Noise params missing.")
        if not 'rotation' in config or not 'perspective' in config : warnings.warn("Spatial Transformation params missing.")
        if not 'background' in config: warnings.warn("Background params missing.")
        if not 'brightness_change' in config : warnings.warn("Brightness Change params missing.")
        if not 'gamma_spatial' in config: warnings.warn("Gamma Spatial params missing.")
        return config

# Reads Input Image or PDF file
# @Input:   image_path: image or PDF path
# @Out:     list of image pages
def read_image(image_path : str, dpi=300):
    assert os.path.exists(image_path)
    image_list = []
    if image_path.endswith(".pdf"):
        with WandImage(filename=image_path, resolution=dpi) as img:
            for page_img_seq in img.sequence:
                page_img = WandImage(page_img_seq)
                page_img.background_color = Color('white')
                page_img.alpha_channel = 'remove'
                img_buffer = np.asarray(bytearray(page_img.make_blob(format='jpeg')), dtype=np.uint8)
                if img_buffer is not None:
                    image_list.append(imdecode(img_buffer, IMREAD_COLOR))
    elif image_path.endswith(".png") or image_path.endswith(".jpg") or image_path.endswith(".jpeg"):
        image_list.append(imread(image_path, IMREAD_COLOR))
    else:
        sys.exit("Unknown input file format. Accepted inputs: .pdf, .jpg, .jpeg, .png")
    return image_list
