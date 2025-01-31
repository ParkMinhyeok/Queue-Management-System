import cv2
import socket
import pickle
import struct
import numpy as np

last_proportional = 0
integral = 0
setpoint = 80

def calculate_power_difference(cx):
    global last_proportional, integral
    proportional = cx - setpoint
    derivative = proportional - last_proportional
    integral += proportional
    last_proportional = proportional

    power_difference = proportional / 10 + integral / 100000 + derivative * 0.65
    return power_difference

def process_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx = setpoint
    else:
        cx = setpoint

    return cx

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '0.0.0.0'
    port = 9999
    server_socket.bind((host_ip, port))
    server_socket.listen(5)
    print(f"Start Server {host_ip}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected {addr}.")

        data = b""
        payload_size = struct.calcsize("L")

        while True:
            while len(data) < payload_size:
                data += client_socket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)

            cx = process_image(frame)
            power_difference = calculate_power_difference(cx)

            client_socket.sendall(struct.pack("f", power_difference))

        client_socket.close()

if __name__ == "__main__":
    start_server()
