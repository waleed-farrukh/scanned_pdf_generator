import cv2
import numpy as np


# Rotation:
# This class sets the parameters for Rotation Transformation.
#
# @Params:- rotation_angle_degree_start: Start value for rotation angle range (degrees).
#           rotation_angle_degree_end: Stop value for rotation angle range (degrees).
#           rotation_angle_degree_step: Step value for rotation angle range (degrees).
class Rotation:
    def __init__(self, rotation_angle_degree_start : int, rotation_angle_degree_end : int, rotation_angle_degree_step : int):
        self.rotation_angle_degree_start = rotation_angle_degree_start
        self.rotation_angle_degree_end = rotation_angle_degree_end
        self.rotation_angle_degree_step = rotation_angle_degree_step

    # Get transformation matrix (3x3) for rotation.
    def _get_transformation_matrix_rotation(self, angle : int) -> np.array:
        transformation_mat =  np.vstack([cv2.getRotationMatrix2D((0, 0), angle, 1.), [0, 0, 1]])
        return transformation_mat

    def _get_random_angle_degrees(self) -> int:
        return np.random.choice(
            np.arange(self.rotation_angle_degree_start, self.rotation_angle_degree_end, self.rotation_angle_degree_step))


# Perspective:
# This class sets the parameters for Perpective Transformation.
#
# @Params:- perspective_x_start: Start value for horizontal perspective distortion.
#           perspective_x_end: Stop value for horizontal perspective distortion.
#           perspective_y_start: Step value for vertical perspective distortion.
#           perspective_y_end: Step value for vertical perspective distortion.
# Note: The values for these in the default config.json are selected based on experiments.
class Perspective:
    def __init__(self, perspective_x_start : float, perspective_x_end : float, perspective_y_start : float, perspective_y_end: float):
        self.perspective_x_start = perspective_x_start
        self.perspective_x_end = perspective_x_end
        self.perspective_y_start= perspective_y_start
        self.perspective_y_end= perspective_y_end

    # Get transformation matrix (3x3) for perspective.
    def _get_transformation_matrix(self, perspective_x : float, perspective_y : float) -> np.array:
        return np.array([[1, 0, 0], [0, 1, 0], [perspective_x, perspective_y, 1]], np.float32)

    def _get_random_perspective(self) -> tuple:
        perspective_x = np.random.choice(np.arange(self.perspective_x_start, self.perspective_x_end, 0.000025))
        perspective_y = np.random.choice(np.arange(self.perspective_y_start, self.perspective_y_end, 0.000025))
        return (perspective_x, perspective_y)


# Spatial Transformer:
# This class implements all the spatial transformations, including rotation and perspective.
#
# @Params:- rotation_transformer: 'Rotation' object.
#           perspective_transformer: 'Perspective' object
class SpatialTransformer:
    def __init__(self, rotation_transformer: Rotation, perspective_transformer: Perspective):
        self.rotation_transformer = rotation_transformer
        self.perspective_transformer = perspective_transformer

    # Apply Spatial transformation with random paramters from given range in config
    # @Input:- img: input image
    # @Out:-   Output image
    def apply(self, img):
        # Create a reference image to note keep track of spatial transformation. Used in other variant functions e.g. Background.
        # The reference image is filled with (1, 1, 1).
        transformed = np.copy(img)
        img_reference = np.ones(img.shape, dtype=np.uint8)

        #List containing all transformations
        transformation_matrix_list = []

        shift_to_origin = np.array([[1, 0, -transformed.shape[1] / 2], [0, 1, -transformed.shape[0] / 2], [0, 0, 1]], np.float32)
        shift_to_center = np.array([[1, 0, transformed.shape[1] / 2], [0, 1, transformed.shape[0] / 2], [0, 0, 1]], np.float32)
        transformation_matrix_list.append(shift_to_center)

        # Perspective Transform
        if self.perspective_transformer:
            perspective_x, perspective_y = self.perspective_transformer._get_random_perspective()
            perspective_tranformation_matrix = self.perspective_transformer._get_transformation_matrix(perspective_x,
                                                                                                      perspective_y)
            transformation_matrix_list.append(perspective_tranformation_matrix)

        # Rotation
        if self.rotation_transformer:
            angle_rotation = self.rotation_transformer._get_random_angle_degrees()
            transformation_matrix_list.append(self.rotation_transformer._get_transformation_matrix_rotation(angle_rotation))

        #Shift to Origin
        transformation_matrix_list.append(shift_to_origin)

        # Calculate scaling required to contain transformed image in figure
        transformation_matrix_for_scaling = np.identity(3, np.float32)
        for t in transformation_matrix_list:
            transformation_matrix_for_scaling = np.matmul(transformation_matrix_for_scaling, t)
        scale_factor_x, scale_factor_y = self._get_scale_factor(transformation_matrix_for_scaling, transformed)
        scale_factor_x = min(scale_factor_x, scale_factor_y)
        scale_factor_y = scale_factor_x
        scale_mat = np.array(
            [[scale_factor_x, 0, (1 - scale_factor_x) / 2 * transformed.shape[1]], [0, scale_factor_y, (1 - scale_factor_y) / 2 * transformed.shape[0]], [0, 0, 1]],
            np.float32)
        transformation_matrix_list.insert(0, scale_mat)

        # Calculate final transformation matrix
        transformation_matrix = np.identity(3, np.float32)
        for t in transformation_matrix_list:
            transformation_matrix = np.matmul(transformation_matrix, t)

        # Apply all applicable transformations to document
        transformed = cv2.warpPerspective(transformed, transformation_matrix, (transformed.shape[1], transformed.shape[0]))
        reference = cv2.warpPerspective(img_reference, transformation_matrix, (transformed.shape[1], transformed.shape[0]))

        # Crop Image to remove excessive padding
        top_left, bottom_left, top_right, bottom_right = (0,0), (0, img.shape[0]), (img.shape[1], 0),  (img.shape[1], img.shape[0])
        top_left, bottom_left, top_right, bottom_right = self._apply_to_point(top_left, transformation_matrix), \
                                                         self._apply_to_point(bottom_left, transformation_matrix), \
                                                         self._apply_to_point(top_right, transformation_matrix), \
                                                         self._apply_to_point(bottom_right, transformation_matrix)
        min_x, max_x = min(top_left[0], bottom_left[0], top_right[0], bottom_right[0]), max(top_left[0], bottom_left[0], top_right[0], bottom_right[0])
        min_y, max_y = min(top_left[1], bottom_left[1], top_right[1], bottom_right[1]), max(top_left[1], bottom_left[1], top_right[1], bottom_right[1])
        transformed = transformed[min_y : max_y, min_x : max_x]
        reference = reference[min_y: max_y, min_x: max_x]

        return  transformed, reference

    # Get scale factor to make sure image does not go out of bounds.
    # @Input:-  transformation_matrix: the transformation matrix (3x3) for all the included spatial transformations
    #           img: the input image
    # @Out:-    tuple of required scale factor in horizontal and vertical axis
    def _get_scale_factor(self, transformation_matrix, img):
        tl = (0, 0)
        tr = (img.shape[1], 0)
        bl = (0, img.shape[0])
        br = (img.shape[1], img.shape[0])
        tl_perspective, tr_perspective, bl_perspective, br_perspective = [self._apply_to_point(x, transformation_matrix) for x in [tl, tr, bl, br]]
        x_coordinates = np.array([point[0] for point in [tl_perspective, tr_perspective, bl_perspective, br_perspective]])
        y_coordinates = np.array([point[1] for point in [tl_perspective, tr_perspective, bl_perspective, br_perspective]])
        x_diff_left, x_diff_right = 0 - x_coordinates, x_coordinates - img.shape[1]
        y_diff_top, y_diff_bottom = 0 - y_coordinates, y_coordinates - img.shape[0]
        max_x_diff = max(np.concatenate((x_diff_left, x_diff_right)))
        max_y_diff = max(np.concatenate((y_diff_top, y_diff_bottom)))
        return img.shape[1] / (img.shape[1] + 2 * max_x_diff), img.shape[0] / (img.shape[0] + 2 * max_y_diff)

    # Apply spatial transformation to a particular point (pixel).
    # @Input:-  point: tuple of point (x, y)
    #           transformation matrix: the transformation matrix (3x3) for all the included spatial transformations
    # @Out:-    tranformed point (x, y)
    def _apply_to_point(self, point : tuple, transformation_matrix) -> tuple:
        out_x = (transformation_matrix[0, 0] * point[0] + transformation_matrix[0, 1] * point[1] + transformation_matrix[0, 2]) / (transformation_matrix[2, 0] * point[0] +transformation_matrix[2, 1] * point[1] + transformation_matrix[2, 2])
        out_y = (transformation_matrix[1, 0] * point[0] + transformation_matrix[1, 1] * point[1] + transformation_matrix[1, 2]) / (transformation_matrix[2, 0] * point[0] +transformation_matrix[2, 1] * point[1] + transformation_matrix[2, 2])
        return int(out_x), int(out_y)





