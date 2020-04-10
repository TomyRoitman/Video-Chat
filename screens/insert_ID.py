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


class InsertID:

    def __init__(self, screen):
        """
        initialize the variables
        """

        self.screen = screen
        self.background_color = BACKGROUND_COLOR  # White
        self.screen.fill(self.background_color)
        self.running = True
        self.ID = None

        self.title = Text(self.screen, "Video Chat", 0, 100, (255, 255, 255), text_size=200)
        title_size = self.title.get_size()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.title.x = (screen_width - title_size[0]) // 2

        join_button_width = 200
        ID_text_box_width = 350
        y = 400
        height = 75
        self.join_button = Button(self.screen, (screen_width - ID_text_box_width - join_button_width) // 2
                                  + ID_text_box_width, y, join_button_width, height, function=self.join_call, text="Join",
                                  bold_text=True, hover_color=(255, 0, 0), font_size=45)

        self.ID_text_box = TextBox(self.screen, (screen_width - ID_text_box_width - join_button_width) // 2,
                                   y, ID_text_box_width, 75,
                                     text_size=35, place_text='Enter chat ID')

    def run(self):
        self.events()
        self.update()
        self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.join_button.hovered:
                    self.join_button.click()
                if self.ID_text_box.hovered:
                    self.ID_text_box.click()
            if event.type == pygame.KEYDOWN:
                self.ID_text_box.user_input(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.join_button.update(mouse_pos)
        self.ID_text_box.update(mouse_pos)

    def draw(self):
        self.join_button.draw()
        self.ID_text_box.draw()
        self.title.draw()
        pygame.display.update()

    def join_call(self):
        self.ID = "".join(self.ID_text_box.text)
        self.running = False
