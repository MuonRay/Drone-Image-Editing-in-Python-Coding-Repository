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

import imutils

images=[]
for infile in os.listdir("./"):
    print( "file : " + infile)
    if infile[-3:] == "jpg" or infile[-3:] == "JPG" :
       # print "is tif or DNG (RAW)"
       outfile = infile[:-3] + "png"
       
       print( "new filename : " + outfile)
       dim=(1024,768)
       image = cv2.imread(infile)
       image = cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
       
       images.append(image)
       #Read the images from your directory
       



#stitcher = cv2.createStitcher()
stitcher = cv2.Stitcher.create()
ret,pano = stitcher.stitch(images)

if ret==cv2.STITCHER_OK:
    cv2.imshow('Panorama',pano)
    cv2.waitKey()
    cv2.destroyAllWindows()
else: 
    print("Error during Stitching")
 