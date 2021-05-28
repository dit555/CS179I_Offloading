import cv2
import sys
import logging as log
import datetime as dt
import numpy as np
from time import sleep

cascPath = "data.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

overlay_path = "me_gusta_filter.png"
video_capture = cv2.VideoCapture(0)
anterior = 0

while True:
	if not video_capture.isOpened():
		print('Unable to load camera.')
		sleep(5)
		pass

	# Capture frame-by-frame
	ret, frame = video_capture.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
	)
	
	overlay = cv2.imread(overlay_path)
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		center_x = int(x + w/2)
		center_y = int(y + h/2)
		x2 = int(overlay.shape[1]/2)
		y2 = int(overlay.shape[0]/2)
		y_1 = center_y - y2
		y_2 = center_y + y2
		x_1 = center_x - x2
		x_2 = center_x + x2
		frame[y_1:y_2, x_1:x_2] = overlay
		

	if anterior != len(faces):
		anterior = len(faces)


	# Display the resulting frame
	cv2.imshow('Video', frame)


	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	# Display the resulting frame
	cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
