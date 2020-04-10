import socket
import time
import threading
import cv2
import numpy as np

# from video_manager import Camera
# from window_manager import Window
MSG_CODE_SIZE = 4
MSG_SIZE_HEADER_SIZE = 8
MSG_CHUNK_SIZE = 1024
SERVER_IP = '0.0.0.0'
SERVER_PORT = 11233
threads = []
thread_id = 0
users = {}
users_id = 0


class User:
    def __init__(self, msg_code, ip, port):
        self.msg_code = msg_code
        self.ip = ip
        self.port = port
        self.id = None
        self.matched = False
        self.match = ""


def recv_by_size(client_socket):
    msg_code = ""
    while len(msg_code) < MSG_CODE_SIZE:
        msg_code += client_socket.recv(MSG_CODE_SIZE - len(msg_code)).decode()

    size_header = ""
    while len(size_header) < MSG_SIZE_HEADER_SIZE:
        size_header += client_socket.recv(MSG_SIZE_HEADER_SIZE - len(size_header)).decode()

    content_length = int(size_header)
    content = ""
    while len(content) < content_length:
        content += client_socket.recv(content_length - len(content)).decode()

    return msg_code, content_length, content


def split_by_len(seq, length):
    return [seq[x: x + length] for x in range(0, len(seq), length)]


def send_by_size(client_socket, msg_code, content):
    header_to_send = msg_code + str(len(content)).zfill(MSG_SIZE_HEADER_SIZE)
    header_to_send = header_to_send.encode()
    client_socket.send(header_to_send)
    chunks = split_by_len(content, MSG_CHUNK_SIZE)
    for chunk in chunks:
        client_socket.send(chunk.encode())


def interpret_entry(msg):
    print(msg)
    params = msg.split(",")
    if "," in msg:
        id = params[0].split("=")[1]
        port = params[1].split("=")[1]
        return id, port
    else:
        port = msg.split("=")[1]
        print(port)
        return port


def export_user_info(user):
    return "ip={},port={}".format(user.ip, user.port)


def handle_client(client_socket, address):
    global users
    global users_id
    ip_address = address[0]
    msg_code, content_length, content = recv_by_size(client_socket)
    print(msg_code, content_length, content)
    id = ""
    lock = threading.Lock()
    new_user = ""
    if msg_code == "INIT":  # Initialize call
        # Save user in the global dictionary
        port = int(interpret_entry(content))
        new_user = User(msg_code, ip_address, port)
        lock.acquire()
        users_id += 1
        users[users_id] = new_user
        new_user.id = users_id
        lock.release()


    elif msg_code == "JOIN":
        # Save user in the global dictionary
        id, port = interpret_entry(content)
        port = int(port)
        id = int(id)
        new_user = User(msg_code, ip_address, int(port))
        lock = threading.Lock()
        lock.acquire()
        users_id += 1
        users[users_id] = new_user
        new_user.id = users_id
        lock.release()

    if msg_code == "INIT":
        lock.acquire()
        found = new_user.matched
        lock.release()
        while not found:
            lock.acquire()
            found = new_user.matched
            lock.release()
        print("Sending -> INIT")
        send_by_size(client_socket, "PART", new_user.match)
        print("INIT _> Sent")
        client_socket.close()

    elif msg_code == "JOIN":
        lock.acquire()
        users[id].match = export_user_info(new_user)
        users[id].matched = True
        send_by_size(client_socket, "PART", export_user_info(users[id]))
        lock.release()
        client_socket.close()


def main():
    global threads
    global thread_id
    server_socket = socket.socket()
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(10)
    run = True
    while run:
        client_socket, address = server_socket.accept()
        new_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread_id += 1
        threads.append(new_thread)
        new_thread.start()

    for thread in threads:
        thread.join()
    server_socket.close()

if __name__ == '__main__':
    main()
## Face cascade to detect faces
# face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
#
# # Load the video
# camera = cv2.VideoCapture(0)
#
# # Keep looping
# while True:
#     # Grab the current paintWindow
#     (grabbed, frame) = camera.read()
#     frame = cv2.flip(frame, 1)
#     frame2 = np.copy(frame)
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # Add the 'Next Filter' button to the frame
#     frame = cv2.rectangle(frame, (500,10), (620,65), (235,50,50), -1)
#     cv2.putText(frame, "HEY THERE", (512, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
#
#     # Detect faces
#     faces = face_cascade.detectMultiScale(gray, 1.25, 6)
#     for (x, y, w, h) in faces:
#         # Grab the face
#         gray_face = gray[y:y+h, x:x+w]
#         color_face = frame[y:y+h, x:x+w]
#         # Normalize to match the input format of the model - Range of pixel to [0, 1]
#         gray_normalized = gray_face / 255
#         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (235, 50, 50), -1)
#
#     cv2.imshow("Selfie Filters", frame)
#
#     # If the 'q' key is pressed, stop the loop
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
#
#     time.sleep(1/25)
#
#
# # Cleanup the camera and close any open windows
# camera.release()
# cv2.destroyAllWindows()
