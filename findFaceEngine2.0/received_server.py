#!/usr/bin/env python3
import socket
import cv2
import pickle
import struct
import os

<<<<<<< HEAD
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
HOST = "130.127.134.19"
PORT = 65432
=======
#HOST = ''
PORT = 8486
HOST = '130.127.134.18'  # The server's hostname or IP address

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')
>>>>>>> e26ccf5d9d3e25180402aa54b5e03cef773f2040

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

dirName = '/users/dit55/CS179I_Offloading/findFaceEngine2.0/storageData'  # create a directory to store images
try:
    os.mkdir(dirName)  # Create target Directory
except FileExistsError:
    print("Directory ", dirName, " already exists")

a = 0
count = 0
data = b""
payload_size = struct.calcsize(">L")
# print("payload_size: {}".format(payload_size))
while True:

    # get data and unpack
    while len(data) < payload_size:
        # print("Recv: {}".format(len(data)))
        data += conn.recv(4096)
        if not data:
            break
    if len(data) == 0:
        break
    # print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    # print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    fileName = (dirName + "/Result{}.jpg").format(a)
    cv2.imwrite(fileName, frame)    # write frame into jpg image
    a = a + 1


#os.system('rm -rf ' + dirName)
conn.close()
s.close()

