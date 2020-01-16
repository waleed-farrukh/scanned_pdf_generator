import cv2
import numpy as np



# Gaussian Blur:
# This class implements Gaussian blur on an image. Gaussian Blur is a way of implementing focus blur.
#
# @Params:- kernel_size_start: Start value for Gaussian filter kernel size range (HAS to be ODD).
#           kernel_size_end: Stop value for Gaussian filter kernel size range.
#           sigma_x_start: Start value for Gaussian filter x_axis standard deviation range
#           sigma_x_end: Start value for Gaussian filter x_axis standard deviation range
#           sigma_y_start: Start value for Gaussian filter y_axis standard deviation range
#           sigma_y_end: Start value for Gaussian filter y_axis standard deviation range
class GaussianBlur:
    def __init__(self, kernel_size_start : int, kernel_size_end : int, sigma_x_start : float, sigma_x_end : float, sigma_y_start : float, sigma_y_end : float):
        assert kernel_size_start % 2 == 1
        self.kernel_size_start = kernel_size_start
        self.kernel_size_end = kernel_size_end
        self.sigma_x_start = sigma_x_start
        self.sigma_x_end = sigma_x_end
        self.sigma_y_start = sigma_y_start
        self.sigma_y_end = sigma_y_end

    # Apply Gaussian Blur with random paramters from given range in config
    # @Input:- img: input image
    def apply(self, img):
        kernel_size = np.random.choice(np.arange(self.kernel_size_start, self.kernel_size_end + 1, 2))
        kernel = (kernel_size, kernel_size)
        sigma_x = np.random.choice(np.arange(self.sigma_x_start, self.sigma_x_end, 0.5))
        sigma_y = np.random.choice(np.arange(self.sigma_y_start, self.sigma_y_end, 0.5))
        return cv2.GaussianBlur(img, kernel, sigma_x, sigma_y)

    # Apply Gaussian Blur with specific params
    # @Params:- img: input image
    #           kernel: Tuple of kernel
    #           sigma_x: Gaussian filter standard deviation x_axis
    #           sigma_y: Gaussian filter standard deviation y_axis
    def apply_specific(self, img, kernel: tuple, sigma_x : float, sigma_y : float):
        return cv2.GaussianBlur(img, kernel, sigma_x, sigma_y)