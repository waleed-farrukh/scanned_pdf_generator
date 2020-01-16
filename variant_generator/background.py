import numpy as np
import cv2
from .utils import imshow


# Background:
# This class merges a transformed image onto a background with random translation.
#
# @Input:-  background_image: Background image, 2D numpy array, type uint8
# @Out:-    Final Image with background.
class Background:
    def __init__(self, background_image : np.array, zoom : float = 0.1):
        zoom = 0.0 if zoom < 0 else zoom
        self.zoom = zoom
        self.background_image = background_image

    def _generate_random_anchor(self, document_image):
        offset_x = np.random.choice(np.arange(0, self.background_image.shape[1] - document_image.shape[1], int(self.background_image.shape[1]*0.0025)))
        offset_y = np.random.choice(np.arange(0, self.background_image.shape[0] - document_image.shape[0], int(self.background_image.shape[0]*0.0025)))
        return offset_x, offset_y

    def _resize_document_image(self, document_image):
        max_ratio = max(document_image.shape[0] / self.background_image.shape[0] , \
                        document_image.shape[1] / self.background_image.shape[1])
        return cv2.resize(document_image, (int(document_image.shape[1] * (1 / max_ratio - 0.01)), int(document_image.shape[0] * (1 / max_ratio - 0.01))))

    def apply(self, document_image, reference_image):
        document_image = np.pad(document_image, ((int(self.zoom * document_image.shape[0]), int(self.zoom * document_image.shape[0])), (int(self.zoom * document_image.shape[1]), int(self.zoom * document_image.shape[1])), (0, 0)), 'constant', constant_values = 0)
        reference_image = np.pad(reference_image, ((int(self.zoom * reference_image.shape[0]), int(self.zoom * reference_image.shape[0])), (int(self.zoom * reference_image.shape[1]), int(self.zoom * reference_image.shape[1])), (0, 0)), 'constant', constant_values = 0)
        document_image = self._resize_document_image(document_image)
        reference_image = self._resize_document_image(reference_image)
        offset_x, offset_y = self._generate_random_anchor(document_image)

        # Put background around the document
        background_roi = self.background_image[offset_y: offset_y + document_image.shape[0],
                         offset_x: offset_x + document_image.shape[1]]
        output_image = background_roi * (1 - reference_image) + document_image * (reference_image)
        return output_image

