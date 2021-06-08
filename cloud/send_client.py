#!/usr/bin/env python3
import cv2
import socket
import struct
import pickle
from os import path

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('130.127.134.18', 8486))
#client_socket.connect(('localhost', 8486))
connection = client_socket.makefile('wb')

img_counter = 0

last_good = 0  # latest index we found
num = 0  # cur index
max_it = 5
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
def findRecent():
    r = True
    name = ""
    good = ""
    num = last_good
    it = 0  # how many times we have ran since we found a file
    while r:
        name = "/users/dit55/CS179I_Offloading/findFaceEngine2.0/storageData/Result"
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

last_sent = ""
while True:
    name = findRecent()

    if name != "BAD" or name != last_sent:
        frame = cv2.imread(name)
        last_sent = name
        # print(name)
        if frame is None:
            continue
    else:
        #print("no image found")
        continue

    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)

    #print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1



