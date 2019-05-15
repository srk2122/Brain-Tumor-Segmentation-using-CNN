#two images

import os
import numpy
import SimpleITK
import matplotlib.pyplot as plt
import medpy
from medpy.io import load

#%pylab inline
from matplotlib import pyplot as PLT

def sitk_show(img, title=None, margin=0.0, dpi=40):
    nda = SimpleITK.GetArrayFromImage(img)
    #spacing = img.GetSpacing()
    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
    #extent = (0, nda.shape[1]*spacing[1], nda.shape[0]*spacing[0], 0)
    extent = (0, nda.shape[1], nda.shape[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])

    plt.set_cmap("gray")
    ax.imshow(nda,extent=extent,interpolation=None)

    if title:
        plt.title(title)

    plt.show()

# Paths to the .mhd files

def main(imgT2Smooth):

# =============================================================================
#     print("INFUN")
# 
#     #filenameT1 = r"ab1"
#     #filenameT2 = r"ab1"
#     mage_data, image_header = load(ab1)
#     mage_data, image_header = load(ab2)
#     # Slice index to visualize with 'sitk_show'
#     idxSlice = 26
# 
#     # int label to assign to the segmented gray matter
#     labelGrayMatter = 1
# 
#     imgT1Original = SimpleITK.ReadImage(ab1)
#     imgT2Original = SimpleITK.ReadImage(ab2)
#     
#     print("1")
#     sitk_show(SimpleITK.Tile(imgT1Original[:, :, idxSlice],
#                              imgT2Original[:, :, idxSlice],
#                              (2, 1, 0)))
# 
#     imgT1Smooth = SimpleITK.CurvatureFlow(image1=imgT1Original,
#                                           timeStep=0.125,
#                                           numberOfIterations=5)
# 
#     imgT2Smooth = SimpleITK.CurvatureFlow(image1=imgT2Original,
#                                           timeStep=0.125,
#                                           numberOfIterations=5)
#     print("2")
#     sitk_show(SimpleITK.Tile(imgT1Smooth[:, :, idxSlice],
#                              imgT2Smooth[:, :, idxSlice],
#                              (2, 1, 0)))
# =============================================================================
    idxSlice = 26

    # int label to assign to the segmented gray matter
    labelGrayMatter = 1
    lstSeeds = [(165, 178, idxSlice),
                (98, 165, idxSlice),
                (205, 125, idxSlice),
                (173, 205, idxSlice)]

    imgSeeds = SimpleITK.Image(imgT2Smooth)

    for s in lstSeeds:
        imgSeeds[s] = 10000
        print("3")
    sitk_show(imgSeeds[:, :, idxSlice])

# =============================================================================
#   def sitk_tile_vec(lstImgs):
#         lstImgToCompose = []
#         for idxComp in range(lstImgs[0].GetNumberOfComponentsPerPixel()):
#             lstImgToTile = []
#             for img in lstImgs:
#                 lstImgToTile.append(SimpleITK.VectorIndexSelectionCast(img, idxComp))
#             lstImgToCompose.append(SimpleITK.Tile(lstImgToTile, (len(lstImgs), 1, 0)))
#                 
#         print("Sitk 1")
#         sitk_show(SimpleITK.Compose(lstImgToCompose))
#     
#         imgGrayMatterT1 = SimpleITK.ConfidenceConnected(image1=imgT1Smooth,
#                                                         seedList=lstSeeds,
#                                                         numberOfIterations=7,
#                                                         multiplier=1.0,
#                                                         replaceValue=labelGrayMatter)
#     
#         imgGrayMatterT2 = SimpleITK.ConfidenceConnected(image1=imgT2Smooth,
#                                                         seedList=lstSeeds,
#                                                         numberOfIterations=7,
#                                                         multiplier=1.5,
#                                                         replaceValue=labelGrayMatter)
#     
#         imgT1SmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(imgT1Smooth),
#                                         imgGrayMatterT1.GetPixelID())
#         imgT2SmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(imgT2Smooth),
#                                         imgGrayMatterT2.GetPixelID())
#     
#         sitk_tile_vec([SimpleITK.LabelOverlay(imgT1SmoothInt[:,:,idxSlice],
#                                               imgGrayMatterT1[:,:,idxSlice]),
#                        SimpleITK.LabelOverlay(imgT2SmoothInt[:,:,idxSlice],
#                                              imgGrayMatterT2[:,:,idxSlice])])
#     
#     
#         imgComp = SimpleITK.Compose(imgT1Smooth, imgT2Smooth)
#     
#         imgGrayMatterComp = SimpleITK.VectorConfidenceConnected(image1=imgComp,
#                                                        seedList=lstSeeds,
#                                                        numberOfIterations=1,
#                                                        multiplier=0.1,
#                                                        replaceValue=labelGrayMatter)
#     
#         print("4")
#         sitk_show(SimpleITK.LabelOverlay(imgT1SmoothInt[:,:,idxSlice],
#                                          imgGrayMatterComp[:,:,idxSlice]))
#         sitk_show(SimpleITK.LabelOverlay(imgT2SmoothInt[:,:,idxSlice],
#                                          imgGrayMatterComp[:,:,idxSlice]))
#     
#         SimpleITK.WriteImage(imgGrayMatterComp, "GrayMatter.mha")
# 
# =============================================================================
def sitk_tile_vec(lstImgs):
    lstImgToCompose = []
    for idxComp in range(lstImgs[0].GetNumberOfComponentsPerPixel()):
        lstImgToTile = []
        for img in lstImgs:
            lstImgToTile.append(SimpleITK.VectorIndexSelectionCast(img, idxComp))
        lstImgToCompose.append(SimpleITK.Tile(lstImgToTile, (len(lstImgs), 1, 0)))
    sitk_show(SimpleITK.Compose(lstImgToCompose))
    imgGrayMatterT1 = SimpleITK.ConfidenceConnected(image1=imgT1Smooth, 
                                                seedList=lstSeeds,
                                                numberOfIterations=7,
                                                multiplier=1.0,
                                                replaceValue=labelGrayMatter)

    imgGrayMatterT2 = SimpleITK.ConfidenceConnected(image1=imgT2Smooth, 
                                                seedList=lstSeeds,
                                                numberOfIterations=7,
                                                multiplier=1.5,
                                                replaceValue=labelGrayMatter)

    imgT1SmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(imgT1Smooth), 
                                imgGrayMatterT1.GetPixelID())
    imgT2SmoothInt = SimpleITK.Cast(SimpleITK.RescaleIntensity(imgT2Smooth), 
                                imgGrayMatterT2.GetPixelID())

    sitk_tile_vec([SimpleITK.LabelOverlay(imgT1SmoothInt[:,:,idxSlice], 
                                      imgGrayMatterT1[:,:,idxSlice]),
               SimpleITK.LabelOverlay(imgT2SmoothInt[:,:,idxSlice], 
                                     imgGrayMatterT2[:,:,idxSlice])])
    imgComp = SimpleITK.Compose(imgT1Smooth, imgT2Smooth)

    imgGrayMatterComp = SimpleITK.VectorConfidenceConnected(image1=imgComp, 
                                               seedList=lstSeeds,
                                               numberOfIterations=1,
                                               multiplier=0.1,
                                               replaceValue=labelGrayMatter)

    sitk_show(SimpleITK.LabelOverlay(imgT2SmoothInt[:,:,idxSlice], 
                                 imgGrayMatterComp[:,:,idxSlice]))
    SimpleITK.WriteImage(imgGrayMatterComp, "GrayMatter.mhd")
    

 
        
        
if __name__=="__main__":
    print("abcd")
    main(ab1,ab2)
