import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import os.path
from os import path


cascPath = "data.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0

#find most recent image file if one is avalible
last_good = 0 #latest index we found
num = 0 #cur index
max_it = 5 #how many times we allow loop in findRecent() to run after not finding any new 
def findRecent():
	r = True
	name = ""
	good = ""
	num = last_good
	it = 0 #how many times we have ran since we found a file
	while r:
		name = "Result"
		name += str(num)
		name += ".jpg"
		#print("checking for:", name) 
		if(path.exists(name)):
			#print(name, "found:")
			good = name
			it = 0
		else:
			#print(name, "!!!NOT found:")
			it += 1
			if (it >= max_it):
				r = False
				if good == "":
					return "BAD"
		num += 1
	return good



while True:

	#Read frames
	name = findRecent()
	if (name != "BAD"):
		frame = cv2.imread(name)
	else:
		print("no image found")
		continue
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
	)
	
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		print("center at X: ", x + w, "Y: ", y + h)
		
	
	if anterior != len(faces):
		anterior = len(faces)
		log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
	
	
    # Display the resulting frame
	#cv2.imshow('Video', frame)
	
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
    # Display the resulting frame
	#cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
