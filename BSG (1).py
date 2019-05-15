# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import style

import numpy as np
import numpy.core.multiarray
import warnings
import tkinter as tk
from tkinter import ttk
import cv2
from skimage import io
from brain3 import *
import brain3 as bb
#import sr_main_keras as s_code


style.use('ggplot')
warnings.simplefilter('ignore')

from tkinter import filedialog

global_filename = ""
# ===========================================================================================
def get_input(inp):
    print(inp)

# function to browse files
def browsefunc1():
    global global_filename1
    filename = filedialog.askopenfilename()
    global_filename1 = filename
    pathlabel.config(text=filename)

def browsefunc2():
    global global_filename2
    filename = filedialog.askopenfilename()
    global_filename2 = filename
    pathlabel.config(text=filename)


# given the path to image, returns its name
def get_img_name(path):
    path_split = path.split("/")
    return path_split[-1]

# save the genrated image
def save_file(image, img_path, scale):
    img_name = get_img_name(img_path)
    save_img_name = img_name[:-4] + "_SR_x{0}".format(scale) + img_name[-4:]

    save_folder =  filedialog.askdirectory()
    save_file = save_folder + "/" + save_img_name

    io.imsave(save_file, image)

# function to Show low resolution image on a new pop up window
def show_lr(ab1,ab2):
    global imgT1Smooth
    global imgT2Smooth
    global lstImgs
    print("INFUN")

    #filenameT1 = r"ab1"
    #filenameT2 = r"ab1"
    mage_data, image_header = load(ab1)
    mage_data, image_header = load(ab2)
    # Slice index to visualize with 'sitk_show'
    idxSlice = 26

    # int label to assign to the segmented gray matter
    labelGrayMatter = 1

    imgT1Original = SimpleITK.ReadImage(ab1)
    imgT2Original = SimpleITK.ReadImage(ab2)
    
    print("1")
    sitk_show(SimpleITK.Tile(imgT1Original[:, :, idxSlice],
                             imgT2Original[:, :, idxSlice],
                             (2, 1, 0)))

    imgT1Smooth = SimpleITK.CurvatureFlow(image1=imgT1Original,
                                          timeStep=0.125,
                                          numberOfIterations=5)

    imgT2Smooth = SimpleITK.CurvatureFlow(image1=imgT2Original,
                                          timeStep=0.125,
                                          numberOfIterations=5)
    print("2")
    lstImgs=sitk_show(SimpleITK.Tile(imgT1Smooth[:, :, idxSlice],
                             imgT2Smooth[:, :, idxSlice],
                             (2, 1, 0)))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# =============================================================================
#     popup_lr = tk.Tk()
#     popup_lr.wm_title("Segmented Image")
# 
#     label = ttk.Label(popup_lr, justify=tk.LEFT, text="""Segmented  Image""", font=("Verdana", 14, "bold"))
#     label.pack(side="top", fill="x", pady=10, padx=10)
# 
#     img = io.imread(path)
#     if img is None:
#         print(path)
#         print(type(path))
#         print("IMG IS NONE")
# 
#     #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     plt.imshow(img)
#     fig, ax = plt.subplots()
#     im = ax.imshow(img, origin='upper')
#     plt.grid("off")
# 
#     canvas = FigureCanvasTkAgg(fig, popup_lr)
#     canvas.show()
#     canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
# 
# 
# 
#     label = ttk.Label(popup_lr, justify=tk.CENTER, text="")
#     label.pack(side="top", pady=2, padx=30)
#     B1 = ttk.Button(popup_lr, text="SELECT FOLDER TO SAVE THIS IMAGE", command=lambda: save_file(img, path, scale=1))
#     B1.pack(side="top")
#     popup_lr.mainloop()
# =============================================================================

# ============================================================================================#

root = tk.Tk()
tk.Tk.wm_title(root, "Brain Tumor Segmentation")
label = ttk.Label(root, text="Brain Tumor Segmentation", font=("Verdana", 22, "bold"))
label.pack(side="top", pady=30, padx=50)


label = ttk.Label(root, justify=tk.CENTER,
                  text="Click the load button below to select the image file", font=("Verdana", 11))
label.pack(side="top", pady=5, padx=5)


button1 = ttk.Button(root, text="Load Image", command=lambda: browsefunc1())
button1.pack(anchor='w',pady=20,padx=20)

button6 = ttk.Button(root, text="Load Image", command=lambda: browsefunc2())
button6.pack(anchor='w',pady=20,padx=20)

# =============================================================================
button2 = ttk.Button(root, text="Pre Process", command=lambda: show_lr(global_filename1,global_filename2))
button2.pack(anchor='w',pady=20,padx=20)
# =============================================================================

# =============================================================================
button3 = ttk.Button(root, text="Patch Extraction",command=lambda: bb.main(imgT2Smooth))
button3.pack(anchor='w',pady=20,padx=20)
# 
# =============================================================================
button5 = ttk.Button(root, text="Segmentation",command=lambda: bb.sitk_tile_vec(imgT2Smooth))
button5.pack(anchor='w',pady=20,padx=20)


# =============================================================================
# button4 = ttk.Button(root, text="Feature Extraction")
# button4.pack(anchor='w',pady=20,padx=20)
# 
# =============================================================================

pathlabel = ttk.Label(root, font=("Verdana", 11, "bold"))
pathlabel.pack(side="top", pady=3, padx=30)

label = ttk.Label(root, justify=tk.CENTER, text="")
label.pack(side="top", pady=1, padx=30)


if __name__ == "__main__":
    root.mainloop()
