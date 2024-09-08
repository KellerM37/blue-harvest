import pygame
import random
from game.data.settings import SCREEN_HEIGHT, SCREEN_WIDTH

from game.entities.powerup_heart import HeartPowerup
from game.entities.powerup_speed import SpeedPowerup

class PowerupFactory():
    def __init__(self, screen_bounds, game_state, player):
        self.game_state = game_state
        self.player = player
        self.powerup_types = ["HeartPowerup", "ShieldPowerup", "SpeedPowerup"]
        self.spawn_area = pygame.Rect(0, SCREEN_HEIGHT * -0.1, SCREEN_WIDTH, SCREEN_HEIGHT * 0.1)
        self.screen_bounds = screen_bounds
        self.spawn_timer = 0

    def spawn_point(self):
        return (random.randint(self.spawn_area.left, self.spawn_area.right), self.spawn_area.top)

    def select_powerup(self):
        _number = random.randint(0, 100)
        if _number < 50:
            return "HeartPowerup"
        return "SpeedPowerup"

    def spawn_powerup(self):
        _choice = self.select_powerup()
        if _choice == "HeartPowerup":
            return HeartPowerup(*self.spawn_point(), self.screen_bounds)
        elif _choice == "SpeedPowerup":
            return SpeedPowerup(*self.spawn_point(), self.screen_bounds)

    def update(self, dt):
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = 10
            powerup = self.spawn_powerup()
            self.select_powerup()
            self.game_state.drawable.add(powerup)
            self.game_state.updatable.add(powerup)
            self.game_state.powerups.add(powerup)
            return powerup
        return None