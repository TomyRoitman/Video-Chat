import pygame

class Text:

    def __init__(self, screen, text, x, y, text_color, text_size=20, font_name="arial", bold=False, background_color=None):
        self.screen = screen
        self.text = text
        self.x = x
        self.y = y
        self.background_color = background_color
        self.text_color = text_color
        self.text_size = text_size
        self.font_name = font_name
        self.bold = bold

    def draw(self):
        font = pygame.font.SysFont(self.font_name, self.text_size)
        text = font.render(self.text, True, self.text_color, self.background_color)
        text_rect = text.get_rect()
        text_rect.topleft = (self.x, self.y)
        self.screen.blit(text, text_rect)

    def get_size(self):
        font = pygame.font.SysFont(self.font_name, self.text_size)
        text = font.render(self.text, True, self.text_color, self.background_color)
        size = text.get_size()
        return size


