import time

import pygame

from video_manager import Camera
from screens.video_chat import ChatWindow
import socket
from network.TCP_communication import TCPStream
from network.UDP_communication import UDPStream
import threading

FPS = 24
UDP_IP = '0.0.0.0'
UDP_PORT = 10001
MSG_CODE_SIZE = 4
MSG_SIZE_HEADER_SIZE = 8
MSG_CHUNK_SIZE = 1024
SERVER_IP = '192.168.1.41'
SERVER_PORT = 11233
DISPLAY_SIZE = [1280, 720]



def main():
    server_socket = socket.socket()
    server_socket.connect((SERVER_IP, SERVER_PORT))

    tcp_stream = TCPStream(server_socket)

    msg_code = "JOIN"
    msg = "ID=1,PORT={},USERNAME=TOMY".format(UDP_PORT)
    tcp_stream.send_by_size(msg_code, msg)
    dst = tcp_stream.recv_by_size()
    print(dst)
    params = dst[2].split(",")
    dst_ip = params[0].split("=")[1]
    dst_port = int(params[1].split("=")[1])

    pygame.init()
    pygame.display.set_caption("Video Chat")
    screen = pygame.display.set_mode(DISPLAY_SIZE)

    user_window = ChatWindow(screen)
    user_camera = Camera()
    udp_stream = UDPStream(UDP_IP, UDP_PORT, FPS)

    frame_receiver = threading.Thread(target=udp_stream.recv_frame) #, args=(dst_ip, dst_port))
    frame_receiver.start()

    lock = threading.Lock()

    while user_window.running:
        # handle user output
        # user_output = user_camera.share_screen()
        # if user_output is not None:
        #     udp_stream.send_frame(user_output, dst_ip, dst_port)
        #     user_window.update_user_input(user_output)

        lock.acquire()
        if udp_stream.participant_frame is not None:
            user_window.update_participant_input(udp_stream.participant_frame)
        lock.release()

        user_window.run()
        # print("FPS: ", user_window.get_fps())
        time.sleep(1 / FPS)

if __name__ == '__main__':
    main()
