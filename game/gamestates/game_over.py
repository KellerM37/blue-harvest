import pygame
import pygame_gui
from pygame_gui.elements import *
from data.settings import *
from .base_state import BaseGamestate

class GameOver(BaseGamestate):
    def __init__(self, ui_manager, state_manager):
        super().__init__("game_over", state_manager)
        
        self.ui_manager = ui_manager
        self.state_manager = state_manager

    def start(self):
        self.game_over_label = UILabel(pygame.Rect(0, -125, -1, -1),
                                       "Game Over!",
                                       self.ui_manager,
                                       object_id="#game_over",
                                       anchors={"centerx": "centerx", "centery": "centery"})
        self.retry_button = UIButton(pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2, 150, 50),
                                     "Retry",
                                     self.ui_manager)
        self.quit_button = UIButton(pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50),
                                    "Main Menu",
                                    self.ui_manager)
        self.kill_count = UILabel(pygame.Rect(0, -50, -1, -1),
                                  f"Kills: {None}",
                                  self.ui_manager,
                                  object_id="#kill_count",
                                  anchors={"centerx": "centerx", "centery": "centery"})

    def end(self):
        self.game_over_label.kill()
        self.retry_button.kill()
        self.quit_button.kill()
        self.kill_count.kill()

    def update(self, dt):
        self.ui_manager.update(dt)

    def run(self, screen, dt):
        self.update(dt)
        screen.fill(("#1a0000"))
        self.ui_manager.draw_ui(screen)
        for event in pygame.event.get():
            self.ui_manager.process_events(event)
            if event.type == pygame.QUIT:
                self.time_to_quit = True
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.retry_button:
                    self.transition = True
                    self.new_state = "game_state"
                if event.ui_element == self.quit_button:
                    self.transition = True
                    self.new_state = "main_menu"