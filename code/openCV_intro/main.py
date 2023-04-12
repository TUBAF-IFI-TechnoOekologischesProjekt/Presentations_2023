# Detects opens a openCV device, counts blobs based on isolated contours 
# and saves the image when the number of insects changes
#
# Author: Sebastian Zug, TU Bergakademie Freiberg

import cv2
import os
import numpy as np
import time
import shutil

# define a function to check if a contour is a rectangle
def is_contour_bad(c):
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# the contour is 'bad' if it is a rectangle
	return len(approx) == 4

# create new folder for images, delete old folder if it exists
folder = 'insect_images'
if os.path.exists(folder):
    shutil.rmtree(folder)
else:
    os.mkdir(folder)

# define a video capture object
vid = cv2.VideoCapture(4)
bug_count = 0
  
while(True):
    # Capture the video frame
    ret, img = vid.read()

    # Check availablity
    if not ret:
        print('Failed to grab frame')
        break

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 100, 255, 
                                cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(image=thresh, 
                                           mode=cv2.RETR_TREE, 
                                           method=cv2.CHAIN_APPROX_NONE)
    contours = [c for c in contours if not is_contour_bad(c)]

    # draw contours on the original image
    img_result = img.copy()
    cv2.drawContours(image=img_result, contours=contours, 
                     contourIdx=-1, color=(0, 255, 0), 
                     thickness=2, lineType=cv2.LINE_AA)
    
    # Display the resulting frame
    font = cv2.FONT_HERSHEY_SIMPLEX  
    cv2.putText(img_result, 'Number of contours: ' + 
                str(len(contours)), (10, 30), font, 1, 
                (0, 255, 0), 2, cv2.LINE_AA)
    
    # 
    cv2.imshow('result', img_result)

    # Store the resulting frame in case of change
    if len(contours) != bug_count:
        file_path = os.path.join(folder, 'insect_' + str(time.time()) + '.jpg')
        cv2.imwrite(file_path, img_result)
        bug_count = len(contours)

    # Press Q on keyboard to  exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()