import pygame
import pygame_gui
from .base_state import BaseGamestate
from data import settings
from game.entities.player import Player

class GameState(BaseGamestate):
    def __init__(self, ui_manager, state_manager):
        super().__init__("game_state", state_manager)
        
        self.ui_manager = ui_manager
        self.state_manager = state_manager
    
    def start(self):
        player_start = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 0.9)

        self.player = Player(player_start[0], player_start[1])

        # Groups for various sprites to be updated and drawn
        self.updateable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player.add(self.updateable, self.drawable)
        print(f"Player created! {self.player}")
    
    def end(self):
        pass

    def run(self, screen, dt):

        # Event loops
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True

            # Temporary escape key to return to main menu. Will be replaced with a pause menu
            if keys[pygame.K_ESCAPE]:
                self.new_state = "main_menu"
                self.transition = True
            

            self.ui_manager.process_events(event)

        # Update all sprites
        for x in self.updateable:
            x.update(dt)

        # Clear and fill the screen
        screen.fill(("black"))

        # Draw all sprites
        for x in self.drawable:
            x.draw(screen)

        