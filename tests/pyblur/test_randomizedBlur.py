from pyblur.RandomizedBlur import *


def test_blur_functions():
    a = {"0": BoxBlur_random,
         "1": DefocusBlur_random,
         "2": GaussianBlur_random,
         "3": LinearMotionBlur_random,
         "4": PsfBlur_random}
    assert a == blurFunctions,\
        "The order of the blur functions has probably changed"
