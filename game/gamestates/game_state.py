import pygame
import pygame_gui
import random

from game.entities import bullet
from .base_state import BaseGamestate
from data import settings
from saves import *
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
        self.kill_count = 0

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

    def update_hearts(self):
        for i, heart_ui in enumerate(self.hearts):
            if i < self.player.lives:
                heart_ui.show()
            else:
                heart_ui.hide()

    def update(self, dt):
        self.spawn_timer -= dt
        self.player.handle_input(dt)
        self.updateable.update(dt, self.playable_area)
        self.player.bullets.update(dt)
        self.enemies.update(dt)
        self.ui_manager.update(dt)
        self.update_hearts()
        self.check_collisions()

        for enemy in self.enemies:
            enemy.bullets.update(dt)
        if self.spawn_timer <= 0:
            self.spawn_enemy()
        if self.player.current_health <= 0:
            if self.player.lives == 0:
                self.new_state = "game_over"
                self.transition = True
            else:
                self.player.lives -= 1
                self.player.current_health = 100
                self.lives_display.set_text(f"Lives: ")

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
                    self.kill_count += 1
                    self.player.score = self.kill_count * 100
                    self.kill_display.set_text(f"Kills: {self.kill_count}")
                    self.score_display.set_text(f"Score: {self.player.score}")
        for enemy in self.enemies:
            for bullet in enemy.bullets:
                if bullet.rect.colliderect(self.player.rect):
                    bullet.kill()
                    self.player.current_health -= 10
            if enemy.rect.colliderect(self.player.rect):
                enemy.kill()
                self.player.current_health -= 75

    def spawn_enemy(self):
        self.spawn_timer = random.uniform(0.5, 2)
        enemy = TestEnemy(random.uniform(0, settings.SCREEN_WIDTH), -125, pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.enemies.add(enemy)

    def build_ui(self):
        
        self.background_image = pygame.image.load("ui/game_assets/sci_fi_bg1.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, self.background_image.get_height()))
        self.background_speed = 0

        # Player HUD
        self.player_hud = UIPanel(pygame.Rect(0, 0, 400, 100),
                                  manager=self.ui_manager,
                                  object_id="#settings_bg",
                                  anchors={"left": "left",
                                           "top": "top"})
        self.player_health_bar = UIScreenSpaceHealthBar(pygame.Rect(0, 15, 370, 20),
                                                        manager=self.ui_manager,
                                                        sprite_to_monitor=self.player,
                                                        parent_element=self.player_hud,
                                                        anchors={"centerx": "centerx", "top": "top", "centerx_target": self.player_hud}
                                                        )
        self.kill_display = UILabel(pygame.Rect(15, 40, -1, -1),
                                    f"Kills: {self.kill_count}",
                                    manager=self.ui_manager,
                                    container=self.player_hud,
                                    anchors={"top": "top", "left": "left"})
        self.lives_display = UILabel(pygame.Rect(15, 60, -1, -1),
                                    f"Lives: ",
                                    manager=self.ui_manager,
                                    container=self.player_hud,
                                    anchors={"top": "top", "left": "left"})
        self.score_display = UILabel(pygame.Rect(200, 40, -1, -1),
                                    f"Score: {self.player.score}",
                                    manager=self.ui_manager,
                                    container=self.player_hud,
                                    anchors={"top": "top", "left": "left"})
        self.hi_score_display = UILabel(pygame.Rect(200, 60, -1, -1),
                                    f"Hi-Score: {self.state_manager.states['main_menu'].hi_score}",
                                    manager=self.ui_manager,
                                    container=self.player_hud,
                                    anchors={"top": "top", "left": "left"})
        self.heart_image = pygame.image.load("ui/game_assets/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))
        self.hearts = []
        for i in range(self.player.lives):
            heart_ui = UIImage(pygame.Rect(55 + i * 20, 2, 30, 30),
                               self.heart_image,
                               self.ui_manager,
                               parent_element=self.lives_display,
                               anchors={"centery": "centery", "left": "left", "centery_target": self.lives_display})   
            self.hearts.append(heart_ui)
        
        self.hud_elements = [self.player_hud, self.player_health_bar, self.kill_display]
        
        # Pause Menu
        self.pause_panel = UIPanel(pygame.Rect(0, 0, 350, 200),
                                   manager=self.ui_manager,
                                   object_id="#settings_bg",
                                   anchors={"centerx": "centerx", "centery": "centery"},
                                   visible=False)
        self.pause_title = UILabel(pygame.Rect(0, 10, -1, -1),
                                      "Paused",
                                      manager=self.ui_manager,
                                      container=self.pause_panel,
                                      object_id="#settings_titles",
                                      anchors={"top": "top", "centerx": "centerx"})
        self.resume_button = UIButton(pygame.Rect(0, -125, 250, 50),
                                        "Resume",
                                        manager=self.ui_manager,
                                        container=self.pause_panel,
                                        object_id="#settings_buttons",
                                        anchors={"bottom": "bottom", "centerx": "centerx"})
        self.quit_button = UIButton(pygame.Rect(0, -75, 250, 50),
                                        "Quit",
                                        manager=self.ui_manager,
                                        container=self.pause_panel,
                                        object_id="#settings_buttons",
                                        anchors={"bottom": "bottom", "centerx": "centerx"})
        
    def reset(self):
        self.kill_count = 0
    
    def run(self, screen, dt):

        # Event loops
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            self.ui_manager.process_events(event)

            # If window closed, quit game
            if event.type == pygame.QUIT:
                self.time_to_quit = True

            # Temporary escape key to return to main menu. Will be replaced with a pause menu
            if keys[pygame.K_ESCAPE]:
                self.is_paused = True if not self.is_paused else False
                if self.is_paused:
                    self.pause_panel.show()
                    for x in self.hud_elements:
                        x.hide()
                else:
                    self.pause_panel.hide()
                    for x in self.hud_elements:
                        x.show()
            if keys[pygame.K_F12]:
                settings.DEBUG_MODE = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.resume_button:
                    self.is_paused = False
                    self.pause_panel.hide()
                    for x in self.hud_elements:
                        x.show()
                if event.ui_element == self.quit_button:
                    self.new_state = "main_menu"
                    self.transition = True

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
        
        else:
            overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            overlay.set_alpha(20)
            overlay.fill((50, 50, 50))
            screen.blit(overlay, (0, 0))
            self.ui_manager.update(dt)
            self.ui_manager.draw_ui(screen)
