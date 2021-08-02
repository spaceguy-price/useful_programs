#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 20:23:37 2021

@author: Andrew Price

Function to extract the foreground from the testbed images.
"""
import argparse
import numpy as np
import cv2
from skimage.filters import sobel
from skimage.segmentation import watershed
from skimage import morphology

debug = False

def extract_foreground(img, t, scale=10):
    # Resize the image
    w = int(img.shape[1]*scale/100)
    h = int(img.shape[0]*scale/100)
    img_l = cv2.resize(img, dsize = (w,h))
    
    #Ensure image is black and white
    img_b = cv2.cvtColor(img_l, cv2.COLOR_RGB2GRAY)
    
    # Sobel Filter Edge Detection
    img_s =  sobel(img_b)
    
    # Find markers (based on intensity)
    markers = np.zeros_like(img_s)   
    markers[img_b < 50] = 1 #background (low intensity)
    markers[img_b > t] = 2  #illuminated sections (high intensity)
    
    # Run the watershed algorithm
    img_w = watershed(img_s, markers, compactness = 0.001)
    
    # Obtain the foreground mask  
    maskF = np.zeros(np.shape(img_w))
    maskF = img_w - 1
    
    # fill small mask holes (closing)
    area = (np.max(np.shape(maskF))*0.5).astype(np.uint8)
    maskF = morphology.area_closing(image=maskF, 
                                    area_threshold=area,
                                    connectivity=100)
    
    # remove small mask areas (opening)
    area = (np.max(np.shape(maskF))*0.5).astype(np.uint8)
    maskF = morphology.area_opening(image=maskF, 
                                    area_threshold=area,
                                    connectivity=100)
    
    # resize and obtain the background mask
    maskF = cv2.resize(maskF.astype('float32'), 
                       dsize=(np.shape(img)[1], np.shape(img)[0]), 
                       interpolation = cv2.INTER_AREA)
    maskB = maskF.copy()
    maskB[maskF == 0] = 1   #maskB is the inverse of maskA
    maskB[maskF == 1] = 0
    
    # Obtain the foreground and background
    imgF = maskF[:,:,np.newaxis]*img
    imgB = maskB[:,:,np.newaxis]*img
    
    return imgF, imgB


if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    # (For command line operation)
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', 
                    '--image', 
                    type = str,
                    default = 'example.JPG',
                    help = 'Path to the input image')
    ap.add_argument('-s',
                    '--scale',
                    type=int,
                    default = 2,
                    help='Percentage to scale image during processing')
    ap.add_argument('-t',
                    '--threshold',
                    type = int,
                    default = 100,
                    help = 'Cutoff threshold (intensity) for selecting markers')
    args = ap.parse_args()
    
    # Read the image
    img = cv2.imread(args.image)
    
    # Extract the foreground and background
    imgF, imgB = extract_foreground(img=img, 
                                    t=args.threshold, 
                                    scale=args.scale)
    
    # Save the new images to file
    cv2.imwrite(args.image[0:-4] + '_F.jpg', imgF)
    cv2.imwrite(args.image[0:-4] + '_B.jpg', imgB)
    
    
    
    
