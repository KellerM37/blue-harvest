import pygame
from .base_enemy import BaseEnemy

class WhiteEnemyFighter(BaseEnemy):
    _enemy_image = None
    _enemy_rect = None

    def __init__(self, x, y, health_capacity, speed, bullet_speed, shot_delay, point_value):
        super().__init__(x, y, health_capacity, speed, bullet_speed, shot_delay, point_value)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 100)
        self.bullets = pygame.sprite.Group()

        self.shot_timer = 0
        if WhiteEnemyFighter._enemy_image is None or WhiteEnemyFighter._enemy_rect is None:
            WhiteEnemyFighter._enemy_image, WhiteEnemyFighter._enemy_rect = self.get_sprite(pygame.image.load("ui/game_assets/FighterPlaneV2.png").convert_alpha())

        self.image = WhiteEnemyFighter._enemy_image
        self.rect = WhiteEnemyFighter._enemy_rect.copy()
        self.rect.center = self.position
        self.screen = None
        self.draw_health_bar()
     
    def get_sprite(self, image):
        white_ship = pygame.Rect(1064, 0, 1000, 900)
        ship_image = image.subsurface(white_ship)
        ship_image = pygame.transform.scale(ship_image, (100, 100))
        ship_image = pygame.transform.flip(ship_image, False, True)
        ship_rect = ship_image.get_rect(center=self.position)
        return ship_image, ship_rect 
