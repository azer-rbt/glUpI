import pygame
from .shapes import Shape, Rectangle, Text, TextAlignment, Image as ImgShape, Alignment
from .zeit import Time
from .lambdautils import *

class Window:
    def __init__(self, w, h):
        pygame.init()
        self.win = pygame.display.set_mode((w, h))
        self.clock = pygame.time.Clock()
        self.time = Time()
        self.mainloop = None
        self.startup = None
        self.close = None
        self.background = (0, 0, 0)
        self.shapes: {str, Shape} = {}
    def run(self):
        if self.startup is not None:
            self.startup(self)

        def loop():
            while True:
                self.time.set_delta_time(self.clock.tick(self.time.fps) * 0.001)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                self.win.fill(self.background)

                self.time.check_tasks()

                if self.mainloop is not None:
                    res = self.mainloop(self)
                    if res is False:
                        return

                for name, shape in sorted(self.shapes.items(), key=lambda s: s[1].get_z_index()):
                    if not shape.enabled:
                        continue
                    shape.draw(self.win)

                pygame.display.flip()
        loop()

        if self.close is not None:
            self.close(self)
    def ontick(self, func):
        self.mainloop = func
        return self
    def onstartup(self, func):
        self.startup = func
        return self
    def onclose(self, func):
        self.close = func
        return self
    def set_title(self, title):
        pygame.display.set_caption(title)
        return self
    def set_icon_path(self, path):
        pygame.display.set_icon(pygame.image.load(path))
        return self
    def set_fps(self, fps):
        self.time.set_fps(fps)
        return self
    def set_background(self, bg):
        self.background = bg
        return self

    def get_width(self):
        return self.win.get_width()
    def get_height(self):
        return self.win.get_height()
    def get_size(self):
        return self.win.get_size()

    def get_shape(self, name):
        if not self.shapes.__contains__(name):
            raise Exception(f"No shape called '{name}'")
        return self.shapes[name]
    def create(self, t: type, name: str):
        if self.shapes.__contains__(name):
            raise Exception(f"Shape with name '{name}' already exists")
        self.shapes[name] = t(name)
        return self.shapes[name]
