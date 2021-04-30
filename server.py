import cv2
import socket
import struct
import pickle

HOST = ''
PORT = 8000

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket Created')

# bind and listen
s.bind((HOST, PORT))
print('Socket Binding Done')
s.listen(10)
print('Socket listening')

# accept connection
conn, address = s.accept()

data = b''  # convert data to byte
payload_size = struct.calcsize("L")

while True:
    try:
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        # print(frame)

        cv2.imshow('frame', frame)
        cv2.waitKey(10)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        s.close()
        break


