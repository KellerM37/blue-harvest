import pygame
from pygame_gui.elements import *
from .base_enemy import BaseEnemy

class YellowEnemyFighter(BaseEnemy):
    _enemy_image = None
    _enemy_rect = None

    def __init__(self, x, y, health_capacity, speed, bullet_speed, shot_delay, point_value, screen_bounds):
        super().__init__(x, y, health_capacity, speed, bullet_speed, shot_delay, point_value, screen_bounds)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 100)
        self.bullets = pygame.sprite.Group()

        self.shot_timer = 0
        if YellowEnemyFighter._enemy_image is None or YellowEnemyFighter._enemy_rect is None:
            YellowEnemyFighter._enemy_image, YellowEnemyFighter._enemy_rect = self.get_sprite(pygame.image.load("ui/game_assets/FighterPlaneV2.png").convert_alpha())

        self.image = YellowEnemyFighter._enemy_image
        self.rect = YellowEnemyFighter._enemy_rect.copy()
        self.rect.center = self.position
        self.screen = None
        self.draw_health_bar()

    def get_sprite(self, image):
        yellow_ship = pygame.Rect(1064, 1800, 1000, 900)
        yellow_bird_thing = image.subsurface(yellow_ship)
        yellow_bird_thing = pygame.transform.scale(yellow_bird_thing, (100, 100))
        yellow_bird_thing = pygame.transform.flip(yellow_bird_thing, False, True)
        ship_rect = yellow_bird_thing.get_rect(center=self.position)
        return yellow_bird_thing, ship_rect 
