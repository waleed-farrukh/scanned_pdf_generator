import numpy as np
import cv2



# Gamma Change:
# This class varies the Gamma (luminance) value of an image
# @Params:- gamma_start: Start value for Gamma range
#           gamma_end: Stop value for Gamma range
#           gamma_step: Step value for Gamma range
class GammaChange:
    def __init__(self, gamma_start : float, gamma_end : float, gamma_step : float):
        self.gamma_start = gamma_start
        self.gamma_end = gamma_end
        self.gamma_step = gamma_step

    def _get_random_gamma(self):
        return np.random.choice(np.arange(self.gamma_start, self.gamma_end, self.gamma_step)) if self.gamma_step > 0 else self.gamma_start

    # Apply Gamma Change with random paramters from given range in config
    # @Input:- img: input image
    # @Out:-   Output image
    def apply(self, img):
        gamma = self._get_random_gamma()
        inv_gamma = 1. / gamma
        lookup_table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(img, lookup_table)


# Brightness Change:
# This class increases or decreases the Brightness of an image
# @Params:- brightness_change_start: Start value for Brightness difference range (Can be -ve and +ve)
#           brightness_change_end: Stop value for Brightness difference range
#           brightness_change_step: Step value for Brightness difference range
class BrightnessChange:
    def __init__(self, brightness_change_start : int, brightness_change_end : int, brightness_change_step : int):
        self.brightness_change_start = brightness_change_start
        self.brightness_change_end = brightness_change_end
        self.brightness_change_step = brightness_change_step

    def _get_random_brightness_change(self):
        return np.random.choice(np.arange(self.brightness_change_start, self.brightness_change_end, self.brightness_change_step)) if self.brightness_change_step > 0. else self.brightness_change_start

    # Apply Brightness Change with random difference from given range in config
    # @Input:- img: input image
    # @Out:-   Output image
    def apply(self, img):
        image_brightness_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype('float')
        brightness_change = self._get_random_brightness_change()
        image_brightness_hsv[image_brightness_hsv[:, :, 2] >= 255 - brightness_change, 2] = 255 # limiting upper bound to 255
        image_brightness_hsv[image_brightness_hsv[:, :, 2] <= 0 - brightness_change, 2] = 0 # limitng lower bound to 0
        image_brightness_hsv[np.logical_and((image_brightness_hsv[:, :, 2] > 0 - brightness_change),
                                (image_brightness_hsv[:, :, 2] < 255 - brightness_change)), 2] += brightness_change
        image_brightness_hsv = np.uint8(image_brightness_hsv)
        return cv2.cvtColor(image_brightness_hsv, cv2.COLOR_HSV2BGR)

# Gamma Spatial Change:
# This class implements a Light bulb effect on an image
# @Params:- gamma_start: Start value for Light bulb intensity range
#           gamma_end: Stop value for Light bulb intensity range
#           gamma_step: Step value for Light bulb intensity range
#           x_start: Start value for Light bulb x position range
#           x_end_step: Step value for Light bulb x position range
#           x_step: Stop value for Light bulb x position range
#           y_start: Step value for Light bulb y position range
#           y_end: Stop value for Light bulb y position range
#           y_step: Step value for Light bulb y position range
class GammaSpatial:
    def __init__(self, gamma_start : float, gamma_end : float, gamma_step : float, x_start : float, x_end : float, x_step : float, y_start : float, y_end : float, y_step : float):
        self.gamma_start = gamma_start
        self.gamma_end = gamma_end
        self.gamma_step = gamma_step
        self.x_start = x_start
        self.x_end = x_end
        self.x_step = x_step
        self.y_start = y_start
        self.y_end = y_end
        self.y_step = y_step

    def _get_random_bulb_parameters(self):
        gamma = np.random.choice(np.arange(self.gamma_start, self.gamma_end, self.gamma_step)) if self.gamma_step > 0. else self.gamma_start
        x_r = np.random.choice(np.arange(self.x_start, self.x_end, self.x_step)) if self.x_step > 0. else self.x_start
        y_r = np.random.choice(np.arange(self.y_start, self.y_end, self.y_step)) if self.y_step > 0. else self.y_start
        return gamma, x_r, y_r

    # Apply Gamma Spatial Change with random params from given range in config
    # @Input:- img: input image
    # @Out:-   Output image
    def apply(self, img):
        img = np.copy(img)
        #create a light bulb mask
        mask = np.ones(img.shape, dtype = np.uint8) * 255
        gamma, x_r, y_r = self._get_random_bulb_parameters()
        h, w = mask.shape[:2]
        cv_hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV).astype(float)

        lut = np.fromfunction(lambda j, i: ((i / float(w) - x_r) ** 2 + (j / float(h) - y_r) ** 2) ** gamma, (h, w),
                              dtype=float)
        lut = np.repeat(lut[:, :, np.newaxis], 3, axis=2)

        cv_hsv[:, :, :] = ((cv_hsv[:, :, :] / 255) * (lut[:, :, :])) * 255
        mask = np.uint8(cv_hsv)
        mask = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        mask = 255 - mask

        #blend with image
        return self._alpha_blend(img, mask, 0.7)

    # Blend two images together
    # @Params:- alpha: blend ratio
    def _alpha_blend(self, image1, image2, alpha):
        if image1.ndim == 2 and image2.ndim == 3:
            image1 = np.repeat(image1[:, :, np.newaxis], 3, axis=2).copy()
        if image2.ndim == 2 and image1.ndim == 3:
            image2 = np.repeat(image2[:, :, np.newaxis], 3, axis=2)
        res = cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)
        return res
