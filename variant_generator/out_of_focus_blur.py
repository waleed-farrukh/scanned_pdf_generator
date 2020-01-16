import numpy as np
from pyblur.DefocusBlur import DefocusBlur



# Out-of-Focus Blur:
# This class implements out-of-focus blur on an image.
# @ Params:- dim: List of Out-of-focus Kernel dimensions (3, 5, 7, 9)
class FocusBlur:
    def __init__(self, dim : list):
        self.dim = dim

    # Apply Out-of-focus Blur with random paramters from given list in config
    # @Input:- img: input image
    # @Out:-   Output image
    def apply(self, img):
        dim = np.random.choice(self.dim)
        return DefocusBlur(img, dim)

    # Apply Out-of-focus Blur with specific params
    # @Input:- img: input image
    #           dim: kernel dimension
    # @Out:-    Output image
    def apply_specific(self, img, dim : int):
        return DefocusBlur(img, dim)