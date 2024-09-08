
import pygame
import pygame_gui
from pygame_gui.elements.ui_label import UILabel
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu

from game.data import settings

from .base_state import BaseGamestate

class SettingsMenu(BaseGamestate):
    def __init__(self, ui_manager, state_manager):
        super().__init__("settings_menu", state_manager)

        
        self.settings_bg = pygame.image.load("ui/LOGO.jpeg") 

        self.ui_manager = ui_manager
        self.state_manager = state_manager
        self.new_screen_width = settings.SCREEN_WIDTH
        self.new_screen_height = settings.SCREEN_HEIGHT
        self.new_fullscreen = settings.FULLSCREEN
        self.new_debug_mode = settings.DEBUG_MODE
        self.settings_dict = {
            "resolution": f"{settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}",
            "fullscreen": "Fullscreen" if settings.FULLSCREEN else "Windowed",
            "debug_mode": settings.DEBUG_MODE,
            "hitboxes": settings.DEBUG_SHOW_PLAYER_HITBOX
        }
        

        self.show_apply = False

    # Reset the settings to the default values and update the UI elements
    def defaults(self):
        self.new_screen_width = settings.DEFAULT_SCREEN_WIDTH
        self.new_screen_height = settings.DEFAULT_SCREEN_HEIGHT
        self.new_fullscreen = settings.DEFAULT_FULLSCREEN
        self.apply()

    def apply(self):
        settings.SCREEN_WIDTH = self.new_screen_width
        settings.SCREEN_HEIGHT = self.new_screen_height
        settings.FULLSCREEN = self.new_fullscreen
        settings.DEBUG_MODE = self.new_settings_dict["debug_mode"]
        settings.DEBUG_SHOW_PLAYER_HITBOX = self.new_settings_dict["hitboxes"]
        self.save_settings()
        self.update_ui_positions()

    def update_ui_positions(self):
        self.end()
        self.start()

    # Save the settings to the settings.py file
    def save_settings(self):
        self.settings_dict = {
            "resolution": f"{settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}",
            "fullscreen": "Windowed",
            "debug_mode": settings.DEBUG_MODE,
            "hitboxes": settings.DEBUG_SHOW_PLAYER_HITBOX
        }
        settings_path = "game/data/settings.py"
    
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
                elif line.startswith("FULLSCREEN"):
                    f.write(f'FULLSCREEN = {settings.FULLSCREEN}\n')
                elif line.startswith("DEBUG_MODE"):
                    f.write(f'DEBUG_MODE = {settings.DEBUG_MODE}\n')
                elif line.startswith("DEBUG_SHOW_PLAYER_HITBOX"):
                    f.write(f'DEBUG_SHOW_PLAYER_HITBOX = {settings.DEBUG_SHOW_PLAYER_HITBOX}\n')
                else:
                    f.write(line)

    def end(self):
        for x in self.bg_ui_parent, self.left_ui_elements, self.right_ui_elements, self.debug_ui_elements:
            for y in x:
                y.kill()

    def start(self):
        self.new_settings_dict = self.settings_dict.copy()
        # Create the UI Groups. Each box will contain different UI elements
        self.left_ui = UIPanel(pygame.Rect(settings.SCREEN_WIDTH * 0.05,
                                           settings.SCREEN_HEIGHT * 0.12,
                                           settings.SCREEN_WIDTH * 0.4,
                                           settings.SCREEN_HEIGHT * 0.76),
                                           manager=self.ui_manager,
                                           object_id="#settings_bg")
        self.right_ui = UIPanel(pygame.Rect(settings.SCREEN_WIDTH * 0.8,
                                                settings.SCREEN_HEIGHT * 0.6,
                                                settings.SCREEN_WIDTH * 0.15,
                                                settings.SCREEN_HEIGHT * 0.28),
                                                manager=self.ui_manager,
                                                object_id="#settings_bg")
        self.debug_ui = UIPanel(pygame.Rect(settings.SCREEN_WIDTH * 0.55,
                                                settings.SCREEN_HEIGHT * 0.12,
                                                settings.SCREEN_WIDTH * 0.4,
                                                settings.SCREEN_HEIGHT * 0.35),
                                                manager=self.ui_manager,
                                                object_id="#settings_bg",
                                                visible=True if settings.DEBUG_MODE else False)
        
        # Spawns my UI elements
        ## Left UI
        self.ltitle = UILabel(relative_rect=pygame.Rect(0, 25, -1, -1),
                                text="Settings",
                                manager=self.ui_manager,
                                object_id="#settings_titles",
                                container=self.left_ui,
                                anchors={"centerx": "centerx", "top": "top"})
        resolutions_raw = pygame.display.list_modes()
        resolutions = [f"{width}x{height}" for width, height in resolutions_raw]
        self.res_dropdown = UIDropDownMenu( resolutions,
                                            relative_rect=pygame.Rect((self.left_ui.rect.width * 0.85) - 150, self.left_ui.rect.height * 0.17, 150, 25),
                                            starting_option=f"{settings.SCREEN_WIDTH}x{settings.SCREEN_HEIGHT}",
                                            manager=self.ui_manager,
                                            container=self.left_ui,
                                            anchors={"right": "right",
                                                     "right_target": self.left_ui},
                                            object_id="#settings")
        self.res_text = UILabel(pygame.Rect((self.left_ui.rect.width * 0.1), 0, -1, -1),
                                "Resolution:",
                                self.ui_manager,
                                object_id="#settings",
                                container=self.left_ui,
                                anchors={"right": "left", "centery": "centery",
                                         "right_target": self.res_dropdown,
                                         "centery_target": self.res_dropdown})
        self.fullscreen_toggle = UIDropDownMenu(["Fullscreen", "Windowed"],
                                                "Fullscreen" if settings.FULLSCREEN else "Windowed",
                                                pygame.Rect(0, 15, 150, 25),
                                                self.ui_manager,
                                                container=self.left_ui,
                                                anchors={"right": "right",
                                                         "top": "top",
                                                         "right_target": self.res_dropdown,
                                                         "top_target": self.res_dropdown},
                                                object_id="#settings")
        self.fullscreen_text = UILabel(pygame.Rect((self.left_ui.rect.width * 0.1), 0, -1, -1),
                                "Display Mode:",
                                self.ui_manager,
                                object_id="#settings",
                                container=self.left_ui,
                                anchors={"right": "left", "centery": "centery",
                                         "right_target": self.res_dropdown,
                                         "centery_target": self.fullscreen_toggle})
        
        ## Right UI
        self.back_button = UIButton(pygame.Rect(0, self.right_ui.rect.height * -0.3, 150, 50),
                                    text="Back",
                                    manager=self.ui_manager,
                                    container=self.right_ui,
                                    anchors={"centerx": "centerx",
                                             "bottom": "bottom",
                                             "centerx_target": self.right_ui},
                                    object_id="#settings")
        self.defaults_button = UIButton(pygame.Rect(0, -50, 150, 50),
                                    text="Defaults",
                                    manager=self.ui_manager,
                                    container=self.right_ui,
                                    anchors={"centerx": "centerx",
                                             "bottom": "bottom",
                                             "centerx_target": self.right_ui,
                                             "bottom_target": self.back_button},
                                    object_id="#settings")
        self.apply_button = UIButton(pygame.Rect(0, -50, 150, 50),
                                    text="Apply",
                                    manager=self.ui_manager,
                                    container=self.right_ui,
                                    anchors={"centerx": "centerx",
                                             "bottom": "bottom",
                                             "centerx_target": self.right_ui,
                                             "bottom_target": self.defaults_button},
                                    object_id="#settings",
                                    visible=True if settings.DEBUG_MODE else False)
        
        ## Debug UI
        self.dtitle = UILabel(relative_rect=pygame.Rect(0, 25, -1, -1),
                                text="Debug Cheats, ya Cheater",
                                manager=self.ui_manager,
                                object_id="#settings_titles",
                                container=self.debug_ui,
                                anchors={"centerx": "centerx", "top": "top"})
        self.hitbox_toggle = UIDropDownMenu(["Show Hitboxes", "True", "False"],
                                            "True" if settings.DEBUG_SHOW_PLAYER_HITBOX else "False",
                                            pygame.Rect((self.debug_ui.rect.width // 2) - (self.debug_ui.rect.width // 4), 65, 150, 25),
                                            self.ui_manager,
                                            container=self.debug_ui,
                                            anchors={"centerx": "centerx",
                                                     "top": "top",
                                                     "centerx_target": self.debug_ui},
                                            object_id="#settings")

        
        # Grouping the elements into a list for easy recall
        self.bg_ui_parent = [self.left_ui, self.right_ui, self.debug_ui, self.ltitle]
        self.left_ui_elements = [self.res_dropdown, self.fullscreen_toggle, self.fullscreen_text, self.res_text]
        self.right_ui_elements = [self.back_button, self.defaults_button, self.apply_button]
        self.debug_ui_elements = [self.dtitle, self.hitbox_toggle]
        

    def run(self, screen, dt):
        

        
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.new_state = "main_menu"
                self.transition = True
            elif keys[pygame.K_RETURN]:
                self.apply()
            if keys[pygame.K_F12]:
                self.new_settings_dict["debug_mode"] = False if self.new_settings_dict["debug_mode"] else True

            # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True

            self.ui_manager.process_events(event)

            # If the player changes the resolution or fullscreen settings, set temp values
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.res_dropdown:
                    self.new_screen_width = int(event.text.split("x")[0])
                    self.new_screen_height = int(event.text.split("x")[1])
                    self.new_settings_dict["resolution"] = event.text
                    print(self.new_settings_dict)
                elif event.ui_element == self.fullscreen_toggle:
                    self.new_settings_dict["fullscreen"] = event.text
                elif event.ui_element == self.hitbox_toggle:
                    self.new_settings_dict["hitboxes"] = "True" if event.text == "True" else "False"

            # Track player input for the buttons
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.apply_button:
                    self.apply()
                elif event.ui_element == self.back_button:
                    self.new_state = "main_menu"
                    self.transition = True
                elif event.ui_element == self.defaults_button:
                    self.defaults()

        # Checks if the player has changed any settings, and shows the apply button if they have
        if self.new_settings_dict != self.settings_dict:
            self.apply_button.show()
        else:
            self.apply_button.hide()
        

        self.ui_manager.update(dt)

        screen.fill(("black"))

        self.ui_manager.draw_ui(screen)

        pygame.display.update()
