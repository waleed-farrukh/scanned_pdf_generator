# -*- coding: utf-8 -*-
import numpy as np
import pickle
from PIL import Image
from scipy.signal import convolve2d
import os.path

pickledPsfFilename =os.path.join(os.path.dirname( __file__),"psf.pkl")

with open(pickledPsfFilename, 'rb') as pklfile:
    psfDictionary = pickle.load(pklfile, encoding='latin1')


def PsfBlur(img, psfid):
    kernel = psfDictionary[psfid]
    if img.ndim == 2:
        imgarray = np.array(img, dtype="float32")
        convolved = convolve2d(imgarray, kernel, mode='same', fillvalue=255.0).astype("uint8")
    elif img.ndim == 3:
        convolved = np.zeros(img.shape, dtype=np.uint8)
    for i in range(3):
        imgarray = np.array(img[:, :, i], dtype="float32")
        convolved[:, :, i] = convolve2d(imgarray, kernel, mode='same', fillvalue=255.0).astype("uint8")
    return np.array(convolved)
    
def PsfBlur_random(img):
    psfid = np.random.randint(0, len(psfDictionary))
    return PsfBlur(img, psfid)
    
    
