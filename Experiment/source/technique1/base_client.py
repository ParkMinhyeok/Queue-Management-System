import zmq
import cv2
import numpy as np
import time

context = zmq.Context()
socket = context.socket(zmq.DEALER)
socket.connect("tcp://localhost:5555")

client_id = b"CLIENT_A"
socket.setsockopt(zmq.IDENTITY, client_id)

cap = cv2.VideoCapture(0)

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    _, buffer = cv2.imencode('.jpg', frame)
    socket.send(buffer.tobytes())

    message = socket.recv()
    print(message)
    time.sleep(0.1)

    count += 1
    if count % 100 == 0:
        print(count)


cap.release()
cv2.destroyAllWindows()
