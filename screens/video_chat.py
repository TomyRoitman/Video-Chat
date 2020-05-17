import cv2
import pygame
import numpy as np
from screens.attributes.text import Text

DISPLAY_SIZE = [1280, 720]
BACKGROUND_COLOR = (255, 255, 255)
FRAME_HEIGHT = 480
FRAME_WIDTH = 640
MARGIN = 20
# Frames location in the following format: (x, y)
USER_INPUT_LOCATION = (0, 0)
PARTICIPANT_INPUT_LOCATION = (DISPLAY_SIZE[0] - FRAME_WIDTH, 0)


class ChatWindow:

    def __init__(self, screen, username, participant_username):
        """
        initialize the variables
        """

        self.screen = screen
        self.background_color = BACKGROUND_COLOR  # White
        # Fill background
        self.screen.fill(self.background_color)

        self.user_input = None
        self.username = username

        self.participant_input = None
        self.participant_username = participant_username

        self.running = True

        screen_width, screen_height = pygame.display.get_surface().get_size()
        text_y = 485
        # Make text objects to present both usernames
        self.username_text = Text(self.screen, self.username + " (you)", 0, text_y, (0, 0, 0), text_size=50)
        username_text_size = self.username_text.get_size()
        self.username_text.x = (FRAME_WIDTH - username_text_size[0]) // 2

        self.participant_username_text = Text(self.screen, self.participant_username, 0, text_y, (0, 0, 0), text_size=50)
        participant_username_text_size = self.participant_username_text.get_size()
        self.participant_username_text.x = FRAME_WIDTH + (FRAME_WIDTH - participant_username_text_size[0]) // 2


    def run(self):
        self.events()
        self.update()
        self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if self.button.hovered:
        #             self.button.click()
        #         if self.text_box.hovered:
        #             self.text_box.click()
        #     if event.type == pygame.KEYDOWN:
        #         self.text_box.user_input(event)


    def update(self):
        # mouse_pos = pygame.mouse.get_pos()
        # self.button.update(mouse_pos)
        # self.text_box.update(mouse_pos)
        pass
    def draw(self):
        self.username_text.draw()
        self.participant_username_text.draw()
        pygame.display.update()


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
