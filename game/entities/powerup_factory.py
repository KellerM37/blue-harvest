import pygame
import random
from game.data.settings import SCREEN_HEIGHT, SCREEN_WIDTH

from game.entities.powerup_heart import HeartPowerup
from game.entities.powerup_speed import SpeedPowerup

class PowerupFactory():
    def __init__(self, screen_bounds, game_state, player, powerups):
        self.game_state = game_state
        self.player = player
        self.existing_powerups = powerups
        self.powerup_types = ["HeartPowerup", "ShieldPowerup", "SpeedPowerup"]
        self.spawn_area = pygame.Rect(0, SCREEN_HEIGHT * -0.1, SCREEN_WIDTH, SCREEN_HEIGHT * 0.1)
        self.screen_bounds = screen_bounds

        self.spawn_timer = 0
        self.spawnable_heart = False
        self.heart_timer = 2

        self.speed_timer = 2

    def spawn_point(self):
        return (random.randint(self.spawn_area.left, self.spawn_area.right), self.spawn_area.top)

    def add_group(self, powerup):
        self.game_state.drawable.add(powerup)
        self.game_state.updatable.add(powerup)
        self.game_state.powerups.add(powerup)

    def update(self, dt):
        self.spawn_timer -= dt
        self.heart_timer -= dt
        self.speed_timer -= dt

        heart_powerup_exists = any(x.name == "heart_powerup" for x in self.existing_powerups)
        if self.player.lives < 3 and not heart_powerup_exists:
            self.spawnable_heart = True
        else:
            self.spawnable_heart = False

        if self.heart_timer <= 0 and self.spawnable_heart:
            self.heart_timer = 120
            _spawn = HeartPowerup(*self.spawn_point(), self.screen_bounds)
            self.spawnable_heart = False
            self.add_group(_spawn)
            return _spawn
        elif self.speed_timer <= 0:
            self.speed_timer = 60
            _spawn = SpeedPowerup(*self.spawn_point(), self.screen_bounds)
            self.add_group(_spawn)
            return _spawn        
        return None