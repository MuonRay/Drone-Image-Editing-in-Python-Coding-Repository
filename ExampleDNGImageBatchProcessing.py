# -*- coding: utf-8 -*-
"""
@author: cosmi

Working Batch Processer for DNG to JPG

rawpy is an easy-to-use Python wrapper for the LibRaw library. 
rawpy works natively with numpy arrays and supports a lot of options, 
including direct access to the unprocessed Bayer data to perform demosaicing (post process) allowing it to be
used freely by many other native python libraries for gamma correction, histogram correction, etc.
It also contains some extra functionality for finding and repairing hot/dead pixels.
import rawpy.enhance for this

skimage s also very handy here as it has a very nice exposure correction tool for histogram correction


"""

import os
import rawpy
import imageio
import cv2
import numpy as np
## Visual and plotting libraries
import matplotlib.pyplot as plt
## Image Processing libraries
from skimage import exposure

for infile in os.listdir("./"):
    print( "file : " + infile)
    if infile[-3:] == "tif" or infile[-3:] == "DNG" :
       # print "is tif or DNG (RAW)"
       outfile = infile[:-3] + "jpg"
       raw = rawpy.imread(infile)
       print( "new filename : " + outfile)
       
       
       #rgb = raw.postprocess()


       
# Postprocessing, i.e demosaicing here, will always 
#change the original pixel values. Typically what you want
# is to get a linearly postprocessed image so that roughly 
#the number of photons are in linear relation to the pixel values. 
#You can do that with:

       rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=8)
       
       # in python image processing an image is considered as a matrix. 
       # the simplest way to represent it is using a numpy.array type, as shown below:       
       
      
       
       #Apply gamma corrections: gamma values greater than 1 will shift the image histogram towards left and the output image will be darker than the input image. On the other hand, for gamma values less than 1, the histogram will shift towards right and the output image will be brighter than the input image.
  
       gamma_corrected_rgb = exposure.adjust_gamma(rgb, gamma=0.5, gain=1)

       
       image=gamma_corrected_rgb
  
      
       #apply histogram equalization
       #using skimage (easy way)
       hist_equalized = exposure.equalize_hist(image)


           
       #save images to working directory    
       imageio.imsave(outfile, hist_equalized)
       
