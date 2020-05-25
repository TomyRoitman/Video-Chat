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
        frame = self.__image_resize(frame, width=640)
        _, encoded = cv2.imencode('.JPEG', frame)
        return encoded

    def share_screen(self):
        printscreen_pil = ImageGrab.grab()
        printscreen_numpy = np.array(printscreen_pil.getdata(), dtype='uint8') \
            .reshape((printscreen_pil.size[1], printscreen_pil.size[0], 3))
        return printscreen_numpy[0:480, 0:640]

    def __update_frame(self):
        pass

    def __process_image(self):
        pass

    def __image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized
