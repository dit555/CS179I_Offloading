#!/usr/bin/env python3
import cv2
import socket
import struct
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('130.127.134.18', 8485))
#client_socket.connect(('localhost', 8486))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320)
cam.set(4, 240)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    cv2.imshow('Input', frame)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)

    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

