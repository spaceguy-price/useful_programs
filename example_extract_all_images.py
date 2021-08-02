#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 21:14:22 2021

@author: Andrew Price

Example to extract the foreground for all images
"""

import os
import cv2
from extract import extract_foreground

# Variables
scale = 2       # percentage of scaling (ex: mask is reduced to a resolution of 10%)
threshold = 100 # number from 1-255, try different values if the lighting changes

# Get list of all images
image_location = '/home/butters/Desktop/Foreground_Segmentation/images/'
image_list = os.listdir(image_location) #list EVERYTHING in the folder 'images'

# Where to save images?
image_save = '/home/butters/Desktop/Foreground_Segmentation/imagesFB/'

for image_name in image_list:
    # Read the image
    img = cv2.imread(image_location + image_name)
    
    # Extract the foreground
    imgF, imgB = extract_foreground(img, t=threshold, scale=scale)
    
    # Save the new images to file
    cv2.imwrite(image_save + image_name[0:-4] + '_F.jpg', imgF)
    cv2.imwrite(image_save + image_name[0:-4] + '_B.jpg', imgB)
