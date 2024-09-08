import pygame
import pygame_gui
import random

from pygame_gui.elements import UIImage

from game.data.settings import DEBUG_SHOW_PLAYER_HITBOX, SCREEN_WIDTH, SCREEN_HEIGHT

from game.entities.base_entity import BaseEntity
from game.entities.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, ui_manager):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.ui_manager = ui_manager
        
        self.bullets = pygame.sprite.Group()
        self.image, self.rect = self.get_sprite(pygame.image.load("ui/game_assets/FighterPlaneV2.png").convert_alpha())
        self.rect.center = self.position
        self.heart_bool, self.speed_bool, self.weapon_bool = False, False, False
        self.screen_bounds = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.playable_area = pygame.Rect(50, 150, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200)

        self.lives = 3
        self.hearts = []
        self.score = 0
        self._player_speed = 300
        self.current_health = 100
        self.health_capacity = 100

        self.shot_timer = 0
        self.bullet_speed = -700
        
        self.powerup_timer = 0
        self.boost = 0
        self.has_powerup = False

    def get_sprite(self, image):
        ship_selection = pygame.Rect(1064, 1800, 1000, 900)
        ship_sprite = image.subsurface(ship_selection)
        ship_sprite = pygame.transform.scale(ship_sprite, (100, 100))
        ship_rect = ship_sprite.get_rect(center=self.position)
        return ship_sprite, ship_rect 
       
    def draw(self, screen):        
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

    def move_vert(self, dt, direction):
        self.position.y += direction * self._player_speed * dt
        self.rect.y = self.position.y

    def move_hor(self, dt, direction):
        self.position.x += direction * self._player_speed * dt
        self.rect.x = self.position.x

    def check_collision(self, enemies, powerups, enemy_bullets, game_state):
        for x in powerups:
            if self.rect.colliderect(x.rect):
                self.handle_powerup(x, game_state)
        for x in enemy_bullets:
            if self.rect.colliderect(x.rect):
                x.kill()
                self.current_health -= 10
                self.player_hit(game_state)
        for x in enemies:
            if self.rect.colliderect(x.rect):
                x.kill()
                self.current_health -= 50
                self.player_hit(game_state)

    def shoot(self):
        if self.shot_timer <= 0:
            bullet = Bullet(self.position.x, self.position.y, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            bullet.velocity = pygame.Vector2(0, self.bullet_speed)
            self.bullets.add(bullet)
            self.shot_timer = 0.3
            
    def player_hit(self, game_state):
        if self.current_health <= 0:
            if  self.lives == 0:
                game_state.game_length = game_state.time_elapsed
                game_state.new_state = "game_over"
                game_state.transition = True
            else:
                self.lives -= 1
                self.current_health = 100
                self.update_hearts(game_state) 

    def update_hearts(self, game_state):
        self.heart_image = pygame.image.load("ui/game_assets/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))
        for heart_ui in self.hearts:
            heart_ui.kill()
        self.hearts.clear()
        for i in range(self.lives):
            heart_ui = UIImage(pygame.Rect(55 + i * 20, 2, 30, 30),
                               self.heart_image,
                               self.ui_manager,
                               parent_element=game_state.lives_display,
                               anchors={"centery": "centery", "left": "left", "centery_target": game_state.lives_display})   
            self.hearts.append(heart_ui)
        for i, heart_ui in enumerate(self.hearts):
            if i < self.lives:
                heart_ui.show()
            else:
                heart_ui.hide()

    def handle_powerup(self, powerup, game_state):
        if powerup.name == "speed_powerup":
            self.speed_bool = True
            self.boost = powerup.apply(self)
            powerup.kill()
        elif powerup.name == "heart_powerup":
            powerup.apply(self)
            self.update_hearts(game_state)
            powerup.kill()

    def kill_boost(self):
        if self.speed_bool == True:
            self.speed_bool = False
            self._player_speed -= self.boost
            self.boost = 0

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_vert(dt, -1)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_vert(dt, 1)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_hor(dt, -1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_hor(dt, 1)
        if keys[pygame.K_SPACE] and self.shot_timer <= 0:
            self.shoot()

    def update(self, dt, screen_bounds):
        self.shot_timer -= dt
        self.powerup_timer -= dt

        if self.powerup_timer <= 0:
            self.kill_boost()
            self.powerup_timer = 0

        self.handle_input(dt)
        self.bullets.update(dt, self.screen_bounds)
        self.position.x = max(self.playable_area.left, min(self.position.x, self.playable_area.right))
        self.position.y = max(self.playable_area.top, min(self.position.y, self.playable_area.bottom))
        self.rect.center = self.position