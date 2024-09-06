import pygame
import pygame_gui
import random

from game.data.settings import DEBUG_SHOW_PLAYER_HITBOX, SCREEN_WIDTH, SCREEN_HEIGHT

from game.entities.base_entity import BaseEntity
from game.entities.bullet import Bullet
from game.entities.enemy_white_fighter import WhiteEnemyFighter

class Player(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, health_capacity=100)
        self.position = pygame.Vector2(x, y)
        self.bullets = pygame.sprite.Group()
        self.image, self.rect = self.get_sprite(pygame.image.load("ui/game_assets/FighterPlaneV2.png").convert_alpha())

        self.lives = 3
        self.score = 0
        self._player_speed = 300
        self.current_health = self.health_capacity

        self.shot_timer = 0
        self.bullet_speed = -700

    def get_sprite(self, image):
        ship_selection = pygame.Rect(1064, 1800, 1000, 900)
        ship_sprite = image.subsurface(ship_selection)
        ship_sprite = pygame.transform.scale(ship_sprite, (100, 100))
        ship_rect = ship_sprite.get_rect(center=self.position)
        return ship_sprite, ship_rect 
       
    def draw(self, screen):        
        screen.blit(self.image, self.rect)

    def move_vert(self, dt, direction):
        self.position.y += direction * self._player_speed * dt
        self.rect.y = self.position.y

    def move_hor(self, dt, direction):
        self.position.x += direction * self._player_speed * dt
        self.rect.x = self.position.x

    def shoot(self):
        if self.shot_timer <= 0:
            bullet = Bullet(self.position.x, self.position.y, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            bullet.velocity = pygame.Vector2(0, self.bullet_speed)
            self.bullets.add(bullet)
            self.shot_timer = 0.3

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

    def update(self, dt, playable_area):
        self.shot_timer -= dt
        self.position.x = max(playable_area.left, min(self.position.x, playable_area.right))
        self.position.y = max(playable_area.top, min(self.position.y, playable_area.bottom))
        self.rect.center = self.position