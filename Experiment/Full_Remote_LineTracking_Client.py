import cv2
import socket
import pickle
import struct
from AlphaBot2 import AlphaBot2

Ab = AlphaBot2()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = 'pc address' 
port = 9999
client_socket.connect((host_ip, port))

maximum = 13
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        data = pickle.dumps(frame)
        message_size = struct.pack("L", len(data))
        client_socket.sendall(message_size + data)

        power_difference_data = client_socket.recv(4)
        power_difference = struct.unpack("f", power_difference_data)[0]

        power_difference = max(min(power_difference, maximum), -maximum)

        if power_difference < 0:
            Ab.setPWMA(maximum + power_difference)
            Ab.setPWMB(maximum)
        else:
            Ab.setPWMA(maximum)
            Ab.setPWMB(maximum - power_difference)

        Ab.forward()

except KeyboardInterrupt:
    print("Client End")

finally:
    cap.release()
    client_socket.close()
    Ab.stop()
