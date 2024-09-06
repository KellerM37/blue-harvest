from os import name
import pygame
import pygame_gui
import json
from pygame_gui.elements import *
from data.settings import *
from .base_state import BaseGamestate
from saves import *

class GameOver(BaseGamestate):
    def __init__(self, ui_manager, state_manager):
        super().__init__("game_over", state_manager)
        
        self.ui_manager = ui_manager
        self.state_manager = state_manager
        self.leaderboard = {}
        self.is_hi_score = False

    def start(self):

        # Score dependent UI elements
        self.load_leaderboard()
        self.hi_score = self.get_hi_score()
        if self.state_manager.states["game_state"].player.score > self.hi_score:
            self.is_hi_score = True
            self.hi_score_label = UILabel(pygame.Rect(0, -100, -1, -1),
                                         "New High Score!",
                                         self.ui_manager,
                                         object_id="#game_title",
                                         anchors={"centerx": "centerx", "centery": "centery"})
            self.hi_score_label.rebuild()
            self.hi_score_label.set_position((SCREEN_WIDTH // 2 - self.hi_score_label.rect.width // 2, 25))

        self.name_input = UITextEntryLine(pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50),
                                              self.ui_manager,
                                              placeholder_text="Enter your name")
        self.submit_button = UIButton(pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 100, 150, 50),
                                            "Submit",
                                            self.ui_manager)

        self.game_over_label = UILabel(pygame.Rect(0, -125, -1, -1),
                                       "Game Over!",
                                       self.ui_manager,
                                       object_id="#game_over",
                                       anchors={"centerx": "centerx", "centery": "centery"})
        self.retry_button = UIButton(pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 200, 150, 50),
                                     "Retry",
                                     self.ui_manager,
                                     visible=False if self.is_hi_score else True)
        self.quit_button = UIButton(pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 250, 150, 50),
                                    "Main Menu",
                                    self.ui_manager,
                                    visible=False if self.is_hi_score else True)
        self.kill_count = UILabel(pygame.Rect(0, -50, -1, -1),
                                  f"Kills: {self.state_manager.states['game_state'].kill_count}",
                                  self.ui_manager,
                                  object_id="#kill_count",
                                  anchors={"centerx": "centerx", "centery": "centery"})
        
    def end(self):
        self.game_over_label.kill()
        self.retry_button.kill()
        self.quit_button.kill()
        self.name_input.kill()
        self.submit_button.kill()
        self.kill_count.kill()

    def update(self, dt):
        self.ui_manager.update(dt)

    def load_leaderboard(self):
        try:
            with open("saves/leaderboard.json", "r") as file:
                self.leaderboard = json.load(file)
                # Convert scores to integers
                self.leaderboard = {name: int(score) for name, score in self.leaderboard.items()}
                self.leaderboard = dict(sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.leaderboard = {}
        
    def get_hi_score(self):
        if self.leaderboard:
            return max(self.leaderboard.values())
        return 0
    
    def save_leaderboard(self, name, score):
        if name in self.leaderboard:
            if self.is_hi_score:
                self.leaderboard[name] = score
        with open("saves/leaderboard.json", "w") as file:
            json.dump(self.leaderboard, file)

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
                    self.state_manager.states["game_state"].reset()
                if event.ui_element == self.quit_button:
                    self.transition = True
                    self.new_state = "main_menu"
                if event.ui_element == self.submit_button:
                    if self.name_input.get_text() != "":
                        if self.name_input.get_text() not in self.leaderboard:
                            self.leaderboard[self.name_input.get_text()] = self.state_manager.states["game_state"].player.score
                            self.save_leaderboard(self.name_input.get_text(), self.state_manager.states["game_state"].player.score)
                        if self.name_input.get_text() in self.leaderboard and self.state_manager.states["game_state"].player.score > self.leaderboard[self.name_input.get_text()]:
                            self.leaderboard[self.name_input.get_text()] = self.state_manager.states["game_state"].player.score
                            self.save_leaderboard(self.name_input.get_text(), self.state_manager.states["game_state"].player.score)
                            if self.is_hi_score:
                                self.hi_score_label.kill()
                        self.transition = True
                        self.new_state = "main_menu"
                        self.state_manager.states["game_state"].reset()