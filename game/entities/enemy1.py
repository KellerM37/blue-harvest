import pygame
from data.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from .base_entity import BaseEntity
from .bullet import Bullet

class TestEnemy(BaseEntity):
    _enemy_image = None
    _enemy_rect = None

    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, radius=25, health=100)
        self.tmp_red = (255, 0, 0)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 100)
        self.bullets = pygame.sprite.Group()
        self._enemy_speed = 100
        self.screen_bounds = screen_bounds
        self.shot_timer = 0
        self.bullet_speed = 300
        if TestEnemy._enemy_image is None or TestEnemy._enemy_rect is None:
            TestEnemy._enemy_image, TestEnemy._enemy_rect = self.get_sprite(pygame.image.load("ui/game_assets/FighterPlaneV2.png").convert_alpha())

        self.image = TestEnemy._enemy_image
        self.rect = TestEnemy._enemy_rect.copy()
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.health = 100

    def update(self, dt):
        self.shot_timer -= dt
        self.position.y += self._enemy_speed * dt
        self.rect.y = self.position.y
        if self.shot_timer <= 0:
            self.shoot()
        if self.position.y > self.screen_bounds.height:
            self.kill()
            print("Debug: Enemy out of bounds, deleting")

    def shoot(self):
        bullet = Bullet(self.position.x, self.position.y + 50, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), rotation=180)
        bullet.velocity = pygame.Vector2(0, self.bullet_speed)
        self.bullets.add(bullet)
        self.shot_timer = 1
        print("Debug: Enemy shot")

    def get_sprite(self, image):
        ship_selection = pygame.Rect(1064, 0, 1000, 900)
        yellow_ship = image.subsurface(ship_selection)
        yellow_ship = pygame.transform.scale(yellow_ship, (100, 100))
        yellow_ship = pygame.transform.flip(yellow_ship, False, True)
        ship_rect = yellow_ship.get_rect(center=self.position)
        return yellow_ship, ship_rect 
