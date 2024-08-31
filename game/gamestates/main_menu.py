import pygame
import pygame_gui
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_window import UIWindow

from data.settings import *
from .base_state import BaseGamestate

class MainMenu(BaseGamestate):

    def __init__(self, ui_manager, state_manager):
        super().__init__("main_menu", state_manager)

        self.ui_manager = ui_manager
        self.state_manager = state_manager

        self.title_box = None
        self.title_window = None
        self.game_title = None
        self.play_button = None
        self.settings_button = None
        self.quit_button = None

    def start(self):

        # This is currently a disaster. I will fix this later
        self.background = pygame.image.load("ui/20240823_140057.jpg")

        self.game_title = UILabel(pygame.Rect(0, 0, -1, -1),
                                  GAME_TITLE,
                                  self.ui_manager,
                                  object_id="#game_title",
                                  anchors={"centerx": "centerx", "top": "top"})
        game_title_width = self.game_title.rect.width
        game_title_height = self.game_title.rect.height

        title_panel_width = game_title_width + 30
        title_panel_height = game_title_height + 15
        title_panel_x = (SCREEN_WIDTH - title_panel_width) // 2
        self.title_window = UIWindow(pygame.Rect(title_panel_x, SCREEN_HEIGHT * 0.185, title_panel_width, title_panel_height), manager=self.ui_manager)
        self.title_window.change_layer(0)

        game_title_x = (title_panel_width - game_title_width) // 2
        self.game_title.set_container(self.title_window)

        self.game_credits = UILabel(pygame.Rect(title_panel_x + game_title_x, SCREEN_HEIGHT * 0.251, game_title_width, 100), f"Created by: {AUTHOR}", self.ui_manager)
        
        self.play_button = UIButton(pygame.Rect((SCREEN_WIDTH - 150) // 2, 450, 150, 50), "Play", self.ui_manager)
        self.settings_button = UIButton(pygame.Rect((SCREEN_WIDTH - 150) // 2, 500, 150, 50), "Settings", self.ui_manager)
        self.quit_button = UIButton(pygame.Rect((SCREEN_WIDTH - 150) // 2, 550, 150, 50), "Exit", self.ui_manager)


    def end(self):
        self.title_window.kill()
        self.game_title.kill()
        self.play_button.kill()
        self.settings_button.kill()
        self.quit_button.kill()
        self.game_credits.kill()
        

    def run(self, screen, dt):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True

            if keys[pygame.K_ESCAPE]:
                self.time_to_quit = True
            if keys[pygame.K_F12]:
                DEBUG_MODE = False

            self.ui_manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.quit_button:
                    self.time_to_quit = True
                elif event.ui_element == self.play_button:
                    self.new_state = "game_state"
                    self.transition = True
                elif event.ui_element == self.settings_button:
                    self.new_state = "settings_menu"
                    self.transition = True

        self.ui_manager.update(dt)

        screen.blit(self.background, (0, 0))

        self.ui_manager.draw_ui(screen)

