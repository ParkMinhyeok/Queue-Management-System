# 위 코드는 서버에 접속하여 지속적으로 웹캠 데이터를 전송한다.
# client_id 변수를 통해 자신의 ID를 변경할 수 있다. --> 서버 측에서 전송할 때 필요

import zmq
import cv2
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.DEALER)
socket.connect("tcp://localhost:5555")

client_id = b"CLIENT_A"
socket.setsockopt(zmq.IDENTITY, client_id)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    _, buffer = cv2.imencode('.jpg', frame)
    socket.send(buffer.tobytes())

    message = socket.recv()
    print(message)

cap.release()
cv2.destroyAllWindows()
