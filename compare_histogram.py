from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import cv2

def compare_histograms( current_img_name ):	
    index = {}
    images = {}
    i = 0

    for image_path in glob.glob("images/enter/" + "/*.png"):
        file_name = image_path[image_path.rfind("/") + 1:]
        
        if(i<1):
            #print current_img_name
            image = cv2.imread("images/exit/"+current_img_name)
            images[current_img_name] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist = cv2.normalize(hist).flatten()
            index[current_img_name] = hist
            i = 1
            continue
        
        image = cv2.imread(image_path)
        images[file_name] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist).flatten()
        index[file_name] = hist

    results = {}
    reverse = False
    total_images = 0
    comparison_distribution = []
    image_labels = []

    for (k, hist) in index.items():
        if(k == current_img_name):
            continue

        d = cv2.compareHist(index[current_img_name], hist, cv2.cv.CV_COMP_INTERSECT)
        results[k] = d

    fig = plt.figure("Exit image: " + current_img_name )
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(images[current_img_name])
    plt.axis("off")
    images.pop(current_img_name)
    total_images = len(images)
    results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)

    for (i, (v, k)) in enumerate(results):
        image_labels.append(k)
        comparison_distribution.append(v)
    
    fig, ax = plt.subplots()    
    width = 0.75 # the width of the bars 
    ind = np.arange(len(images))  # the x locations for the groups
    ax.barh(ind, comparison_distribution, width, color="blue")
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(image_labels, minor=False)
    plt.title('Comparing the exiting person with the entering ones')
    plt.xlabel('Correlation (more correlation = better similarity)')
    plt.ylabel('Image name')  
    for i, v in enumerate(comparison_distribution):
        ax.text(v + 3, i + .25, str(v), color='red', fontweight='bold')

    #print comparison_distribution
    plt.show()
    return