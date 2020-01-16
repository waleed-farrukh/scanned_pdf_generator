from .motion_blur import *
from .gaussian_blur import *
from .out_of_focus_blur import FocusBlur
from .psf_blur import PSFBlur
from .lighting_variation import BrightnessChange, GammaSpatial
from .noise import SaltPepperNoise
from .spatial_transformer import SpatialTransformer, Rotation, Perspective
from .background import Background
from .utils import read_image
import cv2
import os, sys
import random
from glob import glob
from pkg_resources import resource_filename, resource_listdir



# This function generates a scanned variant of an input image.
# @Input:-  image: Input image. numpy array 2D, type uint8.
#           config: OrderedDict() containing all the variant transformers' params.
#           background_path: file path for the background. Defualt is None.
#                            If background path is None AND config['background']['apply'] is True, then this is
#                            automatically set to a random background from default backgrounds in the package.
def generate_scanned_variant(image, config, background_path = None):

    ## Spatial Transformation
    if 'rotation' in config and 'perspective' in config:
        rotation_transform_params = config['rotation']
        rotation_transformer = Rotation(rotation_transform_params['rotation_angle_start'],
                                        rotation_transform_params['rotation_angle_end'],
                                        rotation_transform_params['rotation_angle_step']) if rotation_transform_params[
            'apply'] else None
        perspective_transform_params = config['perspective']
        perspective_transformer = Perspective(perspective_transform_params['perspective_x_start'],
                                              perspective_transform_params['perspective_x_end'],
                                              perspective_transform_params['perspective_y_start'],
                                              perspective_transform_params['perspective_y_end']) if \
        perspective_transform_params['apply'] else None
        spatial_transformer = SpatialTransformer(rotation_transformer, perspective_transformer)
        image, reference = spatial_transformer.apply(image)

    ## Background
    if 'background' in config:
        background_params = config['background']
        if background_params['apply']:
            if background_path is None:
                background_path = _get_random_background()
            elif os.path.isdir(background_path):
                background_path = _get_random_background_from_directory(background_path)
            if os.path.exists(background_path):
                background = cv2.imread(background_path)
            else:
                sys.exit("Input background file does not exist.")
            background_transformer = Background(background, background_params['zoom'])
            image = background_transformer.apply(image, reference)

    # Motion Blur
    if 'motion_blur' in config:
        motion_blur_params = config['motion_blur']
        motion_blur_generator = MotionBlur(motion_blur_params['dim'], motion_blur_params['angle_start'],
                                           motion_blur_params['angle_end'],
                                           motion_blur_params['angle_step'], motion_blur_params['linetype'])
        image = motion_blur_generator.apply(image) if motion_blur_params['apply'] else image

    # Gaussian Blur
    if 'gaussian_blur' in config:
        gaussian_blur_params = config['gaussian_blur']
        gaussian_blur_generator = GaussianBlur(gaussian_blur_params['kernel_start'],
                                               gaussian_blur_params['kernel_end'],
                                               gaussian_blur_params['sigma_x_start'],
                                               gaussian_blur_params['sigma_x_end'],
                                               gaussian_blur_params['sigma_y_start'],
                                               gaussian_blur_params['sigma_y_end'])
        image = gaussian_blur_generator.apply(image) if gaussian_blur_params['apply'] else image

    # Focus Blur
    if 'focus_blur' in config:
        focus_blur_params = config['focus_blur']
        focus_blur_generator = FocusBlur(focus_blur_params['dim'])
        image = focus_blur_generator.apply(image) if focus_blur_params['apply'] else image

    # PSF Blur
    if 'psf_blur' in config:
        psf_blur_params = config['psf_blur']
        psf_blur_generator = PSFBlur(psf_blur_params['psf_id_start'],
                                     psf_blur_params['psf_id_end'],
                                     psf_blur_params['psf_id_step'])
        image = psf_blur_generator.apply(image) if psf_blur_params['apply'] else image

    ## Noise
    if 'salt_pepper' in config:
        salt_pepper_params = config['salt_pepper']
        salt_pepper_generator = SaltPepperNoise(salt_pepper_params['salt_start'], salt_pepper_params['salt_end'],
                                                salt_pepper_params['salt_step'],
                                                salt_pepper_params['pepper_start'],
                                                salt_pepper_params['pepper_end'],
                                                salt_pepper_params['pepper_step'])
        image = salt_pepper_generator.apply(image) if salt_pepper_params['apply'] else image

    ## Lighting
    if 'brightness_change' in config:
        brightness_change_params = config['brightness_change']
        brightness_change_generator = BrightnessChange(brightness_change_params['brightness_change_start'],
                                             brightness_change_params['brightness_change_end'],
                                             brightness_change_params['brightness_change_step'])
        image = brightness_change_generator.apply(image) if brightness_change_params['apply'] else image

    if 'gamma_spatial' in config:
        gamma_spatial_params = config['gamma_spatial']
        gamma_spatial_generator = GammaSpatial(gamma_spatial_params['gamma_start'], gamma_spatial_params['gamma_end'],
                                               gamma_spatial_params['gamma_step'],
                                               gamma_spatial_params['x_start'], gamma_spatial_params['x_end'],
                                               gamma_spatial_params['x_step'],
                                               gamma_spatial_params['y_start'], gamma_spatial_params['y_end'],
                                               gamma_spatial_params['y_step'])
        image = gamma_spatial_generator.apply(image) if gamma_spatial_params['apply'] else image
    return image


# This function generates a scanned variants for multiple images. Intended to handle a PDF with multiple pages.
# @Input:-  image_path: Path for input image or PDF.
#           config: OrderedDict() containing all the variant transformers' params.
#           background_path: File path for the background. Defualt is None. All images in image_list have this same background.
#                            If background path is None AND config['background']['apply'] is True, then this is
#                            automatically set to a random background from default backgrounds in the package.
# @Out:- List of all image pages. Each element is a numpy array 2D, type uint8
def generate_scanned_variant_multiple_page(image_path, config, background_path = None):
    image_list = read_image(image_path)
    if 'background' in config:
        background_params = config['background']
        if background_params['apply']:
            if background_path is None:
                background_path = _get_random_background()
            elif os.path.isdir(background_path):
                background_path = _get_random_background_from_directory(background_path)
            if not os.path.exists(background_path):
                sys.exit("Input background file does not exist.")
    for i, image in enumerate(image_list):
        image_list[i] = generate_scanned_variant(image, config, background_path)
    return image_list



# Get random background file_path from default backgrounds in the package.
def _get_random_background():
    backgrounds = resource_listdir('variant_generator.resources.backgrounds','.')
    backgrounds = [b for b in backgrounds if b.endswith('jpg')]
    background = random.choice(backgrounds)
    background = resource_filename('variant_generator.resources.backgrounds', background)
    return background


# Get random background file_path from a given directory containing background images (.jpg files).
# @Params:-     backgrounds_dir: Directory containing background .jpg files.
# @Out:-        randomly selected background file_path
def _get_random_background_from_directory(backgrounds_dir):
    backgrounds = glob(f"{backgrounds_dir}/*.jpg")
    if backgrounds:
        background = random.choice(backgrounds)
        return background
    sys.exit("Background directory doesnot contain any image file")



