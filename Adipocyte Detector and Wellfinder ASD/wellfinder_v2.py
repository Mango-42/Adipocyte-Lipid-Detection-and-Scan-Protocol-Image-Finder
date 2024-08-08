#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 16:24:42 2024

@author: ananyadalal
"""

# code for drawPoints and loadImage function adapted from https://learnopencv.com/mouse-and-trackbar-in-opencv-gui/ 

#imports
import cv2
import pandas as pd
import os

#general global scope variables

points = []
allpoints = []
region_names = []
all_regions = []
size_y = 3948
size_x = 4247
#super crucial, this is the matrix for identifying the image number based on the where you click on a TD image
df = pd.read_excel("Image_Matrix.xlsx", sheet_name=0)
order_matrix = df.to_numpy()



#create a window where images will display
cv2.namedWindow("Window - click center and control points")


def drawPoints(action, x, y, flags, *userdata):
    """Desc: this function draws points on a TD image based on where you click """
    # When left click happens, save the xy location to a list called points and show it on the image
    
    if action == cv2.EVENT_LBUTTONDOWN:
      points.append((x,y))
      cv2.circle(image, points[-1], 16, (255, 0, 0), -1)
      
      cv2.imshow("Window - click center and control points",image)
      print('point identified!', points[-1])

def loadImage():
    """Desc: this function loads in a TD image in a window and waits for mouse clicks on the image and then sends xy data to drawPoints()
        It saves all xy points in a list 'points' and after q is hit, moves the 'points' list into allpoints. 
        allpoints stores all the image-identifying points in one list, with the same indices as the list of images to be used, myimages (which has """
    global points
    global image 
    
    dummy = image.copy()
    # highgui function called when mouse events occur
    cv2.setMouseCallback("Window - click center and control points", drawPoints)  

    # Make a dummy image, will be useful to clear the drawing
    
    k=0
    # Close the window when key q is pressed
    while k!=113:
      # Display the image
      cv2.imshow("Window - click center and control points", image)
      k = cv2.waitKey(0)
      # Clear the window and existing points if c is pressed
      if (k == 99):
        print('Inputs cleared.')
        image = dummy
        cv2.imshow("Window - click center and control points", image)
        points = []
    
    allpoints.append(points)
    points = []

def find_regions(imgname, x_coord, y_coord):
    """Desc: takes the original image as input (just to know what day and well it is), and the xy coords from above fxn
    Determines the name of the local region image to use for processing. You can take this output and send it for processsing"""
    #dimensions of individual regions
    region_y = size_y/10
    region_x = size_x/8

    #find the closest matrix position based on the coordinate of center
    matrix_y = int(y_coord //region_y)
    matrix_x = int(x_coord // region_x)
    #find the closest region by number in the matrix. offset by 1 bc I put the matrix in wrong lol
    region_num = int(order_matrix[matrix_y][matrix_x]) -1

    # find number after TD --> tells you which well is it
    well_num = (imgname[imgname.find('TD') +2])

    #add 68 region offset for each well (1st well has no offset, thus the - 1)
    region_num += 68*(int(well_num) -1)
    
    #me when I save my files as D2 instead of D02 smh my bad 
    if int(region_num) < 10: 
        region_num = '0' + str(region_num)

    region_name = imgname[0:16] + 'D_p00_0_A01f' + str(region_num) + 'd4.TIF'
    
    return region_name


def wf_main(myimages):
    """Desc: this function opens all TD images and sends xy point data to find_regions to get names. 
    It stores all_region data, which is a list of names of images that should be processed for analysis"""
    # run all the TD images and manually identify what regions you want to analyze. click control region last
    global image
    global region_names
    for img in myimages:
        # Read Images
 
        image = cv2.imread(img)

        loadImage()
    #once you're done selecting images, close the window
    cv2.destroyAllWindows()
    
    #find regions given the points you selected
    i = 0
    for TD_set in allpoints:
        for point in TD_set:
            x_coord = point[0]
            y_coord = point[1]
            region_name = find_regions(myimages[i], x_coord, y_coord)
            region_names.append(region_name)
        all_regions.append(region_names)
        region_names = []
        i += 1
    #if something's wrong here with image names, you can uncomment the next line
    # print(all_regions)
    # print(all_regions)
    return all_regions

def imageCheck(imageName):
    """Desc: this function takes in an image name, opens it in a window. if you click c, it will print the name in the terminal (useful for verifying detection)"""
    image = cv2.imread(imageName)
    k=0
    # Close the window when key q is pressed
    while k!=113:
      # Display the image
      cv2.imshow("Window - click center and control points", image)
      k = cv2.waitKey(0)
      # If poor detection is seen click key c and store the file name so it can be filtered out later
      if (k == 99):
        print(imageName)
        # cv2.imshow("Window - click center and control points", image)
    

