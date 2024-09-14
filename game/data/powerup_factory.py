import pygame
import random
from game.data.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from game.entities.powerups import BombPowerup, HeartPowerup, SpeedPowerup, WingmanPowerup

class PowerupFactory():
    def __init__(self, screen_bounds, game_state, player, powerups):
        self.game_state = game_state
        self.player = player
        self.existing_powerups = powerups
        self.spawn_area = pygame.Rect(0, SCREEN_HEIGHT * -0.1, SCREEN_WIDTH, SCREEN_HEIGHT * 0.1)
        self.screen_bounds = screen_bounds

        self.spawn_timer = 0
        self.heart_timer = 30
        self.speed_timer = 50
        self.ally_timer = 10
        self.bomb_timer = 60

    def spawn_point(self):
        return (random.randint(self.spawn_area.left, self.spawn_area.right), self.spawn_area.top)

    def add_group(self, powerup):
        self.game_state.drawable.add(powerup)
        self.game_state.updatable.add(powerup)
        self.game_state.powerups.add(powerup)

    def check_spawn(self):
        if self.ally_timer <= 0 and len(self.player._allies) < 2:
            self.ally_timer = 45
            _spawn = WingmanPowerup(*self.spawn_point(), self.screen_bounds)
            self.add_group(_spawn)
            return _spawn
        if self.heart_timer <= 0 and len(self.player.hearts) < 3:
            self.heart_timer = 45
            _spawn = HeartPowerup(*self.spawn_point(), self.screen_bounds)
            self.spawnable_heart = False
            self.add_group(_spawn)
            return _spawn
        elif self.bomb_timer <= 0 and self.player.bombs < 3:
            self.bomb_timer = 90
            _spawn = BombPowerup(*self.spawn_point(), self.screen_bounds)
            self.spawnable_bomb = False
            self.add_group(_spawn)
            return _spawn
        elif self.speed_timer <= 0:
            self.speed_timer = 100
            _spawn = SpeedPowerup(*self.spawn_point(), self.screen_bounds)
            self.add_group(_spawn)
            return _spawn  

    def update(self, dt):
        self.spawn_timer -= dt
        self.heart_timer -= dt
        self.speed_timer -= dt
        self.ally_timer -= dt
        self.bomb_timer -= dt
        self.check_spawn()