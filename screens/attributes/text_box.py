import pygame

class TextBox:

    def __init__(self, screen, x, y, width, height, state='', color=(176, 176, 176), active_color=(255, 255, 255),
                 border=True, border_color=(0, 0, 0), border_width=2, place_text='', text_name='arial', text_size=20,
                 text_color=(0, 0, 0)):
        self.screen = screen
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.state = state
        self.color = color
        self.active_color = active_color
        self.border = border
        self.border_color = border_color
        self.border_width = border_width
        self.place_text = place_text
        self.text = []
        self.text_name = text_name
        self.text_size = text_size
        self.text_color = text_color
        self.cursor_pos = 0
        self.active = False
        self.hovered = False

    def update(self, pos):
        if self.is_hovered(pos):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self):
        if self.border:
            self.image.fill(self.border_color)
            if self.active:
                pygame.draw.rect(self.image, self.active_color,
                                 (self.border_width, self.border_width,
                                  self.width - (self.border_width * 2), self.height - (self.border_width * 2)))

            else:
                pygame.draw.rect(self.image, self.color,
                                 (self.border_width, self.border_width,
                                  self.width - (self.border_width * 2), self.height - (self.border_width * 2)))

        else:
            if self.active:
                self.image.fill(self.active_color)
            else:
                self.image.fill(self.color)

        if len(self.text) > 0:
            self.show_text()
        else:
            self.show_place_text()
        self.screen.blit(self.image, self.pos)

    def is_hovered(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.width:
            if self.pos[1] < pos[1] < self.pos[1] + self.height:
                return True
        return False

    def show_text(self):
        text = ''.join(self.text)
        font = pygame.font.SysFont(self.text_name, self.text_size, )
        text = font.render(text, False, self.text_color)
        size = text.get_size()
        if size[0] + 10 > self.width + 10:
            x, y = self.width - (size[0] + 10), (self.height // 2) - (size[1] // 2)
        else:
            x, y = 10, (self.height // 2) - (size[1] // 2)

        pos = x, y
        self.image.blit(text, pos)

    def show_place_text(self):
        text = ''.join(self.place_text)
        font = pygame.font.SysFont(self.text_name, self.text_size, )
        text = font.render(text, False, self.text_color)
        size = text.get_size()
        if size[0] + 10 > self.width + 10:
            x, y = self.width - (size[0] + 10), (self.height // 2) - (size[1] // 2)
        else:
            x, y = 10, (self.height // 2) - (size[1] // 2)

        pos = x, y
        self.image.blit(text, pos)

    def click(self):
        self.active = True

    def user_input(self, event):
        if event.key != 13 and event.key != 273 and event.key != 274 and event.key != 275 and event.key != 276 \
                and event.key != 8 and event.key != 127:
            self.text.insert(self.cursor_pos, event.unicode)
            self.cursor_pos += 1
        elif event.key == 8 and self.cursor_pos > 0 and len(self.text) > 0:
            del self.text[self.cursor_pos - 1]
            self.cursor_pos -= 1
        elif event.key == 276 and self.cursor_pos > 0:
            self.cursor_pos -= 1
        elif event.key == 275 and self.cursor_pos < len(self.text):
            self.cursor_pos += 1
        elif event.key == 127 and self.cursor_pos < len(self.text):
            del self.text[self.cursor_pos]