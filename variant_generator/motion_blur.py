from pyblur import LinearMotionBlur, LinearMotionBlur_random
import numpy as np




# Motion Blur:
# This class implements motion blur on an image. Motion blur is sometimes caused when a object/camera/scanner is moved right before capture.
#
# @Params:- dim: List of line lengths (3, 7, 5, 9)
#           angle_start: Starting angle in degrees for blur angle range
#           angle_end: End angle in degrees for blur angle range
#           angle_step: Angle step size in degrees for blur angle range
#           linetype: List of blur line type ("full", "left", "right")
class MotionBlur:
    def __init__(self, dim : list, angle_start : int, angle_end : int, angle_step : int, linetype : list):
        self.dim = dim #list
        self.angle_start = angle_start
        self.angle_end = angle_end
        self.angle_step = angle_step
        self.angles = np.arange(angle_start, angle_end, angle_step) if angle_step > 0 else angle_start
        self.linetype = linetype #list

    def __str__(self):
        return f"dim={self.dim}, angle={self.angle}, linetype={self.linetype}"

    # Apply Motion Blur with random paramters from given range in config
    # @Input:- img: input image
    # @Out:-   Output image
    def apply(self,img):
        dim = np.random.choice(self.dim)
        angle = np.random.choice(self.angles)
        linetype = np.random.choice(self.linetype)
        return LinearMotionBlur(img, dim, angle, linetype)

    # Apply Motion Blur with specific params
    # @Params:- img: input image
    #           dim: line length
    #           angle: blur angle in degree
    #           linetype: blur line type
    # @Out:-    Output image
    def apply_specific(self,img, dim, angle, linetype):
        assert isinstance(dim,int)
        assert isinstance(linetype,str)
        return LinearMotionBlur(img, dim, angle, linetype)

    # Apply Motion Blur with random params
    # @Input:- img: input image
    # @Out:-   Output image
    def apply_random(self,img):
        return LinearMotionBlur_random(img)

