import zmq
import cv2
import numpy as np
from queue import Queue
import threading
import time

q = Queue()
client_identities = []

context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind("tcp://*:5555")


def send_message_to_client(client_id, message):
    socket.send(client_id, zmq.SNDMORE)
    socket.send(message)

def process_thread():
    while True:
        if q.empty():
            # print('empty queue')
            time.sleep(0.01)
            continue

        time.sleep(0.01)
        priority, value = q.get()
        print(f"{priority} poped")

        send_message_to_client(priority, b"Message Recieved")


inference_def = threading.Thread(target=process_thread)
inference_def.start()

while True:
    identity = socket.recv()
    message = socket.recv()

    if identity not in client_identities:
        client_identities.append(identity)
        print(f"New client connected: {identity}")

    q.put((identity, message))

cv2.destroyAllWindows()
