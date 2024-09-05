import pygame
import pygame_gui
import random

from game.entities import bullet
from .base_state import BaseGamestate
from data import settings
from game.entities.player import Player
from game.entities.bullet import Bullet
from game.entities.enemy1 import TestEnemy
from pygame_gui.elements import *

class GameState(BaseGamestate):
    def __init__(self, ui_manager, state_manager):
        super().__init__("game_state", state_manager)
        
        self.ui_manager = ui_manager
        self.state_manager = state_manager
    
    def start(self):
        player_start = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 0.9)
        self.playable_area = pygame.Rect(50, 150, settings.SCREEN_WIDTH - 100, settings.SCREEN_HEIGHT - 200)
        self.player = Player(player_start[0], player_start[1])

        self.spawn_timer = 0

        # Groups for various sprites to be updated and drawn
        self.updateable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player.add(self.updateable, self.drawable)

        self.build_ui()
        self.is_paused = False
    
    def end(self):
        self.ui_manager.clear_and_reset()
        self.updateable.empty()
        self.drawable.empty()
        self.enemies.empty()
        self.player.bullets.empty()
        self.player.kill()

    def update(self, dt):
        self.spawn_timer -= dt
        self.player.handle_input(dt)
        self.updateable.update(dt, self.playable_area)
        self.player.bullets.update(dt)
        self.enemies.update(dt)
        self.ui_manager.update(dt)
        self.check_collisions()

        for enemy in self.enemies:
            enemy.bullets.update(dt)
        if self.spawn_timer <= 0:
            self.spawn_enemy()
        if self.player.current_health <= 0:
            self.new_state = "game_over"
            self.transition = True

    def draw(self, screen):
        self.drawable.draw(screen)
        self.player.bullets.draw(screen)
        self.enemies.draw(screen)
        for enemy in self.enemies:
            enemy.bullets.draw(screen)
        
        self.ui_manager.draw_ui(screen)

    def check_collisions(self):
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    enemy.kill()
        for enemy in self.enemies:
            for bullet in enemy.bullets:
                if bullet.rect.colliderect(self.player.rect):
                    bullet.kill()
                    self.player.current_health -= 10

    def spawn_enemy(self):
        self.spawn_timer = random.uniform(1, 2.5)
        enemy = TestEnemy(random.uniform(0, settings.SCREEN_WIDTH), -125, pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.enemies.add(enemy)

    def build_ui(self):
        
        self.background_image = pygame.image.load("ui/game_assets/sci_fi_bg1.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, self.background_image.get_height()))
        self.background_speed = 0

        self.player_hud = UIPanel(pygame.Rect(0, 0, 400, 100),
                                  manager=self.ui_manager,
                                  object_id="#settings_bg",
                                  anchors={"left": "left",
                                           "top": "top"})
        self.player_health_bar = UIScreenSpaceHealthBar(pygame.Rect(10, 10, 380, 20),
                                                        manager=self.ui_manager,
                                                        sprite_to_monitor=self.player,
                                                        parent_element=self.player_hud
                                                        )
    
    def pause(self):
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
                self.is_paused = True if not self.is_paused else False
            if keys[pygame.K_F12]:
                settings.DEBUG_MODE = False

            self.ui_manager.process_events(event)
        

        if not self.is_paused:
            # Background scrolling
            self.background_speed += 25 * dt
            if self.background_speed >= self.background_image.get_height():
                self.background_speed = 0
            screen.blit(self.background_image, (0, self.background_speed - self.background_image.get_height()))
            screen.blit(self.background_image, (0, self.background_speed))

            self.update(dt)

            if settings.DEBUG_SHOW_PLAYER_HITBOX:
                pygame.draw.rect(screen, ("White"), self.playable_area, width=2) # Debugging
            self.draw(screen)
