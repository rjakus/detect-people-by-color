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
    plt.ioff()
    # loop over the image paths
    i = 0
    for imagePath in glob.glob("images/enter" + "/*.png"):
    # extract the image filename (assumed to be unique) and
    # load the image, updating the images dictionary
        if(i<1):
            image = cv2.imread("images/exit/"+time+".png")
            images[time+".png"] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist).flatten()
            index[time+".png"] = hist
            i = 1
        
        filename = imagePath[imagePath.rfind("/") + 1:]
        print filename
        image = cv2.imread(imagePath)
        images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update
    # the index
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist).flatten()
        
        index[filename] = hist
    
    # ako je samo jedna slika u bazi vrati se u program, nema se sta usporedivat    
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
        #print k, hist
        d = cv2.compareHist(index[time+".png"], hist, cv2.cv.CV_COMP_INTERSECT)
        results[k] = d
        #plt.plot(hist)
    
    
    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)
    #print results
    
    #fig = plt.figure("Results: %s, %s" % (methodName, time))
    #fig.suptitle(methodName, fontsize = 20)
    
    bestcorr=0

    # loop over the results
    for (i, (v, k)) in enumerate(results):
        # show the result
        #if v>1.5:

        if k==time+".png":
            continue
        
        if bestcorr<v:
            bestcorr=v
            bestcorrpic=k
            
    
    fig = plt.figure("Results: %s, Correlation: %f" % (methodName, bestcorr))
    fig.suptitle(methodName, fontsize = 20)
            
   # print "\n najbolja corr "
   # print bestcorr

    actualimage=cv2.imread("images/exit/" +time+".png")
    
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(actualimage, cv2.COLOR_BGR2RGB))
       
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(images[bestcorrpic])
    plt.axis("off")
    
    # show the OpenCV methods
    plt.ion()
    plt.show(block=True)
    
    return
