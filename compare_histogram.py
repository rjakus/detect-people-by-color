# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:53:18 2016

@author: lenovo
"""

# USAGE
# python compare.py --dataset images

# import the necessary packages
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import cv2

index = {}
images = {}

def compare_histograms(time):
    # loop over the image paths
    plt.ioff()
    for imagePath in glob.glob("images" + "/*.jpg"):
    # extract the image filename (assumed to be unique) and
    # load the image, updating the images dictionary
        filename = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)
        images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update
    # the index
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist).flatten()
        
        index[filename] = hist
    
    #ako je samo jedna slika u bazi vrati se u program, nema se šta uspoređivat    
    if len(index.items())==1:
        return
    
    # METHOD #1: UTILIZING OPENCV
    # initialize OpenCV methods for histogram comparison
    #OPENCV_METHODS = (("Correlation", cv2.cv.CV_COMP_CORREL))
    OPENCV_METHODS = (
	("Correlation", cv2.cv.CV_COMP_CORREL),
	("Chi-Squared", cv2.cv.CV_COMP_CHISQR),
	("Intersection", cv2.cv.CV_COMP_INTERSECT), 
	("Hellinger", cv2.cv.CV_COMP_BHATTACHARYYA))
	
    methodName="Intersection"
    # loop over the comparison methods
    
    # initialize the results dictionary and the sort
    # direction
    results = {}
    reverse = True
    
    
    # loop over the index
    for (k, hist) in index.items():
        # compute the distance between the two histograms
        # using the method and update the results dictionary
        #if k==time+".jpg":
        #    continue
        d = cv2.compareHist(index[time+".jpg"], hist, cv2.cv.CV_COMP_INTERSECT)
        results[k] = d
      #  plt.plot(hist)
    
    
    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)
    
    # show the query image
    #fig = plt.figure("Query")
    #ax = fig.add_subplot(1, 1, 1)
    #ax.imshow(images["doge.png"])
    #plt.axis("off")
    
    # initialize the results figure
    #plt.ion()
  #  fig=plt.figure(figsize=(8, 6))
    fig = plt.figure("Results: %s, %s" % (methodName, time))
    fig.suptitle(methodName, fontsize = 20)
    
    
    # loop over the results
    for (i, (v, k)) in enumerate(results):
        # show the result
        #if v>0.7:
        
        
        ax = fig.add_subplot(1, len(images), i + 1)
        if k==time+".jpg":
            ax.set_title("detektiran auto")
        else:
            ax.set_title("%s: %.2f" % (k, v))
        plt.imshow(images[k])
        plt.axis("off")
    
    # show the OpenCV methods
    plt.ion()
    plt.show()
    
    return
