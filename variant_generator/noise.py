import numpy as np


# Salt and Pepper Noise:
# This class implements Salt and Pepper grain noise that comes with a dirty scanner.
# @Params:- salt_rate_start: Start percentage value for salt grain noise range
#           salt_rate_end: Stop percentage value for salt grain noise range
#           salt_rate_step: Percentage value step for salt grain noise range
#           pepper_rate_start: Start percentage value for pepper grain noise range
#           pepper_rate_end: Stop percentage value for pepper grain noise range
#           pepper_rate_step: Percentage step value for pepper grain noise range
class SaltPepperNoise:
    def __init__(self, salt_rate_start : float, salt_rate_end : float, salt_rate_step : float, pepper_rate_start : float, pepper_rate_end : float, pepper_rate_step : float):
        self.salt_rate_start = salt_rate_start
        self.salt_rate_end = salt_rate_end
        self.salt_rate_step = salt_rate_step
        self.pepper_rate_start = pepper_rate_start
        self.pepper_rate_end = pepper_rate_end
        self.pepper_rate_step = pepper_rate_step

    def _get_random_salt_rate(self):
        return np.random.choice(np.arange(self.salt_rate_start, self.salt_rate_end, self.salt_rate_step)) if self.salt_rate_step > 0. else self.salt_rate_start

    def _get_random_pepper_rate(self):
        return np.random.choice(np.arange(self.pepper_rate_start, self.pepper_rate_end, self.pepper_rate_step)) if self.pepper_rate_step> 0. else self.pepper_rate_start

    # Apply Salt and Pepper Noise with random paramters from given range in config
    # @Input:- img: input image
    # @Out:-   Output image
    def apply(self, img : np.array):
        image_noise = np.copy(img)
        salt_rate = self._get_random_salt_rate()
        pepper_rate = self._get_random_pepper_rate()
        image_noise = image_noise.reshape(-1, 3) # assuming colored image
        salt_quantity = int(np.ceil(salt_rate * image_noise.shape[0]))
        pepper_quantity = int(np.ceil(pepper_rate * image_noise.shape[0]))
        salt_coords = np.random.choice(np.arange(0, image_noise.shape[0]), size = salt_quantity)
        pepper_coords = np.random.choice(np.arange(0, image_noise.shape[0]), size = pepper_quantity)
        image_noise[salt_coords] = (255, 255, 255)
        image_noise[pepper_coords] = (0, 0, 0)
        return image_noise.reshape(img.shape)



