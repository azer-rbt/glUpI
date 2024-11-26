import pygame
from enum import Enum
from .image import *

class Shape:
    def __init__(self, name):
        self.name = name
        self.enabled = True
        self.x = 0
        self.y = 0
        self.color = (255, 255, 255)
        self.z_index = 0
    def set_enabled(self, enabled):
        self.enabled = enabled
        return self
    def toggle_enabled(self):
        self.enabled = not self.enabled
        return self
    def set_position(self, x, y):
        self.x = x
        self.y = y
        return self
    def set_x(self, x):
        self.x = x
        return self
    def set_y(self, y):
        self.y = y
        return self
    def move(self, x, y):
        self.x += x
        self.y += y
        return self
    def set_color(self, color):
        self.color = color
        return self
    def set_z_index(self, z):
        self.z_index = z
        return self

    def get_z_index(self):
        return self.z_index

    def draw(self, win):
        ...

class Rectangle(Shape):
    def __init__(self, name):
        super().__init__(name)
        self.w = 0
        self.h = 0
    def set_size(self, w, h):
        self.w = w
        self.h = h
        return self
    def set_width(self, w):
        self.w = w
        return self
    def set_height(self, h):
        self.h = h
        return self

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

class TextAlignment(Enum):
    Left = 0
    Center = 1
    Right = 2

class Text(Shape):
    def __init__(self, name):
        super().__init__(name)
        self.text = ""
        self.antialias = True
        self.alignment = TextAlignment.Left
        self.font_name = "Arial"
        self.font_size = 16
        self.font = None; self.reload_font()
        self.render = None; self.render_text()
    def set_text(self, text):
        self.text = text
        self.render_text()
        return self
    def set_antialias(self, aa):
        self.antialias = aa
        self.render_text()
        return self
    def set_alignment(self, align):
        self.alignment = align
        return self
    def reload_font(self):
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.render_text()
    def render_text(self):
        self.render = self.font.render(self.text, self.antialias, self.color)
    def set_font_name(self, name):
        self.font_name = name
        self.reload_font()
        return self
    def set_font_size(self, size):
        self.font_size = size
        self.reload_font()
        return self
    def set_font(self, name, size):
        self.font_name = name
        self.font_size = size
        self.reload_font()
        return self

    def set_all(self, text, font_name, size, antialias=None):
        self.text = text
        self.font_name = font_name
        self.font_size = size
        if antialias is not None: self.antialias = antialias
        self.reload_font()
        return self

    def get_width(self):
        return self.render.get_width()
    def get_height(self):
        return self.render.get_height()
    def get_text(self):
        return self.text

    def draw(self, win: pygame.Surface):
        x = self.x
        if self.alignment == TextAlignment.Left:
            x = self.x
        elif self.alignment == TextAlignment.Center:
            x = self.x - self.render.get_width() // 2
        elif self.alignment == TextAlignment.Right:
            x = self.x - self.render.get_width()
        win.blit(self.render, (x, self.y))

class Alignment(Enum):
    TopLeft = 0
    Top = 1
    TopRight = 2
    Left = 3
    Center = 4
    Right = 5
    BottomLeft = 6
    Bottom = 7
    BottomRight = 8

class Image(Shape):
    def __init__(self, name):
        super().__init__(name)
        self.image: pygame.Surface = None
        self.alignment: Alignment = Alignment.TopLeft
    def set_image(self, img):
        self.image = pillow_to_pg_image(img)
        return self
    def set_image_pygame(self, img):
        self.image = img
        return self
    def set_image_path(self, path: str):
        self.image = pygame.image.load(path).convert()
        return self
    def set_size(self, w, h):
        self.image = pygame.transform.scale(self.image, (w, h))
        return self
    def set_width(self, w, keep_ratio=False):
        h = self.image.get_height()
        if keep_ratio:
            h *= w / self.image.get_width()
        self.image = pygame.transform.scale(self.image, (w, h))
        return self
    def set_height(self, h, keep_ratio=False):
        w = self.image.get_width()
        if keep_ratio:
            w *= h / self.image.get_height()
        self.image = pygame.transform.scale(self.image, (w, h))
        return self
    def set_alignment(self, align):
        self.alignment = align
        return self

    def get_width(self):
        return self.image.get_width()
    def get_height(self):
        return self.image.get_height()

    def draw(self, win):
        if self.image is None:
            return

        x, y = self.x, self.y

        if self.alignment in [Alignment.Top, Alignment.Center, Alignment.Bottom]:
            x = self.x - self.image.get_width() // 2
        elif self.alignment in [Alignment.TopRight, Alignment.Right, Alignment.BottomRight]:
            x = self.x - self.image.get_width()

        if self.alignment in [Alignment.Left, Alignment.Center, Alignment.Right]:
            y = self.y - self.image.get_height() // 2
        elif self.alignment in [Alignment.BottomLeft, Alignment.Bottom, Alignment.BottomRight]:
            y = self.y - self.image.get_height()

        win.blit(self.image, (x, y))
