import cv2
import pygame
import numpy as np
from screens.attributes.button import Button
from screens.attributes.text_box import TextBox

DISPLAY_SIZE = [1280, 720]
BACKGROUND_COLOR = (255, 255, 255)
FRAME_HEIGHT = 480
FRAME_WIDTH = 640
MARGIN = 20
# Frames location in the following format: (x, y)
USER_INPUT_LOCATION = (0, 0)
PARTICIPANT_INPUT_LOCATION = (DISPLAY_SIZE[0] - FRAME_WIDTH, 0)


class ChatWindow:

    def __init__(self, caption):
        """
        initialize the variables
        """
        pygame.init()
        pygame.display.set_caption(caption)

        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.background_color = BACKGROUND_COLOR  # White
        self.user_input = None
        self.participant_input = None
        self.screen.fill(self.background_color)
        self.running = True
        self.make_buttons()

    def run(self):
        self.events()
        self.update()
        self.draw()

    def make_buttons(self):
        self.button = Button(self.screen, 50, 50, 100, 50, function=self.button_click, text="Press Here",
                             bold_text=True, hover_color=(2, 244, 12))
        self.text_box = TextBox(self.screen, 50, 200, 100, 50, place_text='Type Here')

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.hovered:
                    self.button.click()
                if self.text_box.hovered:
                    self.text_box.click()
            if event.type == pygame.KEYDOWN:
                self.text_box.user_input(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button.update(mouse_pos)
        self.text_box.update(mouse_pos)

    def draw(self):
        self.button.draw()
        self.text_box.draw()
        pygame.display.update()

    def button_click(self):
        print("CLICK")

    def update_user_input(self, frame):
        frame = self.__form_input(frame)
        self.user_input = pygame.surfarray.make_surface(frame)
        self.screen.blit(self.user_input, USER_INPUT_LOCATION)

    def update_participant_input(self, frame):
        frame = self.__form_input(frame)
        self.participant_input = pygame.surfarray.make_surface(frame)
        self.screen.blit(self.participant_input, PARTICIPANT_INPUT_LOCATION)

    def terminate_window(self):
        pygame.quit()

    def __form_input(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        return frame



