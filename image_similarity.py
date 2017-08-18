# import the necessary packages
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import plotly.plotly as py
import numpy as np
import glob
import cv2

def compareImages( current_img_name ):	
	my_classifier = HistogramColorClassifier(channels=[0, 1, 2], hist_size=[128, 128, 128], hist_range=[0, 256, 0, 256, 0, 256], hist_type='BGR')
	image_labels = []
	total_images = 0
	
	for image_path in glob.glob("images" + "/*.jpg"):
		file_name = image_path[image_path.rfind("/") + 1:]

		if file_name == current_img_name:
			continue
		
		total_images = total_images + 1
		image_labels.append(file_name)
		image_model = cv2.imread("images/" + file_name)
		my_classifier.addModelHistogram(image_model)

	current_image = cv2.imread("images/" + current_img_name)
	comparison_array = my_classifier.returnHistogramComparisonArray(current_image, method="intersection")
	#Normalisation of the array
	comparison_distribution = comparison_array / np.sum(comparison_array)
	#print("Comparison Array:")
	#print(comparison_array)
	#print("Distribution Array: ")
	#print(comparison_distribution)
	font_size = 20
	width = 0.5 
	fig = plt.figure(figsize=(16, 6), dpi=100)
	plt.barh(np.arange(total_images), comparison_distribution, width, color='r')
	plt.yticks(np.arange(total_images) + width/2.,image_labels , rotation=0, size=font_size)
	plt.xlim(0.0, 1.0)
	plt.ylim(-0.5, 8.0)
	plt.xlabel('Probability [%]', size=font_size)
	plt.title('Current imge: ' + current_img_name)
	plt.show()

#compareImages('21:10:49.jpg')
