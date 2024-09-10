import pygame

from .base_powerup import BasePowerup

class HeartPowerup(BasePowerup):
    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, pygame.image.load("ui/game_assets/Health.png").convert_alpha(), "heart_powerup")
        self.screen_bounds = screen_bounds
        self.position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 130

    def update(self, dt, screen_bounds):
        self.position.y += self.speed * dt
        self.rect.y = self.position.y
        if self.position.y > screen_bounds.height:
            print("Powerup missed")
            self.kill()

    def apply(self, player):
        player.lives += 1
        self.kill()