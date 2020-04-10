# import numpy as np
# from PIL import ImageGrab
# import cv2
#
# while True:
#     printscreen_pil = ImageGrab.grab()
#     printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8') \
#         .reshape((printscreen_pil.size[1], printscreen_pil.size[0], 3))
#     cv2.imshow('window', printscreen_numpy)
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
from window.window_manager import  Window

window = Window("Hello")

while window.running:
    window.run()
