#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:17:51 2024

@author: ananyadalal
"""


# imports: numpy and PIL for image loading, matplotlib for plotting, skimage for droplet detection. time and os for overarching program functionality 
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from math import sqrt
from skimage.feature import blob_log, blob_doh
from skimage.filters import gaussian
import time
import os
import csv


#if running only a single image or directory of preselected images, just change the path within this script. otherwise keep commented-- will mess with pathing of the program!
# path = "/Volumes/TOSHIBA EXT/Adipo, vibration in pt 1/Qualitative Data D0 to D26/"
# os.chdir(path)
# dirList = os.listdir(path)
# myImages = []
# #if running a directory of preselected images
# for i in range(0, len(dirList)):
#     file = dirList[i]
#     if file.find('._') != 0: #remove ._ duplicate files that MacOS creates
#         myImages.append(file)

def processImage(imageName):
    """Desc: this function takes in a microscope scanned image (imageName) and highlights adipocytes and lipid droplets. Returns the image name and percent covered by adipocytes on the image -- imageName, percentCovered
    Key arrays and operations:
        
    
    """
    startRegionTime = time.time()
    print('\n-----Starting work on ', imageName,"-----")
    
    # open the image, convert it to a grayscale numpy array grayImage with shape size_y by size_x
    image = Image.open(imageName)
    
    grayImage = image.convert('L')
    grayImage = np.array(grayImage)
    size_y, size_x = grayImage.shape
    
    # create empty nan arrays to store intermediate steps. 
    # adipocytesImage holds first pass thresholding by scikit's blob_doh method to find big regions of interest; logImage has identified droplet regions by scikit's  blob_log function
    adipocytesImage = np.full((size_y, size_x), np.nan)
    logImage = np.full((size_y, size_x), np.nan)
    finalImage = np.full((size_y, size_x), np.nan)
    
    
    # find the average color of the grayImage -- will be helpful as darker images need a slightly different step later due to thresholding steps picking up better on brighter images
    average_color = np.mean(grayImage)
    
    # detect blobs using scikit's blob_doh method on grayImage
    #detectedBlobs is a list of tuples of the form (y, x, r)-- signifiying the center and radius of a region of interest
    if average_color > 130: dohThreshold = .005
    elif average_color < 115: dohThreshold = .003
    else: dohThreshold= .0035
    
    detectedBlobs = blob_doh(grayImage, min_sigma = 1.5, max_sigma = 7, num_sigma = 30, threshold= dohThreshold)
    print(len(detectedBlobs), "general regions of interest were tagged. Finding droplets...")
    
    # plot each blob area but at a slightly larger radius (to account for spots blob_doh misses) on empty adipocytesImage. this cuts background noise that the next method blob_log would otherwise detect
    for blob in detectedBlobs:
        y, x, r = blob
        # increased plotting radius by 5; may need to be different for images of different resolution or for much larger avg droplet size
        r = int(r+5)
        y = int(y)
        x = int(x)
        #copies these regions from the grayImage onto adipocytesImage
        adipocytesImage[y-r : y+r, x-r : x+r] = grayImage[y-r : y+r, x-r : x+r]
        
    # if present, remove scale bar at this steo bc it will always gets detected (very bright..)
    # adipocytesImage[1450:1535, 0:500] = np.nan
    
    logThreshold = 10
    if average_color < 115: logThreshold = 0
   
    # detect droplets on the adipocytes image using blob log. threshold is very high to ensure less noise on brighter images.
    detectedDrops = blob_log(adipocytesImage, min_sigma = 1.5, max_sigma = 9, threshold= logThreshold)
    # plot these droplet areas on the empty logImage
    for drop in detectedDrops:
        y, x, r = drop
        # on scikit's page for blob_log, r is approx the third value in the drop tuple * sqrt(2)
        r = int(r*sqrt(2))
        y = int(y)
        x = int(x)
        #plot regions marked as droplets as squares. if something is wrong in detection at later steps, try plotting logImage, it'll let you know what is getting detected. 
        logImage[y-r : y+r, x-r : x+r] = int(100)
    
    
    # if detection is poor from this process, turn on these plots. they'll show you processing layers so you can check where the problem is. turn off plots at the end
    # plt.figure(dpi=600)
  
    # plt.imshow(grayImage, cmap = 'Greys_r', alpha = .5)
    # plt.imshow(adipocytesImage, cmap = 'Greys_r', alpha = 1)
    # plt.imshow(logImage, cmap = 'winter', alpha = 1)
    
    
    # we're going to blur out logImage to find general adipocytes now, which should be brightly labeled by blob_log on logImage. first, we need to replace the np.nan values in the bg with 1 (low value), bc otherwise the blur function next won't work.
    # VECTORIZE THIS FUNCTION 
    for j in range(0, 1536):
        for i in range (0, 2048):
            if logImage[j][i] != 100:
                logImage[j][i] = 1
    # blurImage is a numpy array with the scikit gaussian blur of logImage. you can adjust sigma to be higher if you're working with less dense droplet samples. you can experiment with this function on any random array to see what works best
    blurImage = gaussian(logImage, sigma = 10)
    
    # iterate through the blurImage array -- if a pixel is greater than detectionVal, store it on the final array in the same place
    # VECTORIZE THIS FUNCTION
    #change detection val based on brightness of the image, IF NEEDED
   
    # if average_color < 115: detectionVal = 5
    
    detectionVal = 20
    if average_color > 130: detectionVal = 25
    if average_color < 115: detectionVal = 10
    
    
    #variables to measure percent covered
    numPix = 0
    totalPix = size_x * size_y
    
    for j in range(0, 1536):
        for i in range (0, 2048):
            if blurImage[j][i] > detectionVal:
                numPix += 1
                finalImage[j][i] = blurImage[j][i]
    percentCovered = round(numPix/ totalPix * 100, 3)
    
    # plotting the final image -- dpi. move this line up if you plot earlier
    plt.figure(dpi=600)
    
    # plot background gray image 
    plt.imshow(grayImage, cmap = 'Greys_r', alpha = 1)
    
    # plot gaussian blurred regions showing full adipocytes
    plt.imshow(finalImage, cmap = 'winter', alpha = .3)
    plt.axis('off')
    plt.title(str(imageName)) #+ "\nLabeled adipocytes with lipid droplets")
    
    
    # save the figure, if wanted
    saveName = 'edit_' + imageName
    print(saveName)
    plt.savefig(saveName, dpi = 600, format='png')
    plt.show()
    print(percentCovered, '% of the surface on ', imageName, 'was detected to be adipocytes with significant amounts of lipid droplets\n', average_color, 'was the avg color')
    endRegionTime = round(time.time() - startRegionTime, 2)
    print('Process Complete -- Data exporting to area data spreadsheet.csv and control_colors.csv')
    print('-----Total time:', endRegionTime, 'seconds-----\n')
    
    return imageName, percentCovered, average_color


def recordData(imgname, percent_cover, avgValue):
    bound1 = imgname.find('1f')
    bound2 = imgname.find('d4')
    well_num = int(imgname[bound1 +2 : bound2]) // 68 + 1
    abbr = str(imgname[0:6]) +' well #' + str(well_num)
    
    with open('/Volumes/TOSHIBA EXT/area_data_spreadsheet.csv', 'a', newline='') as csvfile:
        mywriter = csv.writer(csvfile)
        mywriter.writerow([abbr, imgname, percent_cover, avgValue])

    

#if running only a single image or directory of preselected images, uncomment the following line(s)
# for imageName in myImages:
#     processImage(imageName)


        
