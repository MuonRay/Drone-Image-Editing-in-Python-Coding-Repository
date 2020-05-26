# -*- coding: utf-8 -*-
"""
Created on Mon May 25 10:26:29 2020

@author: cosmi
"""

#Image stitching (Panorama Maker Batch Version)"


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
    if infile[-3:] == "jpg" or infile[-3:] == "JPG" :
       # print "is tif or DNG (RAW)"
       outfile = infile[:-3] + "jpg"
       
       print( "new filename : " + outfile)
       #dim=(1024,768)
       dim=(640, 360)

       image = cv2.imread(infile)
       image = cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
       
       images.append(image)
       #Read the images from your directory
       



#stitcher = cv2.createStitcher()
stitcher = cv2.Stitcher.create()
ret,pano = stitcher.stitch(images)

if ret==cv2.STITCHER_OK:
     
    #Apply gamma corrections: gamma values greater than 1 will shift the image histogram towards left and the output image will be darker than the input image. On the other hand, for gamma values less than 1, the histogram will shift towards right and the output image will be brighter than the input image.
    

    gamma_corrected_pano = exposure.adjust_gamma(pano, gamma=0.3, gain=0.5)

       
    panoimage=gamma_corrected_pano
       
    #apply histogram equalization
    #using skimage (easy way)
    hist_equalized_pano = exposure.equalize_hist(panoimage)

    
    panoramaoutfile = "panoresult.png"
    #need to swap colors here, demosaicing algoithm in rawpy jumbles to colors for some reason?:
    #truepano = cv2.cvtColor(pano,cv2.COLOR_BGR2RGB)
    

    
    cv2.imshow('Panorama',hist_equalized_pano)
    imageio.imsave(panoramaoutfile, pano)

    cv2.waitKey()
    cv2.destroyAllWindows()
else: 
    print("Error during Stitching")
 