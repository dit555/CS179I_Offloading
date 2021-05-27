#!/usr/bin/env python3

import socket

HOST = '130.127.134.18'  # The server's hostname or IP address
PORT = 65431        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    sii = "lkajsd"
    s.sendall(str.encode(sii))
    data = s.recv(1024)

print(sii, repr(data))
