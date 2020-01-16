import numpy as np
from pyblur.PsfBlur import PsfBlur



# Point Spread Function Blur:
# This class implements PSF blur on an image.
# @ Params:- psf_id_start: int [0-99]
#            psf_id_end: int [0-99] && >= psf_id_start
#            psf_id_step: int
class PSFBlur:
    def __init__(self, psf_id_start : int, psf_id_end : int, psf_id_step : int):
        self.psf_id_start = psf_id_start
        self.psf_id_end = psf_id_end
        self.psf_id_step = psf_id_step

    # Apply Out-of-focus Blur with random paramters from given list in config
    # @Input:- img: input image
    # @Out:-   Output image
    def apply(self, img):
        psf_id = np.random.choice(np.arange(self.psf_id_start, self.psf_id_end, self.psf_id_step) if self.psf_id_step> 0 else self.psf_id_start)
        return PsfBlur(img, psf_id)

    # Apply Out-of-focus Blur with specific params
    # @Input:- img: input image
    #           dim: kernel dimension
    # @Out:-    Output image
    def apply_specific(self, img, psf_id : int):
        return PsfBlur(img, psf_id)