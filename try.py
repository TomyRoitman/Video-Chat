# import numpy as np
# from PIL import ImageGrab
# import cv2
#
# while True:
#     printscreen_pil = ImageGrab.grab()
#     printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8') \
#         .reshape((printscreen_pil.size[1], printscreen_pil.size[0], 3))
#     cv2.imshow('screens', printscreen_numpy)
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break
#
# import struct
# packed = struct.pack('!i', 1123)
# print(packed)
#
# unpacked = struct.unpack('!i', packed)[0]
# print(type(unpacked))
# print(unpacked)
#
DISPLAY_SIZE = [1280, 720]

import pygame

from screens.main_menu import MainMenuWindow
from screens.insert_ID import InsertID
pygame.init()
pygame.display.set_caption("Video Chat")
screen = pygame.display.set_mode(DISPLAY_SIZE)
insert_ID_screen = InsertID(screen)

while insert_ID_screen.running:
    insert_ID_screen.run()

print("ID: ", insert_ID_screen.ID)
