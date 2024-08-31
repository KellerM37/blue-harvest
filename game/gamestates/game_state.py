import pygame
import pygame_gui

from game.entities import bullet
from .base_state import BaseGamestate
from data import settings
from game.entities.player import Player
from game.entities.bullet import Bullet

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
        self.bullets = pygame.sprite.Group()

        self.playable_area = pygame.Rect(50, 150, settings.SCREEN_WIDTH - 100, settings.SCREEN_HEIGHT - 150)
        
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
            if keys[pygame.K_F12]:
                settings.DEBUG_MODE = False

            self.ui_manager.process_events(event)

        # Update all sprites
        for x in self.updateable:
            x.update(dt, self.playable_area)
        for x in self.player.bullets:
            x.update(dt, self.player.test_enemies)
        for x in self.player.test_enemies:
            x.update(dt, self.player.bullets)

        # Clear and fill the screen
        screen.fill(("black"))

        if settings.DEBUG_SHOW_PLAYER_HITBOX:
            pygame.draw.rect(screen, ("White"), self.playable_area, width=2) # Debugging

        # Draw all sprites
        for x in self.drawable:
            x.draw(screen)
        for x in self.player.bullets:
            x.draw(screen)
        for x in self.player.test_enemies:
            x.draw(screen)
