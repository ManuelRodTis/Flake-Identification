#from cProfile import label
#from turtle import width
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import pyplot
import cv2 
from collections import Counter
import os

import skimage
from skimage import data, filters, measure, morphology
from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate
from skimage import color
from skimage import io


import tkinter
from tkinter import *

######################################################################
######################################################################

# We are going to define some functions we will need to use

######################################################################
######################################################################


#####################################################################

#This Function finds the most common value in a list.

def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]  

######################################################################


#######################################################################

# This function returns true if a flake candidate is found.  
# It requires the following parameters:
# - file directory (file_dir)
# - RGB minimum and maximum contrats values (r_val_min, r_val_max, g_val_min, g_val_max, b_val_min, b_val_max,) 
# - Area

def flake_candidate(file_dir, r_val_min, r_val_max, g_val_min, g_val_max, b_val_min, b_val_max, Area):
   
    ##################################################################
    #                        Read Image                              #
    ##################################################################

    # Read the image and get array
    image = cv2.imread(file_dir)

    # cv2.imread gets image in BGR2, with this line we turn it to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
    ##################################################################
    #                        Red channel                             #
    ##################################################################

    # This line gets the red channel 
    channel_r = image [:,:,0]

    # Here we find the Backround value
    list_r = channel_r.flatten()
    Backrgound_red = most_frequent(list_r)


    # Here we apply our mask to the red channel. We keep the pixels that meet the condition and turn the rest to 0.

    channel_r = image [:,:,0]
    # We define the formula to be applied
    r_ratios = (np.abs(channel_r - Backrgound_red))/(Backrgound_red + channel_r)
    # We use the formula to create the mask
    mask_r = np.logical_or(r_ratios<r_val_min, r_ratios > r_val_max)
    # We update our channel using the mask 
    channel_r[mask_r] = 0

    
    ##################################################################
    #                        Green channel                           #
    ##################################################################

    # This line gets the green channel 
    channel_g = image [:,:,1]

    # Here we find the Backround value
    list_g = channel_g.flatten()
    Backrgound_green = most_frequent(list_g)

    # Here we apply our mask to the red channel. We keep the pixels that meet the condition and turn the rest to 0.

    channel_g = image [:,:,1]
    # We define the formula to be applied
    g_ratios = (np.abs(channel_g - Backrgound_green ))/(Backrgound_green + channel_g)
    # We use the formula to create the mask
    mask_g = np.logical_or(g_ratios<g_val_min, g_ratios > g_val_max)
    # We update our channel using the mask 
    channel_g[mask_g] = 0


    ##################################################################
    #                        Blue channel                            #
    ##################################################################

    # This line gets the blue channel 

    channel_b = image [:,:,2]

    # Here we find the Backround value
    list_b = channel_b.flatten()
    Backrgound_blue = most_frequent(list_b)

    # Here we apply our mask to the red channel. We keep the pixels that meet the condition and turn the rest to 0.

    channel_b = image [:,:,2]
    # We define the formula to be applied
    b_ratios = (np.abs(channel_b - Backrgound_blue))/(Backrgound_blue + channel_b)
    # We use the formula to create the mask
    mask_b = np.logical_or(b_ratios<b_val_min, b_ratios >  b_val_max)
    # We update our channel using the mask 
    channel_b[mask_b] = 0

    ##################################################################
    #                        New Image                               #
    ##################################################################

    # After segmenting our color channels we can use them to create a new image and measure the area

    image [:,:,0] = channel_r
    image [:,:,1] = channel_g
    image [:,:,2] = channel_b

    # Skimage helps us get information of an image including the area of different regions in the image.
    # Here we can get a list of the "areas" of the the regions found in the image and can use this to target images
    # containing objects with a specific size  

    object_features = skimage.measure.regionprops(image)
    object_areas = [objf["area"] for objf in object_features]

    flakes = []

    for i in object_areas:
        if i > Area:
            flakes.append(i)

    len(flakes)

    if len(flakes)>0:
        #plt.imshow(image)
        #print("yes")
        return True
    
########################################################################


#########################################################################

# This function returns true if a flake candidate is found.  
# It requires the following parameters:
# - file directory (file_dir)
# - Background Values (Background_red, Background_green, Background_blue,)
# - RGB minimum and maximum contrats values (r_val_min, r_val_max, g_val_min, g_val_max, b_val_min, b_val_max,) 
# - Area

def flake_candidate_Background_given(file_dir,Background_red, Background_green, Background_blue,
                                     r_val_min, r_val_max, g_val_min, g_val_max, b_val_min, b_val_max, Area):

    ##################################################################
    #                        Read Image                              #
    ##################################################################

    # Read the image and get array
    image = cv2.imread(file_dir)

    # cv2.imread gets image in BGR2, with this line we turn it to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    ##################################################################
    #                        Red channel                             #
    ##################################################################

     # This line gets the red channel
    channel_r = image [:,:,0]
    
    # Here we apply our mask to the red channel. We keep the pixels that meet the condition and turn the rest to 0.

    # We define the formula to be applied
    r_ratios = (np.abs(channel_r - Background_red))/(Background_red + channel_r)
    # We use the formula to create the mask
    mask_r = np.logical_or(r_ratios<r_val_min, r_ratios > r_val_max)
    # We update our channel using the mask 
    channel_r[mask_r] = 0


    ##################################################################
    #                        Green channel                           #
    ##################################################################

    # This line gets the green channel 
    channel_g = image [:,:,1]

    # Here we apply our mask to the red channel. We keep the pixels that meet the condition and turn the rest to 0.

    # We define the formula to be applied
    g_ratios = (np.abs(channel_g - Background_green))/(Background_green + channel_g)
    # We use the formula to create the mask
    mask_g = np.logical_or(g_ratios<g_val_min, g_ratios > g_val_max)
    # We update our channel using the mask 
    channel_g[mask_g] = 0


    ##################################################################
    #                        Blue channel                            #
    ##################################################################

    # This line gets the green channel 
    channel_b = image [:,:,2]

    # Here we apply our mask to the red channel. We keep the pixels that meet the condition and turn the rest to 0.

    # We define the formula to be applied
    b_ratios = (np.abs(channel_b - Background_blue))/(Background_blue + channel_b)
    # We use the formula to create the mask
    mask_b = np.logical_or(b_ratios<b_val_min, b_ratios >  b_val_max)
    # We update our channel using the mask
    channel_b[mask_b] = 0

    ##################################################################
    #                        New Image                               #
    ##################################################################


  # After segmenting our color channels we can use them to create a new image and measure the area
  
    image [:,:,0] = channel_r
    image [:,:,1] = channel_g
    image [:,:,2] = channel_b


    # Skimage helps us get information of an image including the area of different regions in the image.
    # Here we can get a list of the "areas" of the the regions found in the image and can use this to target images
    # containing objects with a specific size  

    object_features = skimage.measure.regionprops(image)
    object_areas = [objf["area"] for objf in object_features]

    flakes = []

    for i in object_areas:
        if i > Area:
            flakes.append(i)

    len(flakes)

    if len(flakes)>0:
        #plt.imshow(image)
        #print("yes")
        return True

#########################################################################


#########################################################################

# This function will be the main function containing everything (calculates background)  

def main(file_dir, r_val_min, r_val_max, g_val_min, g_val_max, b_val_min, b_val_max, Area):
    # We use the slsh to construct the path to each txt file
    slash='\\'
    
    # This empty list will contane the names of the txt data files
    dir_lists = []
    
    # This empty list will contain the paths to the txt data files 
    final_paths = [] 
    

    # Here we fill out the dir_list list
    for file in os.listdir(file_dir):
    # check only text files
        if file.endswith('.tif'):
            dir_lists.append(file)
        
    # Here we fill out the dir_list list    
    for i in range(len(dir_lists)):
        union = file_dir+slash+dir_lists[i]
        final_paths.append(union)

    # Here we create a txt file where we'll sabe the name if the targeted images. In the actual GUI yoy will be able to name it.
    images_text_file = open("Text_file_entry","w+")


    for i, path in enumerate(final_paths):
    #print(i,path)
    #print(path)
        func = flake_candidate(r_val_min, r_val_max, g_val_min, g_val_max, b_val_min, b_val_max, Area)

        if func == True:
            images_text_file.write(dir_lists[i] + '\n')
    
    images_text_file.close()

#########################################################################


#########################################################################

# This function will be the main function contining evrything (needs background values)  

def main_need_background(file_dir,Background_red, Background_green, Background_blue, 
                         r_val_min, r_val_max, g_val_min, g_val_max, b_val_min, b_val_max, Area):
    # We use the slsh to construct the path to each txt file
    slash='\\'
    
    # This empty list will contane the names of the txt data files
    dir_lists = []
    
    # This empty lis will contain the paths to the txt data files 
    final_paths = [] 
    

    # Here we fill out the dir_list list
    for file in os.listdir(file_dir):
    # check only text files
        if file.endswith('.tif'):
            dir_lists.append(file)
        
    # Here we fill out the dir_list list    
    for i in range(len(dir_lists)):
        union = file_dir+slash+dir_lists[i]
        final_paths.append(union)

    # Here we create a txt file where we'll sabe the name if the targeted images. In the actual GUI yoy will be able to name it.
    images_text_file = open("flakes.txt","w+")


    for i, path in enumerate(final_paths):
    #print(i,path)
    #print(path)
        func = flake_candidate(path,Background_red, Background_green, Background_blue, 
                               r_val_min, r_val_max, g_val_min, g_val_max, b_val_min, b_val_max, Area)

        if func == True:
            images_text_file.write(dir_lists[i] + '\n')
    
    images_text_file.close()

#########################################################################



# Create an instance of tkinter window

root = Tk()
root.title("Image Analysis")
root.geometry("650x600")

######################################################################
# File directory entry 
######################################################################

directory_label = Label(root, text="Directory Location: ")
directory_label.grid(row=1,column=0,)

e = Entry(root, width=70)
e.grid(row=1, column=1, columnspan=3)

######################################################################
# Space label 
######################################################################

space_label1 = Label(root, text="   ")
space_label1.grid(row=2,column=0,)



######################################################################
# Background values
######################################################################

Bg = tkinter.IntVar()

tkinter.Label(root, 
        text="""Background Values:""",
        justify = tkinter.LEFT,
        padx = 20).grid(row = 3, column = 0)

tkinter.Radiobutton(root, 
               text="Calculate",
               padx = 20, 
               variable=Bg, 
               value=0).grid(row = 3, column = 1)

tkinter.Radiobutton(root, 
               text="Input",
               padx = 20, 
               variable=Bg, 
               value=1).grid(row = 3, column = 2)

######################################################################
# Space label 
######################################################################

space_label1 = Label(root, text="   ")
space_label1.grid(row=4,column=0,)


######################################################################
# Backgrund Inputs
######################################################################

# Background Red Values

BG_Red = Label(root, text="Background Red: ")
BG_Red.grid(row=5,column=0,)
BG_Red_val = Entry(root, width=70)
BG_Red_val.grid(row=5, column=1, columnspan=3)

# Background Green Values

BG_Green = Label(root, text="Background Green: ")
BG_Green.grid(row=6,column=0,)
BG_Green_val = Entry(root, width=70)
BG_Green_val.grid(row=6, column=1, columnspan=3)


# Background Blue Values

BG_Blue = Label(root, text="Background Blue: ")
BG_Blue.grid(row=7,column=0,)
BG_Blue_val = Entry(root, width=70)
BG_Blue_val.grid(row=7, column=1, columnspan=3)


######################################################################
# Space label 
######################################################################

space_label1 = Label(root, text="   ")
space_label1.grid(row=8,column=0,)

######################################################################
# RED CHANNEL INPUT 
######################################################################

# Write label

R_label = Label(root, text="RED CHANNEL ")
R_label.grid(row=9,column=0,)


# Make min value box

R_label_min = Label(root, text="Min value: ")
R_label_min.grid(row=10,column=0,)
R_brigntess_min = Entry(root, width=70)
R_brigntess_min.grid(row=10, column=1, columnspan=3)

# Make max value box

R_label_max = Label(root, text="Max value: ")
R_label_max.grid(row=11,column=0,)
R_brigntess_max = Entry(root, width=70)
R_brigntess_max.grid(row=11, column=1, columnspan=3)


######################################################################
# Space label 
######################################################################

space_label2 = Label(root, text="   ")
space_label2.grid(row=12,column=0,)


######################################################################
# GREEN CHANNEL INPUT 
######################################################################

# Write label

G_label = Label(root, text="GREEN CHANNEL ")
G_label.grid(row=13,column=0,)

# Create min value box 

G_label_min = Label(root, text="Min value: ")
G_label_min.grid(row=14,column=0,)
G_brigntess_min = Entry(root, width=70)
G_brigntess_min.grid(row=14, column=1, columnspan=3)

# Create max value box 

G_label_max = Label(root, text="Max value: ")
G_label_max.grid(row=15,column=0,)
G_brigntess_max = Entry(root, width=70)
G_brigntess_max.grid(row=15, column=1, columnspan=3)



######################################################################
# Space label 
######################################################################

space_label10 = Label(root, text="   ")
space_label10.grid(row=16,column=0,)



######################################################################
# BLUE CHANNEL INPUT 
######################################################################

# Write label

B_label = Label(root, text="BLUE CHANNEL ")
B_label.grid(row=17,column=0,)

# Create min value box 

B_label_min = Label(root, text="Min value: ")
B_label_min.grid(row=18,column=0,)
B_brigntess_min = Entry(root, width=70)
B_brigntess_min.grid(row=18, column=1, columnspan=3)

# Create max value box

B_label_max = Label(root, text="Max value: ")
B_label_max.grid(row=19,column=0,)
B_brigntess_max = Entry(root, width=70)
B_brigntess_max.grid(row=19, column=1, columnspan=3)


######################################################################
# Space label 
######################################################################

space_label = Label(root, text="   ")
space_label .grid(row=20,column=0,)



######################################################################
# Flake Area 
######################################################################

# Write flake area

Flake_area = Label(root, text="Flake Area (um)").grid(row=21,column=0,)

Flake_area_entry = Entry(root, width=70)
Flake_area_entry.grid(row=21, column=1, columnspan=4)



######################################################################
# Text file name
######################################################################

# Write flake area

Text_file = Label(root, text="Text file name").grid(row=23,column=0,)

Text_file_entry = Entry(root, width=70)
Text_file_entry.grid(row=23, column=1, columnspan=4)


######################################################################
# Space label 
######################################################################

space_label = Label(root, text="   ")
space_label .grid(row=24,column=0,)


######################################################################
# Magnification Buttons 
######################################################################


magnification = tkinter.IntVar()

tkinter.Label(root, 
        text="""Choose Magnification:""",
        justify = tkinter.LEFT,
        padx = 20).grid(row = 25, column = 0)

tkinter.Radiobutton(root, 
               text="10x",
               padx = 20, 
               variable=magnification, 
               value=1).grid(row = 25, column = 1)

tkinter.Radiobutton(root, 
               text="20x",
               padx = 20, 
               variable=magnification, 
               value=2).grid(row = 25, column = 2)


tkinter.Radiobutton(root, 
               text="60x",
               padx = 20, 
               variable=magnification, 
               value=3).grid(row = 26, column = 1)

tkinter.Radiobutton(root, 
               text="100x",
               padx = 20, 
               variable=magnification, 
               value=4).grid(row = 26, column = 2)


######################################################################
# Space label 
######################################################################

space_label = Label(root, text="   ")
space_label .grid(row=27,column=0,)

#Cell size (per pixel) = Physical length of a pixel on the CCD / total magnification
# I might have gotten these values wrong but it's an easy fix 

# 100x : 0.0645 um/pixel or 15.50 pixels/um
# 60x  : 0.1075 um/pixel or 9.30 pixels/um
# 20x  : 0.3225 um/pixel or 3.10 pixels/um
# 10x  : 0.645 um/pixel or 1.55 pixel/um


def func():
    # If no background values given 

    # magnification 10x
    if (Bg == 0) and (magnification == 1):
        return main(e.get(), R_brigntess_min.get(), R_brigntess_max.grt(), G_brigntess_min.get(),
                    G_brigntess_max.get(), B_brigntess_min.get(), B_brigntess_max.get(), (1.55**2)*(Flake_area_entry.get()))
    
    # magnification 20x
    elif (Bg == 0) and (magnification == 2):
        return main(e.get(), R_brigntess_min.get(), R_brigntess_max.grt(), G_brigntess_min.get(),
                    G_brigntess_max.get(), B_brigntess_min.get(), B_brigntess_max.get(), (3.10**2)*(Flake_area_entry.get()))
    
    # magnification 60x
    elif (Bg == 0) and (magnification == 3):
        return main(e.get(), R_brigntess_min.get(), R_brigntess_max.grt(), G_brigntess_min.get(),
                    G_brigntess_max.get(), B_brigntess_min.get(), B_brigntess_max.get(), (9.3**2)*(Flake_area_entry.get()))
    
    # magnification 100x
    elif (Bg == 0) and (magnification == 4):
        return main(e.get(), R_brigntess_min.get(), R_brigntess_max.grt(), G_brigntess_min.get(),
                    G_brigntess_max.get(), B_brigntess_min.get(), B_brigntess_max.get(), (15.5**2)*(Flake_area_entry.get()))
    

    # If background values given 

    # magnification 10x
    if (Bg == 1) and (magnification == 1):
        return main_need_background(e.get(), BG_Red_val.get(), BG_Green_val.get, BG_Blue_val.get(),R_brigntess_min.get(),
                                    R_brigntess_max.grt(), G_brigntess_min.get(), G_brigntess_max.get(), B_brigntess_min.get(),
                                    B_brigntess_max.get(), (1.55**2)*(Flake_area_entry.get()))
    
    # magnification 20x
    elif (Bg == 1) and (magnification == 2):
        return main_need_background(e.get(), BG_Red_val.get(), BG_Green_val.get, BG_Blue_val.get(), R_brigntess_min.get(),
                                    R_brigntess_max.grt(), G_brigntess_min.get(), G_brigntess_max.get(), B_brigntess_min.get(),
                                    B_brigntess_max.get(), (3.10**2)*(Flake_area_entry.get()))
    
    # magnification 60x
    elif (Bg == 1) and (magnification == 3):
        return main_need_background(e.get(), BG_Red_val.get(), BG_Green_val.get, BG_Blue_val.get(), R_brigntess_min.get(),
                                    R_brigntess_max.grt(), G_brigntess_min.get(), G_brigntess_max.get(), B_brigntess_min.get(),
                                    B_brigntess_max.get(), (9.3**2)*(Flake_area_entry.get()))
    
    # magnification 100x
    elif (Bg == 1) and (magnification == 4):
        return main_need_background(e.get(), BG_Red_val.get(), BG_Green_val.get, BG_Blue_val.get(), R_brigntess_min.get(),
                                    R_brigntess_max.grt(), G_brigntess_min.get(), G_brigntess_max.get(), B_brigntess_min.get(),
                                    B_brigntess_max.get(), (15.5**2)*(Flake_area_entry.get()))


def close():
   #win.destroy()
   root.quit()

######################################################################
# START BUTTON 
######################################################################

Start_button = Button(root, text="Start",  padx=90,  pady=3, command=func).grid(row = 27, column = 1)

######################################################################
# QUIT BUTTON 
######################################################################

Quit_button = Button(root, text="Quit", padx=90,  pady=3, command=close).grid(row= 27, column = 2)




root.mainloop()
