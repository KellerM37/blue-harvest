import pygame
from pygame_gui.elements import *

from game.data.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from .bullet import Bullet

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health_capacity, speed, bullet_speed, shot_delay, point_value):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.tmp_red = (255, 0, 0)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 100)
        self.bullets = pygame.sprite.Group()
        self.speed = speed
        self.shot_timer = 0
        self.shot_delay = shot_delay
        self.bullet_speed = bullet_speed
        self.health_capacity = health_capacity
        self.current_health = health_capacity
        self.point_value = point_value

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.screen is None:
            self.screen = screen

    def update(self, dt, screen_bounds):
        self.shot_timer -= dt
        self.position.y += self.speed * dt
        self.rect.y = self.position.y
        self.bullets.update(dt, screen_bounds)
        if self.current_health < self.health_capacity:
            self.health_bar.show()
            self.health_bar.set_relative_position((self.rect.centerx - 50, self.rect.centery - 50))
        if self.shot_timer <= 0:
            self.shoot()
            pass
        if self.position.y > screen_bounds.height:
            self.kill()

    def shoot(self):
        bullet = Bullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), rotation=180)
        bullet.velocity = pygame.Vector2(0, self.bullet_speed)
        self.bullets.add(bullet)
        self.shot_timer = self.shot_delay

    def draw_health_bar(self):
        self.health_bar = UIScreenSpaceHealthBar(pygame.Rect(0, 0, 100, 10),
                                                 self.screen,
                                                 self,
                                                 anchors={"top": "top", "centery": "centery", "centery_target": self.rect},
                                                 visible=False)

    def get_sprite(self, image):
        pass
