import pygame
from game.data import settings

class BaseGamestate:
    def __init__(self, name, state_manager):
        self.name = name
        self.state_manager = state_manager
        self.transition = False
        self.new_state = None
        self.time_to_quit = False
        self.state_manager.register_state(self)

    # To be overridden
    def start(self):
        pass
    
    # To be overridden
    def end(self):
        pass

    # To be overridden
    def build_ui(self):
        pass

    # To be overridden
    def update(self, dt):
        pass

    # To be overridden
    def draw(self, screen):
        pass

    # To be overridden
    def run(self, screen, dt):
        pass
            