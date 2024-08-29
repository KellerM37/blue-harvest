import pygame
import pygame_gui
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu

from data.settings import *

from .base_state import BaseGamestate

class SettingsMenu(BaseGamestate):
    def __init__(self, ui_manager, state_manager):
        super().__init__("settings_menu", state_manager)

        self.ui_manager = ui_manager
        self.state_manager = state_manager
        self.res_list_dropdown = ["1920x1080", "1280x720", "800x600"]

    def end(self):
        print("killing settings")
        self.quit_button.kill()
        self.res_dropdown.kill()

    # To be overridden
    def start(self):
        self.quit_button = UIButton(pygame.Rect(565, 550, 150, 50), "Back", self.ui_manager)
        self.res_dropdown = UIDropDownMenu(self.res_list_dropdown, "1920x1080", pygame.Rect(565, 450, 150, 50), self.ui_manager)

        print("entered settings")

    def run(self, screen, dt):
        for event in pygame.event.get():
        # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True

            self.ui_manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.res_dropdown:
                    print(self.res_dropdown.selected_option)
                elif event.ui_element == self.quit_button:
                    self.new_state = "main_menu"
                    self.transition = True

        self.ui_manager.update(dt)

        screen.fill(("black"))

        self.ui_manager.draw_ui(screen)

    # To be overridden
