#!/usr/bin/env python3
import socket
import cv2
import pickle
import struct
import os
HOST = '130.127.134.18'
PORT = 8485

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

#conn, addr = s.accept()
dirName = 'data'  # create a directory to store images
try:
    os.mkdir(dirName)  # Create target Directory
except FileExistsError:
    print("Directory ", dirName, " already exists")

conn, addr = s.accept()
a = 0
data = b""
payload_size = struct.calcsize(">L")
#print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        #print("Recv: {}".format(len(data)))
        data += conn.recv(4096)
        if not data:
            break
    if len(data) == 0:
        break
    #print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    #print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    fileName = (dirName + "/Result{}.jpg").format(a)
    cv2.imwrite(fileName, frame)
    a = a + 1
#os.system('rm -rf ' + dirName)
conn.close()
s.close()

