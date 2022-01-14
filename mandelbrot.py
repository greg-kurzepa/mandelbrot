import numpy as np
from PIL import Image
from numba import vectorize
import time
import math
import numpy as np

#x = 0.281717921930775
#y = 0.5771052841488505
#r = 1E-6

def render_img(itns, dimensions, x, y, r, showImage=True, fileName=None, directory=""):
    if directory and directory[-1] != "/": directory += "/"
    if dimensions[0] > dimensions[1]:
        x_range = [x-r*dimensions[0]/dimensions[1],x+r*dimensions[0]/dimensions[1]]
        y_range = [y-r,y+r]
    else:
        x_range = [x-r,x+r]
        y_range = [y-r*dimensions[1]/dimensions[0],y+r*dimensions[1]/dimensions[0]]
    inputs = np.array([[complex(x_range[0]+j*(x_range[1]-x_range[0])/dimensions[0], y_range[1]-i*(y_range[1]-y_range[0])/dimensions[1]) for j in range(dimensions[0])] for i in range(dimensions[1])], dtype=complex)
    outputs = np.array(mandel_func(inputs, itns))
    outputPng(outputs, showImage, dimensions, directory, itns, fileName)

@vectorize(['int32(complex128, int32)'], target='cuda')
def mandel_func(c, iterations):
    z = complex(0,0)
    for i in range(iterations):
        z = z*z + c
        if abs(z) >= 2:
            i = i + 2 - math.log(math.log2(abs(z)))
            return(i)
    return(0)

COLS = {
    0 : (66,30,15),
    1 : (25,7,26),
    2 : (9,1,47),
    3 : (4,4,73),
    4 : (0,7,100),
    5 : (12,44,138),
    6 : (24,82,177),
    7 : (57,125,209),
    8 : (134,181,229),
    9 : (211,236,248),
    10 : (241,233,191),
    11 : (248,201,95),
    12 : (255,170,0),
    13 : (204,128,0),
    14 : (153,87,0),
    15 : (106,52,3)
}

def outputPng(data, showImage, dimensions, directory, itns, fileName):
    maxiter = np.amax(data)

    data = data/itns
    red = data**0.2
    green = np.zeros((dimensions[1], dimensions[0]))
    blue = np.zeros((dimensions[1], dimensions[0]))
    data = np.rint(np.stack((red,green,blue), axis=2) * 255).astype(np.uint8)
    
    mandelbrot = Image.fromarray(data, mode="RGB")
    
    #wikipedia colour scheme
    #pixels[i,j] = COLS[math.floor((data[j][i]%mod_factor)/(mod_factor/16))]
    
    if not fileName:
        print(f"{directory}{time.time()}")
        mandelbrot.transpose(Image.FLIP_TOP_BOTTOM).save(f"{directory}{time.time()}.png")
    else:
        mandelbrot.transpose(Image.FLIP_TOP_BOTTOM).save(f"{directory}{fileName}.png")
    if showImage: mandelbrot.transpose(Image.FLIP_TOP_BOTTOM).show()
