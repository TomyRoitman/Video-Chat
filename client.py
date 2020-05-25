import time

import cv2
import pygame

from video_manager import Camera
from screens.video_chat import ChatWindow
from screens.main_menu import MainMenuWindow
from screens.init_waiting import InitializerWaitingWindow
from screens.insert_ID import InsertID
import socket
from network.TCP_communication import TCPStream
from network.UDP_communication import UDPStream
import threading

FPS = 24
UDP_IP = '0.0.0.0'
UDP_PORT = 10000
MSG_CODE_SIZE = 4
MSG_SIZE_HEADER_SIZE = 8
MSG_CHUNK_SIZE = 1024
SERVER_IP = '192.168.1.41'
SERVER_PORT = 11233
DISPLAY_SIZE = [1280, 720]


def main():
    # initialize pygame display
    pygame.init()
    pygame.display.set_caption("Video Chat")
    screen = pygame.display.set_mode(DISPLAY_SIZE)

    # run main menu
    main_menu_screen = MainMenuWindow(screen)
    while main_menu_screen.running:
        main_menu_screen.run()
        time.sleep(1.0 / FPS)
    choice = main_menu_screen.choice
    username = main_menu_screen.username
    print("Choice: " + choice)
    print("Username: " + username)

    # address server to get participant's address

    server_socket = socket.socket()
    server_socket.connect((SERVER_IP, SERVER_PORT))

    # create object to communicate with TCP protocol
    tcp_stream = TCPStream(server_socket)

    msg_code = choice
    msg = ""
    ID = ""
    dst_ip, dst_port, dst_username = 0, 0, 0
    if choice == "INIT":
        msg = "PORT={},USERNAME={}".format(UDP_PORT, username)
        tcp_stream.send_by_size(msg_code, msg)
        response = tcp_stream.recv_by_size()
        if response[0] != 'VCID':
            print("Something failed...")
            return
        ID = int(response[2])
        tcp_stream.send_by_size("CONF", "OK")
        waiting_screen = InitializerWaitingWindow(screen, ID)
        waiting = True
        while waiting:
            response = tcp_stream.recv_by_size_with_timeout(1.0 / FPS)
            if response != "Not received yet":
                break
            waiting_screen.run()
            time.sleep(1.0 / FPS)

        params = response[2].split(",")
        print(params)
        dst_ip = params[0].split("=")[1]
        dst_port = int(params[1].split("=")[1])
        dst_username = params[2].split("=")[1]

        # now move to chat screen

    # if user wants to join, get his call ID
    if choice == "JOIN":
        insert_ID_screen = InsertID(screen)
        while insert_ID_screen.running:
            insert_ID_screen.run()
        ID = insert_ID_screen.ID

        msg = "ID={},PORT={},USERNAME={}".format(ID, UDP_PORT, username)
        tcp_stream.send_by_size(msg_code, msg)
        response = tcp_stream.recv_by_size()
        params = response[2].split(",")
        print(params)
        dst_ip = params[0].split("=")[1]
        dst_port = int(params[1].split("=")[1])
        dst_username = params[2].split("=")[1]


    chat_screen = ChatWindow(screen, username, dst_username)
    user_camera = Camera()
    udp_stream = UDPStream(UDP_IP, UDP_PORT, FPS)

    frame_receiver = threading.Thread(target=udp_stream.recv_frame)  # , args=(dst_ip, dst_port))
    frame_receiver.start()

    lock = threading.Lock()
    last_participant_frame = 0
    while chat_screen.running:

        # handle user output

        user_output = user_camera.export_update_frame()
        if user_output is not None:
            udp_stream.send_frame(user_output[1], dst_ip, dst_port)
            chat_screen.update_user_input(user_output[0])

        lock.acquire()
        if udp_stream.received_frames > last_participant_frame:
            chat_screen.update_participant_input(udp_stream.participant_frame)
            last_participant_frame += 1
        lock.release()
        chat_screen.run()
        # print("FPS: ", user_window.get_fps())
        # time.sleep(1 / FPS)
        # pygame.time.wait(int((1.0 / FPS) * 1000))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
