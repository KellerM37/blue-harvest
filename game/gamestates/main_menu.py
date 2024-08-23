import pygame
import pygame_gui
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_panel import UIPanel

from data.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from .base_state import BaseGamestate

class MainMenu(BaseGamestate):

    def __init__(self, ui_manager, state_manager):
        super().__init__("main_menu", state_manager)

        self.ui_manager = ui_manager
        self.state_manager = state_manager

        self.title_box = None
        self.title_panel = None
        self.game_title = None
        self.play_button = None
        self.settings_button = None
        self.quit_button = None

    def start(self):

        self.background = pygame.image.load("ui/20240823_140057.jpg")
        self.title_panel = UIPanel(pygame.Rect(430, 125, 420, 100))
        self.game_title = UILabel(pygame.Rect(440, 125, 400, 100), "KLAR GAME", self.ui_manager, object_id="#game_title")
        self.play_button = UIButton(pygame.Rect(565, 450, 150, 50), "Play", self.ui_manager)
        self.settings_button = UIButton(pygame.Rect(565, 500, 150, 50), "Settings", self.ui_manager)
        self.quit_button = UIButton(pygame.Rect(565, 550, 150, 50), "Exit", self.ui_manager)

    def run(self, screen, dt):
        for event in pygame.event.get():
            # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True

            self.ui_manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.quit_button:
                    self.time_to_quit = True

        self.ui_manager.update(dt)

        screen.blit(self.background, (0, 0))

        self.ui_manager.draw_ui(screen)