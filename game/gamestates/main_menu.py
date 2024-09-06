import pygame
import pygame_gui
import json
from pygame_gui.elements import *

from data.settings import *
from .base_state import BaseGamestate
#from saves import *

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

        self.leaderboard = {}

    def start(self):
        self.load_leaderboard()
        self.build_ui()

        # This is currently a disaster. I will fix this later
        self.background = pygame.image.load("ui/game_assets/main_menu_bg.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.hi_score = self.get_hi_score()

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

    def display_leaderboard(self):
        y_offset = 90
        self.leaderboard_elements = []
        for name, score in self.leaderboard.items():
            name = UILabel(pygame.Rect(-100, y_offset, -1, -1),
                f"{name}",
                self.ui_manager,
                parent_element=self.leaderboard_box,
                object_id="#leader_entries",
                anchors={"centerx": "centerx", "top": "bottom", "centerx_target": self.leaderboard_box, "bottom_target": self.leaderboard_box})
            score = UILabel(pygame.Rect(100, y_offset, -1, -1),
                f"{score}",
                self.ui_manager,
                parent_element=self.leaderboard_box,
                object_id="#leader_entries",
                anchors={"centerx": "centerx", "top": "bottom", "centerx_target": self.leaderboard_box, "bottom_target": self.leaderboard_box})
            self.leaderboard_elements.append(name)
            self.leaderboard_elements.append(score)
            y_offset += 30

    def build_ui(self):
        # UI Parent Panels
        self.title_box = UIPanel(pygame.Rect(0, SCREEN_HEIGHT * 0.185, 450, 100),
                                 manager=self.ui_manager,
                                 object_id="#main_menu_title_box",
                                 anchors={"centerx": "centerx", "top": "top"})
        self.button_box = UIPanel(pygame.Rect(0, SCREEN_HEIGHT * 0.6, 180, 180),
                                  manager=self.ui_manager,
                                  object_id="#main_menu_title_box",
                                  anchors={"centerx": "centerx", "top": "top"})
        self.leaderboard_box = UIPanel(pygame.Rect(-380, SCREEN_HEIGHT * 0.32, 320, 382),
                                 manager=self.ui_manager,
                                 object_id="#main_menu_title_box",
                                 anchors={"right": "right", "top": "top"})
        self.ui_parents = [self.title_box, self.button_box, self.leaderboard_box]
        
        # Title box elements and creds
        self.game_title = UILabel(pygame.Rect(0, 0, -1, -1),
                                  GAME_TITLE,
                                  self.ui_manager,
                                  object_id="#game_title",
                                  parent_element=self.title_box,
                                  anchors={"centerx": "centerx", "centery": "centery", "centery_target": self.title_box})
        self.game_credits = UILabel(pygame.Rect(5, -20, -1, -1),
                                    f"Created by: {AUTHOR}",
                                    self.ui_manager,
                                    anchors={"left": "left", "bottom": "bottom"})
        self.title_elements = [self.game_title, self.game_credits]
        
        # Button box elements
        self.play_button = UIButton(pygame.Rect(0, -165, 150, 50),
                                   "Play",
                                   self.ui_manager,
                                   container=self.button_box,
                                   anchors={"centerx": "centerx", "top": "top", "top_target": self.button_box})
        self.settings_button = UIButton(pygame.Rect(0, 50, 150, 50),
                                       "Settings",
                                       self.ui_manager,
                                       container=self.button_box,
                                       anchors={"centerx": "centerx", "bottom": "bottom", "centerx_target": self.play_button, "bottom_target": self.play_button})
        self.quit_button = UIButton(pygame.Rect(0, 50, 150, 50),
                                   "Exit",
                                   manager=self.ui_manager,
                                   container=self.button_box,
                                   anchors={"centerx": "centerx", "bottom": "bottom", "centerx_target": self.button_box,"bottom_target": self.settings_button})
        self.button_elements = [self.play_button, self.settings_button, self.quit_button]

        # Leaderboard box elements
        self.leaderboard_title = UILabel(pygame.Rect(0, 40, -1, -1),
                                        "Leaderboard",
                                        self.ui_manager,
                                        object_id="#settings_titles",
                                        parent_element=self.leaderboard_box,
                                        anchors={"centerx": "centerx", "top": "bottom", "centerx_target": self.leaderboard_box, "bottom_target": self.leaderboard_box})
        self.display_leaderboard()

    def end(self):
        for parent in self.ui_parents:
            parent.kill()
        for element in self.title_elements:
            element.kill()
        for element in self.button_elements:
            element.kill()
        for element in self.leaderboard_elements:
            element.kill()
        self.leaderboard_title.kill()
        

    def run(self, screen, dt):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            self.ui_manager.process_events(event)
            # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True
            if keys[pygame.K_ESCAPE]:
                self.time_to_quit = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.quit_button:
                    self.time_to_quit = True
                elif event.ui_element == self.play_button:
                    self.new_state = "game_state"
                    self.transition = True
                elif event.ui_element == self.settings_button:
                    self.new_state = "settings_menu"
                    self.transition = True


        screen.blit(self.background, (0, 0))
        self.ui_manager.update(dt)
        self.ui_manager.draw_ui(screen)

        