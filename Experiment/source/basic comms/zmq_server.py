# 위 코드는 여러 대의 클라이언트를 동시 접속이 가능하며 비동기적 양방향 통신이 가능하다.
# target_client_id 변수를 수정하여 송신하고 싶은 클라이언트를 선택할 수 있다.

import zmq
import cv2
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind("tcp://*:5555")

client_identities = {}

def send_message_to_client(client_id, message):
    socket.send(client_id, zmq.SNDMORE)
    socket.send(message)

while True:
    identity = socket.recv()
    message = socket.recv()

    if identity not in client_identities:
        client_identities[identity] = True
        print(f"New client connected: {identity}")
    
    frame = np.frombuffer(message, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    cv2.imshow("Server", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    target_client_id = b'\x00\x80\x00\x00*'
    if identity == target_client_id:
        send_message_to_client(identity, b"Message for B")
    else:
        send_message_to_client(identity, b"Message for A")

cv2.destroyAllWindows()
