#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:40:51 2024

@author: ananyadalal
"""
"""Description: this program works with wellfinder and adipocyte finder and runs on a directory
    to detect adipocytes and lipid droplets in clusters. Change to your directory (path).
    Through this, you can also run individual image analysis or find images using well finder
        
        """
# imports
import wellfinder_v2 as wf #this finds the regions you want to use and 
import adipocyteFinder as af 
import os
import time

start_time = time.time()
mynames = [] #store all the names of the TD files here
stored_areadata = {}

# change the path to your directory containing images
path = "/Volumes/TOSHIBA EXT/Adipo, vibration in pt 1/D36/D36 5.2024-07-06-00-38-20/"
os.chdir(path)

#find TD images within a given directory 
dir_list = os.listdir(path) 
myimages = []
for i in range(0, len(dir_list)):
    file = dir_list[i]
    if file.find('TD') != -1:
        #get rid of duplicate ._ files that MacOS creates 
        if file.find('._') != 0:
            myimages.append(file)

print('-----Process started!-----\n')
print('Window opened -- click regions to select them for analysis! \nPress q to move images, and c to undo points selected for an image.\n Click cell regions first, and then click a control background region of a similar intensity. ')

#all_regions is a list of lists, where each element is the name of a region (str). step requires user input in window
all_regions = wf.wf_main(myimages)

#track progress
numWells = len(all_regions)
currentWell = 1
#run through each 6mm well and all it's individual regions that were selected ; 
for well in all_regions:
    currentCellRegion = 1
    for cell_region in well:
        numCellRegions = len(well)
        #keep track of which well you are on, for UI
        print('Starting region', currentCellRegion, '/', numCellRegions, 'on well', currentWell, '/', numWells)
        #process the image using adipocyte finder and record the data
        imgname, percent_cover, avgValue = af.processImage(cell_region)
        af.recordData(imgname, percent_cover, avgValue)
        currentCellRegion +=1
    currentWell +=1
    
    
    
#optional line-- detection takes a while especially for a library of images so you can get a reminder when processing is complete
#os.system('say "process complete open python"')
#show all the images that have been processed and verify them
print("All processing complete! Displaying images for verification. Press c while viewing an image if detection is poor (image name will print in terminal), and press q to move to next image. ")    

dir_list = os.listdir(path) 
processedImages = []
for i in range(0, len(dir_list)):
    file = dir_list[i]
    if file.find('edit') != -1:
        #get rid of duplicate ._ files that MacOS creates 
        if file.find('._') != 0:
            processedImages.append(file)

for image in processedImages:
    wf.imageCheck(image)


finaltime = round(time.time() - start_time, 2)
print('\n-----Total time:', finaltime, 'seconds-----\nProcess Complete -- Data exported to area data spreadsheet.csv and control_colors.csv')
