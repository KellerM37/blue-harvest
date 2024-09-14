import pygame
import random

from pygame_gui.elements.ui_screen_space_health_bar import UIScreenSpaceHealthBar
from game.data.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from game.entities.bullet import BossBullet
from game.entities.base_enemy import BaseEnemy


class BaseBoss(BaseEnemy):
    def __init__(self, x, y, health_capacity, speed, bullet_speed, shot_delay, point_value, screen):
        super().__init__(x, y, health_capacity, speed, bullet_speed, shot_delay, point_value)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 100)
        self.bullets = pygame.sprite.Group()
        self.speed = speed
        self.shot_timer = 0
        self.shot_delay = shot_delay
        self.bullet_speed = bullet_speed
        self.health_capacity = health_capacity
        self.current_health = self.health_capacity
        self.point_value = point_value
        self.screen = screen
        self.draw_health_bar()

    def get_sprite(self, image):
        self.image = image
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = image.get_rect(center=self.position)
        return self.image, self.rect

    def draw_health_bar(self):
        self.health_bar = UIScreenSpaceHealthBar(pygame.Rect(0, SCREEN_HEIGHT - 30, SCREEN_WIDTH, 30),
                                                 self.screen,
                                                 self,
                                                 anchors={"top": "top", "centery": "centery"},
                                                 visible=True)

    def draw(self, screen):
        self.screen = screen
        self.rect.center = self.position
        screen.blit(self.image, self.rect)

    def update(self, dt, screen_bounds):
        self.bullets.update(dt, screen_bounds)
        self.shot_timer -= dt
        if self.shot_timer <= 0:
            self.shoot()


class Boss1(BaseBoss):
    def __init__(self,x, y, health_capacity=1000, speed=70, bullet_speed=200, shot_delay=1, point_value=1000, screen=None):
        super().__init__(x, y, health_capacity, speed, bullet_speed, shot_delay, point_value, screen)
        self.image, self.rect = self.get_sprite(pygame.image.load("ui/game_assets/Ships maybe/carrier.png").convert_alpha())
        self.rect.center = self.position

    def check_pos(self, dt):
        if self.position.y < SCREEN_HEIGHT * 0.3:
            self.move_vertically(dt)
        else:
            self.move_horizontally(dt)

    def move_vertically(self, dt):
        self.position.y += self.speed * dt
        self.rect.center = self.position
    
    def move_horizontally(self, dt):
        self.position.x += self.speed * dt
        self.rect.center = self.position
        if self.position.x > SCREEN_WIDTH * 0.9 or self.position.x < SCREEN_WIDTH * 0.18:
            self.speed = -self.speed

    def shoot(self):
        bullet = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(0, 1))
        bullet2 = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(-0.5, 1))
        bullet3 = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(-0.5, 0.5))
        bullet4 = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(-1, 1))
        bullet5 = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(-1, 0))
        bullet6 = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(0.5, 0.5))
        bullet7 = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(0.5, 1))
        bullet8 = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(1, 0))
        bullet9 = BossBullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), damage=25, rotation=180, speed=300, direction=(1, 1))
        self.bullets.add(bullet, bullet2, bullet3, bullet4, bullet5, bullet6, bullet7, bullet8, bullet9)
        self.shot_timer = self.shot_delay

    def update(self, dt, screen_bounds):
        self.shot_timer -= dt

        self.check_pos(dt)

        if self.shot_timer <= 0:
            self.shoot()