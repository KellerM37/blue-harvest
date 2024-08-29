from inspect import FullArgSpec
import pygame
import pygame_gui
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu

from data import settings

from .base_state import BaseGamestate

class SettingsMenu(BaseGamestate):
    def __init__(self, ui_manager, state_manager):
        super().__init__("settings_menu", state_manager)

        self.ui_manager = ui_manager
        self.gamestate_manager = state_manager
        self.res_list_dropdown = ["1920x1080", "1280x720", "800x600"]
        self.new_width = settings.SCREEN_WIDTH
        self.new_height = settings.SCREEN_HEIGHT
        self.new_fullscreen = settings.FULLSCREEN
        self.settings_dict = {
            "resolution": f"{settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}",
            "fullscreen": "Fullscreen" if settings.FULLSCREEN else "Windowed"
        }
        self.new_settings_dict = self.settings_dict

        self.show_apply = False

    # Reset the settings to the default values and update the UI elements
    def defaults(self):
        settings.SCREEN_WIDTH = settings.DEFAULT_SCREEN_WIDTH
        settings.SCREEN_HEIGHT = settings.DEFAULT_SCREEN_HEIGHT
        settings.FULLSCREEN = settings.DEFAULT_FULLSCREEN
        screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN if settings.FULLSCREEN else 0)
        self.update_ui_positions(screen.get_width(), screen.get_height(), self)

    def update_ui_positions(self, screen_width, screen_height, gamestate_manager):
        # Update UI elements in the menu screen
        self.res_dropdown.set_relative_position((screen_width // 2 - self.res_dropdown.rect.width // 2, screen_height // 2 + 50))
        self.apply_button.set_relative_position((screen_width - 160, screen_height - 110))
        self.defaults_button.set_relative_position((0, 0, 150, 50))
        self.back_button.set_relative_position((screen_width - 160, screen_height - 60))
        self.fullscreen_toggle.set_relative_position((screen_width // 2 - self.fullscreen_toggle.rect.width // 2, screen_height // 2 + 100))
        self.gamestate_manager.load_states(self.ui_manager, self.gamestate_manager)
        print("All UI elements have been repositioned")

    # Save the settings to the settings.py file
    def save_settings(self):
        self.settings_dict = {
            "resolution": f"{settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}",
            "fullscreen": "Windowed"
        }
        settings_path = "data/settings.py"
    
    # Read the current settings
        with open(settings_path, "r") as f:
            lines = f.readlines()
    
    # Update the specific settings
        with open(settings_path, "w") as f:
            for line in lines:
                if line.startswith("SCREEN_WIDTH"):
                    f.write(f'SCREEN_WIDTH = {settings.SCREEN_WIDTH}\n')
                elif line.startswith("SCREEN_HEIGHT"):
                    f.write(f'SCREEN_HEIGHT = {settings.SCREEN_HEIGHT}\n')               
                # Currently, the FULLSCREEN setting is not being saved to the settings.py file so it loads faster
                #elif line.startswith("FULLSCREEN"):
                    #f.write(f'FULLSCREEN = {settings.FULLSCREEN}')
                else:
                    f.write(line)

    def end(self):
        self.back_button.kill()
        self.res_dropdown.kill()
        self.apply_button.kill()
        self.fullscreen_toggle.kill()
        self.defaults_button.kill()

    def start(self):
        print(pygame.display.list_modes())

        # This 'convenient' rect is used as a template solely for button size, will likely be removed later
        button_rect = pygame.Rect(0, 0, 150, 50)
        
        # Spawns my UI elements
        self.apply_button = UIButton(relative_rect=button_rect,
                                    text="Apply",
                                    manager=self.ui_manager,
                                    object_id="#settings",
                                    visible=False)                                     
        self.fullscreen_toggle = UIDropDownMenu(["Windowed", "Fullscreen"],
                                                "Fullscreen" if settings.FULLSCREEN else "Windowed",
                                                pygame.Rect(565, 400, 150, 50),
                                                self.ui_manager,
                                                object_id="#settings")
        self.res_dropdown = UIDropDownMenu(self.res_list_dropdown,
                                           f"{settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}",
                                           pygame.Rect(565, 450, 150, 50),
                                           self.ui_manager,
                                           object_id="#settings")
        self.back_button = UIButton(relative_rect=button_rect,
                                    text="Back",
                                    manager=self.ui_manager,
                                    object_id="#settings")
        self.defaults_button = UIButton(relative_rect=button_rect,
                                    text="Defaults",
                                    manager=self.ui_manager,
                                    object_id="#settings")
        
        # I really don't like that I have this line here, but I need to update the UI elements here for now
        self.update_ui_positions(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, self.gamestate_manager)

    def run(self, screen, dt):
        self.new_settings_dict = {
            "resolution": f"{self.new_width}x{self.new_height}",
            "fullscreen": "Fullscreen" if self.new_fullscreen else "Windowed"
        }
        if self.new_settings_dict != self.settings_dict:
            self.apply_button.show()
        else:
            self.apply_button.hide()
        
        for event in pygame.event.get():
        # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True

            # Checks if the player has changed any settings, and shows the apply button if they have
            if self.new_settings_dict != self.settings_dict:
                self.apply_button.show()

            self.ui_manager.process_events(event)

            # If the player changes the resolution or fullscreen settings, set temp values
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.res_dropdown:
                    self.new_width = int(event.text.split("x")[0])
                    self.new_height = int(event.text.split("x")[1])
                    self.new_settings_dict["resolution"] = event.text
                    print(self.new_settings_dict)
                elif event.ui_element == self.fullscreen_toggle:
                    if event.text == "Fullscreen":
                        self.new_fullscreen = True
                    elif event.text == "Windowed":
                        self.new_fullscreen = False

            # Track player input for the buttons
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.apply_button:
                    settings.SCREEN_WIDTH = self.new_width
                    settings.SCREEN_HEIGHT = self.new_height
                    settings.FULLSCREEN = self.new_fullscreen
                    self.save_settings()
                    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN if settings.FULLSCREEN else 0)
                    self.update_ui_positions(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, self)
                elif event.ui_element == self.back_button:
                    self.new_state = "main_menu"
                    self.transition = True
                elif event.ui_element == self.defaults_button:
                    self.defaults()

        self.ui_manager.update(dt)

        screen.fill(("black"))

        self.ui_manager.draw_ui(screen)

        pygame.display.update()
