from math import dist
import pygame

from .base_powerup import BasePowerup

class BombPowerup(BasePowerup):
    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, pygame.image.load("ui/game_assets/bomb64.png").convert_alpha(), "bomb_powerup")
        self.screen_bounds = screen_bounds
        self.position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 130

    def update(self, dt, screen_bounds):
        self.position.y += self.speed * dt
        self.rect.y = self.position.y
        if self.position.y > screen_bounds.height:
            self.kill()

    def apply(self, player):
        player.bombs += 1
        self.kill()

class BombExplosion(pygame.sprite.Sprite):
    def __init__(self, position, radius, enemies):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.radius = radius
        self.enemies = enemies
        self.expansion_rate = 750
        self.is_finished = False
    
    def update(self, dt, screen_bounds):
        self.radius += self.expansion_rate * dt
        if self.radius > 1800:
            self.is_finished = True
            self.kill()
        for enemy in self.enemies:
            if (self.position.distance_to(enemy.position) < self.radius):
                enemy.kill()
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), int(self.radius), 1)