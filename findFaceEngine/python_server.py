#!/usr/bin/env python3

import socket, os

HOST = '198.72.184.1'  # Standard loopback interface address (localhost)
PORT = 65431        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	with conn:
		print('Connected by', addr)
		while True:
			data = conn.recv(1024)
			if not data:
				break
			#os.system("../MoonGen/build/MoonGen ../MoonGen/examples/pcap/replay-pcap.lua 0 ../test-packet/gtp_icmp_echo_request_256_loop.pcap -l")
			#conn.sendall(data)
			print(data)
