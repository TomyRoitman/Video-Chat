import pygame
from screens.attributes.button import Button
from screens.attributes.text_box import TextBox
from screens.attributes.text import Text

DISPLAY_SIZE = [1280, 720]
BACKGROUND_COLOR = (0, 51, 255)
FRAME_HEIGHT = 480
FRAME_WIDTH = 640
MARGIN = 20
# Frames location in the following format: (x, y)
USER_INPUT_LOCATION = (0, 0)
PARTICIPANT_INPUT_LOCATION = (DISPLAY_SIZE[0] - FRAME_WIDTH, 0)


class InitializerWaitingWindow:

    def __init__(self, screen, ID):
        """
        initialize the variables
        """

        self.screen = screen
        self.background_color = BACKGROUND_COLOR
        self.screen.fill(self.background_color)
        self.running = True
        self.ID = ID
        self.title = Text(self.screen, "Video Chat", 0, 100, (255, 255, 255), text_size=200)
        title_size = self.title.get_size()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.title.x = (screen_width - title_size[0]) // 2

        self.text1 = Text(self.screen, "Chat ID: {}".format(self.ID), 0, 400,
                         (255, 255, 255), text_size=100)
        text1_size = self.text1.get_size()
        self.text1.x = (screen_width - text1_size[0]) // 2
        self.text2 = Text(self.screen, "Waiting for participant to connect...", 0, 600,
                         (255, 255, 255), text_size=50)
        text2_size = self.text2.get_size()
        self.text2.x = (screen_width - text2_size[0]) // 2


    def run(self):
        self.events()
        self.update()
        self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.title.draw()
        self.text1.draw()
        self.text2.draw()
        pygame.display.update()

