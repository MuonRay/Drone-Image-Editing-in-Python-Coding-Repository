# -*- coding: utf-8 -*-
"""
Created on Mon May 25 18:51:53 2020

@author: cosmi
"""

#Image stitching (Panorama Maker DNG Batch Version)"


import os
import rawpy
import imageio
import cv2
import numpy as np

## Image Processing libraries
from skimage import exposure

images=[]
for infile in os.listdir("./"):
    print( "file : " + infile)
    if infile[-3:] == "tif" or infile[-3:] == "DNG" :
       # print "is tif or DNG (RAW)"
       outfile = infile[:-3] + "jpg"
       
       print( "new filename : " + outfile)
       dim=(640,360)
       raw = rawpy.imread(infile)
       # Postprocessing, i.e demosaicing here, will always 
#change the original pixel values. Typically what you want
# is to get a linearly postprocessed image so that roughly 
#the number of photons are in linear relation to the pixel values. 
#You can do that with:

       rgb = raw.postprocess()
      
       image = cv2.resize(rgb,dim,interpolation = cv2.INTER_AREA)
       image = cv2.bitwise_not(~image)


       images.append(image)
       #Read the images from your directory
       


#stitcher = cv2.createStitcher()
stitcher = cv2.Stitcher.create()
ret,pano = stitcher.stitch(images)

if ret==cv2.STITCHER_OK:
    
    #need to swap colors here, demosaicing algoithm in rawpy jumbles to colors for some reason?:
    truepano = cv2.cvtColor(pano,cv2.COLOR_BGR2RGB)
    
    #Apply gamma corrections: gamma values greater than 1 will shift the image histogram towards left and the output image will be darker than the input image. On the other hand, for gamma values less than 1, the histogram will shift towards right and the output image will be brighter than the input image.
    

    gamma_corrected_pano = exposure.adjust_gamma(truepano, gamma=1, gain=0.5)

       
    panoimage=gamma_corrected_pano
       
    #apply histogram equalization
    #using skimage (easy way)
    hist_equalized_pano = exposure.equalize_hist(panoimage)
    
    
    panoramaoutfile = "panoresult.png"

    
    imageio.imsave(panoramaoutfile, pano)


    cv2.imshow('Panorama',hist_equalized_pano)
    cv2.waitKey()
    cv2.destroyAllWindows()
else: 
    print("Error during Stitching")
 