#!/usr/bin/env python3

import socket
import os

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
HOST = "130.127.134.17"
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, address = s.accept()

filename = 'results.txt'
while True:
    received = conn.recv(BUFFER_SIZE)
    if not received:
        break
    print(received)
    with open(filename, "ab") as f:
        f.write(received)
        f.flush()

# close the client socket
conn.close()
# close the server socket
s.close()

