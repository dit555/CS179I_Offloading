import cv2
import socket
import struct
import pickle

Host = 'localhost'
Port = 8000
camera = cv2.VideoCapture(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((Host, Port))

while True:
    ret, frame = camera.read()
    data = pickle.dumps(frame)

    message_size = struct.pack("L", len(data))
    s.sendall(message_size + data)




