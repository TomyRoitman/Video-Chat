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


class MainMenuWindow:

    def __init__(self, screen):
        """
        initialize the variables
        """

        self.screen = screen
        self.background_color = BACKGROUND_COLOR  # White
        self.screen.fill(self.background_color)
        self.running = True
        self.choice = None
        self.username = None
        self.title = Text(self.screen, "Video Chat", 0, 100, (255, 255, 255), text_size=200)
        title_size = self.title.get_size()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.title.x = (screen_width - title_size[0]) // 2

        self.initialize_button = Button(self.screen, 315, 530, 300, 95, function=self.initiate_call,
                                        text="Initiate call",
                                        bold_text=True, hover_color=(2, 244, 12), font_size=45)
        self.join_button = Button(self.screen, 665, 530, 300, 95, function=self.join_call, text="Join call",
                                  bold_text=True, hover_color=(255, 0, 0), font_size=45)
        name_text_box_width = 350
        self.name_text_box = TextBox(self.screen, (1280 - name_text_box_width) // 2, 400, name_text_box_width, 75,
                                     text_size=35, place_text='Type your name here...')

    def run(self):
        self.events()
        self.update()
        self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.initialize_button.hovered:
                    self.initialize_button.click()
                if self.join_button.hovered:
                    self.join_button.click()
                if self.name_text_box.hovered:
                    self.name_text_box.click()
            if event.type == pygame.KEYDOWN:
                self.name_text_box.user_input(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.initialize_button.update(mouse_pos)
        self.join_button.update(mouse_pos)
        self.name_text_box.update(mouse_pos)

    def draw(self):
        self.initialize_button.draw()
        self.join_button.draw()
        self.name_text_box.draw()
        self.title.draw()
        pygame.display.update()

    def initiate_call(self):
        self.choice = "INIT"
        self.username = "".join(self.name_text_box.text)
        self.running = False

    def join_call(self):
        self.choice = "JOIN"
        self.username = "".join(self.name_text_box.text)
        self.running = False
