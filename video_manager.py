import cv2
import numpy as np
from PIL import ImageGrab


class Camera:

    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def export_update_frame(self):
        self.__update_frame()
        return self.export_frame()

    def export_frame(self):
        ret, frame = self.camera.read()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame = np.rot90(frame)
        # frame = cv2.resize(frame, (450, 600), interpolation=cv2.INTER_AREA)
        return frame

    def share_screen(self):
        printscreen_pil = ImageGrab.grab()
        printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8') \
            .reshape((printscreen_pil.size[1], printscreen_pil.size[0], 3))
        return printscreen_numpy[0:480, 0:640]

    def __update_frame(self):
        pass


    def __process_image(self):
        pass