# Brief Overview
I wrote these scripts to find images I needed from EVOS scan protocols, which scan many extra images, and to detect clustered lipid droplets in adipocytes. I worked on these two steps separately, creating separate well finder and adipocyte finder programs that worked together to find images, detect droplets, and store data about percent covered by lipid droplets in an accessible format. The entire process is shown in the video for Final Method and Final Detection. 

For general use of adipocyteFinder on a directory of pre-selected images, change the directory name in adipocyteFinder.py to your directory with images, and uncomment the code at the top and bottom that is not within functions. You can try this out on the images inside the Sample Images folder!Use the return of processImage in recordData if you want to store percent covered. Note that you might have to change pathing of a few things (area_data_spreadsheet and image_matrix)

For general use of wellfinder, you’re all set if you’re using EVOS scanning on 35 mm dishes. Change directory at the beginning of the file to whatever image directory you want to use, and include a print statement inside wellfinder main for region name (so it'll print the names of the regions you click on). However, you may need to adjust find_regions()’s variables so that the image names are correct, prefix-wise. The same goes for if you use a different image matrix (ie, for a 96 well plate). 

For use of both programs together, use control_center.py. Change directories and just run this file. Make sure the directory you’re using has the files wellfinder uses (total data images and all scanned individual regions). There should be no code running outside of functions in adipocyteFinder or wellFinder when doing this. 

These scripts are detailed heavily through their individual steps in the drive below for further usage in adipocyte detection or just making general image finding easier in the lab (ie, finding specific images on more commonly used 96 well plates by clicking on total data images). There are also videos of how they work!!! 

https://drive.google.com/drive/folders/1lTRZgUaV9EmFKcXo1zdEWKCSoLLFdb6w?usp=sharing
