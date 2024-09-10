import pygame

from .base_powerup import BasePowerup

class SpeedPowerup(BasePowerup):
    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, pygame.image.load("ui/game_assets/speedup.png").convert_alpha(), "speed_powerup")
        self.screen_bounds = screen_bounds
        self.position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 130

    def update(self, dt, screen_bounds):
        self.position.y += self.speed * dt
        self.rect.y = self.position.y

    def apply(self, player):
        boost = 150
        player._player_speed += boost
        player.has_powerup = True
        player.powerup_timer = 5
        return boost
