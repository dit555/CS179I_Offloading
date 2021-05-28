#!/usr/bin/env python3
import socket
import os
import time

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

HOST = '130.127.134.17'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

filename = "positions.txt"
old_size = 0
pos = 0


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        new_size = os.stat(filename).st_size
        if new_size > old_size:
            with open(filename, "rb") as f:
                f.seek(pos)
                for line in f:
                    s.send(line)
                pos = f.tell()
            old_size = new_size
        time.sleep(1)


