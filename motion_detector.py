# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/video_test.mp4

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
from matplotlib import pyplot as plt
from imutils.object_detection import non_max_suppression
import numpy as np
import compare_histogram
#import image_similarity

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=1500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)

# otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None
between = False

# loop over the frames of the video
while True:
    areas = [] 
    # grab the current frame and initialize the occupied/unoccupied text
    (grabbed, frame) = camera.read()
    (grabbed, frame_original) = camera.read()
    text = "Unoccupied"       
	# if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame, draw the range of interest line (roi),
    #  convert it to grayscale, and blur it
    frame = imutils.resize(frame, width = 500)
    img = cv2.line(frame,(250,500),(250,0),(255,0,0),2)
    frame_original=imutils.resize(frame_original, width = 500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    
    frame_color = frame_original

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
      
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts,hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        
        if area > max_area:
            max_area = area
            best_cnt = cnt
    
    if max_area != 0:
    # finding centroids of best_cnt and draw a circle there
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #print cx
        # determine the most extreme points along the contour
        
        
        #compare x value of centroid and ROI, if they are the same take screenshoot
        if cx>242 and cx<253:
            between= True
        if between== True and cx <242:
                print 'screenshot s desna na lijevo'
                #time=datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
                time=datetime.datetime.now().strftime("%H:%M:%S")
                for cnt in cnts:
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    img = masked_image[y:y+h, x:x+w]
                cv2.imwrite("./images/"+time+".png",img)
                compare_histogram.compare_histograms(time)
               # image_similarity.compareImages(time+".jpg")
                between=False
                
        if cx>242 and cx<254:
            between= True
        if between == True and cx >253:
                print 'screenshot s lijeva na desno'
                time=datetime.datetime.now().strftime("%H:%M:%S")
                for cnt in cnts:
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    img = masked_image[y:y+h, x:x+w]
                cv2.imwrite("./images/"+time+".png",img)
                compare_histogram.compare_histograms(time)
            #    image_similarity.compareImages(time+".jpg")
                between=False
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        ar=cv2.contourArea(c)
        areas.append(ar)
        
        (x, y, w, h) = cv2.boundingRect(c)        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
	(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
    masked_image = cv2.bitwise_and(frame_color, frame_color, mask = thresh)
    hist_mask = cv2.calcHist([frame_color],[0], thresh ,[256],[0,256])
    
    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Color", masked_image)
    # cv2.imshow("Thresh", thresh)
    # cv2.imshow("Frame Delta", frameDelta)
    
    key = cv2.waitKey(30) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
#camera.release()
#cv2.destroyAllWindows()
