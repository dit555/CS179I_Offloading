import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import os.path
from os import path

cascPath = "data.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
# log.basicConfig(filename='webcam.log', level=log.INFO)

# video_capture = cv2.VideoCapture(0)
anterior = 0
overlay_path = "me_gusta_filter.png"

# find most recent image file if one is avalible
last_good = 0  # latest index we found
num = 0  # cur index
max_it = 5  # how many times we allow loop in findRecent() to run after not finding any new
a = 0

def findRecent():
    r = True
    name = ""
    good = ""
    num = last_good
    it = 0  # how many times we have ran since we found a file
    while r:
        name = "/users/dit55/CS179I_Offloading/findFaceEngine2.0/data/Result"
        name += str(num)
        name += ".jpg"
        # print("checking for:", name)
        if path.exists(name):
            # print(name, "found:")
            good = name
            it = 0
        else:
            # print(name, "!!!NOT found:")
            it += 1
            if it >= max_it:
                r = False
                if good == "":
                    return "BAD"
        num += 1
    return good


while True:

    # Read frames
    name = findRecent()

    if name != "BAD":
        frame = cv2.imread(name)
        # print(name)
        if frame is None:
            continue
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
    overlay = cv2.imread(overlay_path)
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        center_x = int(x + w / 2)
        center_y = int(y + h / 2)
        x2 = int(overlay.shape[1] / 2)
        y2 = int(overlay.shape[0] / 2)
        y_1 = center_y - y2
        y_2 = center_y + y2
        x_1 = center_x - x2
        x_2 = center_x + x2
        frame[y_1:y_2, x_1:x_2] = overlay

    colorName = "/users/dit55/CS179I_Offloading/findFaceEngine2.0/storageData/Result{}.jpg".format(a)
    cv2.imwrite(colorName, frame)
    if anterior != len(faces):
        anterior = len(faces)
    #       log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))
    a = a + 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

