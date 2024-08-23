import pygame
from .base_state import BaseGamestate

class MainMenu(BaseGamestate):
    def __init__(self, state_manager):
        super().__init__("main_menu", state_manager)

        self.state_manager = state_manager

    def start(self):
        pass

    def run(self, screen, dt):
        for event in pygame.event.get():
            # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True