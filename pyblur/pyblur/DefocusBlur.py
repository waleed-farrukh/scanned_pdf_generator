# -*- coding: utf-8 -*-
import math
import numpy as np
from PIL import Image
from scipy.signal import convolve2d
from skimage.draw import circle

defocusKernelDims = [3,5,7,9]

def DefocusBlur_random(img):
    kernelidx = np.random.randint(0, len(defocusKernelDims))    
    kerneldim = defocusKernelDims[kernelidx]
    return DefocusBlur(img, kerneldim)

def DefocusBlur(img, dim):
    kernel = DiskKernel(dim)
    if img.ndim == 2:
        imgarray = np.array(img, dtype="float32")
        convolved = convolve2d(imgarray, kernel, mode='same', fillvalue=255.0).astype("uint8")
    elif img.ndim == 3:
        convolved = np.zeros(img.shape, dtype=np.uint8)
    for i in range(3):
        imgarray = np.array(img[:, :, i], dtype="float32")
        convolved[:, :, i] = convolve2d(imgarray, kernel, mode='same', fillvalue=255.0).astype("uint8")
    return np.array(convolved)


def DiskKernel(dim):
    kernelwidth = dim
    kernel = np.zeros((kernelwidth, kernelwidth), dtype=np.float32)
    circleCenterCoord = int(math.floor(dim/2))
    circleRadius = circleCenterCoord +1
    
    rr, cc = circle(circleCenterCoord, circleCenterCoord, circleRadius)
    kernel[rr,cc]=1
    
    if(dim == 3 or dim == 5):
        kernel = Adjust(kernel, dim)
        
    normalizationFactor = np.count_nonzero(kernel)
    kernel = kernel / normalizationFactor
    return kernel

def Adjust(kernel, kernelwidth):
    kernel[0,0] = 0
    kernel[0,kernelwidth-1]=0
    kernel[kernelwidth-1,0]=0
    kernel[kernelwidth-1, kernelwidth-1] =0 
    return kernel