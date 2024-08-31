import pygame
import pygame_gui
import random

from data.settings import DEBUG_SHOW_PLAYER_HITBOX, SCREEN_WIDTH, SCREEN_HEIGHT

from game.entities.base_entity import BaseEntity
from game.entities.bullet import Bullet
from game.entities.enemy1 import TestEnemy

class Player(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, radius=44)
        self.tmp_green = (52, 190, 37)
        self.screen_bounds = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.timer = 0
        self.rotation = 180
        self.position = pygame.Vector2(x, y)
        self._player_speed = 300

        self.bullets = pygame.sprite.Group()
        self.bullet_speed = 500

        self.test_enemies = pygame.sprite.Group()
        self.enemy_timer = 0

        self.ship = pygame.image.load("ui/game_assets/FighterPlaneV2.png").convert_alpha()


    def get_sprite(self, image):
        self.ship_selection = (1064, 1800, 1000, 900)
        _yellow_ship = image.subsurface(1064, 1800, 1000, 900)
        _yellow_ship = pygame.transform.scale(_yellow_ship, (100, 100))
        _ship_rect = _yellow_ship.get_rect(center=self.position)

        return _yellow_ship, _ship_rect
    
    def draw(self, screen):
        if DEBUG_SHOW_PLAYER_HITBOX:
            super().draw(screen)

        screen.blit(self.get_sprite(self.ship)[0], self.get_sprite(self.ship)[1])

    def move_vert(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self._player_speed * dt

    def move_hor(self, dt):
        left = pygame.Vector2(1, 0).rotate(self.rotation)
        self.position += left * self._player_speed * dt

    def shoot(self):
        if self.timer <= 0:
            bullet = Bullet(self.position.x, self.position.y, self.screen_bounds)
            bullet.velocity = pygame.Vector2(0, -self.bullet_speed)
            self.bullets.add(bullet)
            self.timer = 0.3
            print("Debug: Bullet spawned")

    def debug_enemy_spawn(self):
        if self.enemy_timer <= 0:
            enemy = TestEnemy(random.uniform(0, SCREEN_WIDTH), 0, self.screen_bounds)
            self.test_enemies.add(enemy)
            self.enemy_timer = 0.65

    def update(self, dt, playable_area):
        self.timer -= dt
        self.enemy_timer -= dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.position.y > playable_area.top + self.radius:
                self.move_vert(dt)
        if keys[pygame.K_s]:
            if self.position.y < playable_area.bottom - self.radius:
                self.move_vert(-dt)
        if keys[pygame.K_a]:
            if self.position.x > playable_area.left + self.radius:
                self.move_hor(dt)
        if keys[pygame.K_d]:
            if self.position.x < playable_area.right - self.radius:
                self.move_hor(-dt)

        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

        if keys[pygame.K_F1] and self.enemy_timer <= 0:
            self.debug_enemy_spawn()