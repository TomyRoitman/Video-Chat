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
from audio_manager import Audio
import threading

FPS = 24
UDP_IP = '0.0.0.0'
UDP_VIDEO_PORT = 10000
UDP_AUDIO_PORT = 10001
MSG_CODE_SIZE = 4
MSG_SIZE_HEADER_SIZE = 8
MSG_CHUNK_SIZE = 1024
SERVER_IP = '192.168.1.41'
SERVER_PORT = 11233
DISPLAY_SIZE = [1280, 720]
AUDIO_SECONDS = 2

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
    dst_ip, dst_video_port, dst_sound_port, dst_username = 0, 0, 0, 0
    if choice == "INIT":
        msg = "VPORT={},SPORT={},USERNAME={}".format(UDP_VIDEO_PORT, UDP_AUDIO_PORT, username)
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
        dst_video_port = int(params[1].split("=")[1])
        dst_sound_port = int(params[2].split("=")[1])
        dst_username = params[3].split("=")[1]

        # now move to chat screen

    # if user wants to join, get his call ID
    if choice == "JOIN":
        insert_ID_screen = InsertID(screen)
        while insert_ID_screen.running:
            insert_ID_screen.run()
        ID = insert_ID_screen.ID

        msg = "ID={},VPORT={},SPORT={},USERNAME={}".format(ID, UDP_VIDEO_PORT, UDP_AUDIO_PORT, username)
        tcp_stream.send_by_size(msg_code, msg)
        response = tcp_stream.recv_by_size()
        params = response[2].split(",")
        print(params)
        dst_ip = params[0].split("=")[1]
        dst_video_port = int(params[1].split("=")[1])
        dst_sound_port = int(params[2].split("=")[1])
        dst_username = params[3].split("=")[1]

    # initiate chat screen
    chat_screen = ChatWindow(screen, username, dst_username)

    # initiate camera object
    user_camera = Camera()

    # initiate udp_stream object
    udp_stream = UDPStream(UDP_IP, UDP_VIDEO_PORT, UDP_AUDIO_PORT, FPS)

    # initiate method on a new thread to receive frames from participant
    frame_receiver = threading.Thread(target=udp_stream.recv_frame)  # , args=(dst_ip, dst_port))
    frame_receiver.start()

    # initiate video variables
    last_participant_frame = 0

    lock = threading.Lock()

    # initiate an audio object
    user_audio = Audio(seconds=AUDIO_SECONDS)

    # initiate method on a new thread to receive sound from participant
    sound_receiver = threading.Thread(target=udp_stream.recv_track)
    sound_receiver.start()

    # initiate method on a new thread to record user sound
    sound_recorder = threading.Thread(target=user_audio.sound_recorder)
    sound_recorder.start()

    # initiate sound variables
    last_participant_track = 0

    start_time = time.time()
    to_start = False
    print('1')
    while chat_screen.running:
        # while udp_stream.received_frames < 1:
        #     start_time = time.time()

        if not to_start:
            if time.time() - start_time > AUDIO_SECONDS + 0.98:
                to_start = True

        # handle user video stream
        user_output = user_camera.export_update_frame()
        if user_output:
            udp_frame_sender = threading.Thread(target=udp_stream.send_frame,

                                                args=(user_output[1], dst_ip, dst_video_port))
            udp_frame_sender.start()
            # udp_stream.send_frame(user_output[1], dst_ip, dst_port)
            chat_screen.add_user_input(user_output[0])

        # handle participant video stream
        lock.acquire()
        if udp_stream.received_frames > last_participant_frame:
            chat_screen.add_participant_input(udp_stream.participant_frame)
            last_participant_frame += 1
        lock.release()

        # handle user sound stream
        lock.acquire()
        user_audio_output = user_audio.export_sound()
        if user_audio_output is not None:
            udp_track_sender = threading.Thread(target=udp_stream.send_track, args=(user_audio_output, dst_ip, dst_sound_port))
            udp_track_sender.start()
        lock.release()

        # handle participant sound stream
        lock.acquire()
        if udp_stream.received_tracks > last_participant_track:
            participant_track = udp_stream.participant_track
            user_audio.add_track(participant_track)
            last_participant_track += 1
        lock.release()

        if to_start:
            chat_screen.run(participant=True)
        else:
            chat_screen.run()

        # delay between each of the screen updates
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        time.sleep(1.0 / FPS)


if __name__ == '__main__':
    main()
