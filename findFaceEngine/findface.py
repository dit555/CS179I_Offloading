import cv2
import logging as log
import datetime as dt
from os import path
import time
import numpy as np
import os.path

cascPath = "data.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
#log.basicConfig(filename='webcam.log', level=log.INFO)

#video_capture = cv2.VideoCapture(0)
anterior = 0

# find most recent image file if one is avalible
last_good = 0  # latest index we found
num = 0  # cur index
max_it = 5  # how many times we allow loop in findRecent() to run after not finding any new


def findRecent():
    r = True
    name = ""
    good = ""
    num = last_good
    it = num  # how many times we have ran since we found a file
    while r:
        name = "/users/dit55/data/Result"
        name += str(it)
        name += ".jpg"
        # print("checking for:", name)
        if path.exists(name):
            # print(name, "found:")
            good = name
            num = it
            it_max = 0
        else:
            # print(name, "!!!NOT found:")
            it_max += 1
            if it_max >= max_it:
                r = False
                if good == "":
                    return "BAD"
        it += 1
    return good


num_o = 0 #number appended to overlay image name
for i in range(1,1000):

    # Read frames
    name = findRecent()
    #calculate run speed
    fps = []
    start = time.time()

    #check if there is a recent file
    if name != "BAD":
        
        frame = cv2.imread(name)
        if(frame is None):
            continue
        #print(name)
    else:
        #print("no image found")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    #for (x, y, w, h) in faces:
        #print("center at X: ", x + w, "Y: ", y + h)
    

    if anterior != len(faces):
        anterior = len(faces)
        #log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))

    # Display the resulting frame
    # cv2.imshow('Video', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #print fps
    end = time.time()
    f = 1 /(end - start)
    fps.append(f)
    print("fps: ", f)

# Display the resulting frame
# cv2.imshow('Video', frame)

# When everything is done, release the capture
# video_capture.release()
#cv2.destroyAllWindows()
print("average fps:", np.mean(fps))

