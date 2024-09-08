import pygame
import random
from game.data import settings

from game.entities.enemy_white_fighter import WhiteEnemyFighter
from game.entities.enemy_black_fighter import BlackEnemyFighter
from game.entities.enemy_yellow_fighter import YellowEnemyFighter

class EnemyFactory():
    def __init__(self, screen_bounds, game_state):
        self.game_state = game_state
        self.enemy_types = ["WhiteEnemyFighter", "BlackEnemyFighter", "YellowEnemyFighter"]
        self.spawn_area = pygame.Rect(0, settings.SCREEN_HEIGHT * -0.1, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT * 0.1)
        self.screen_bounds = screen_bounds
        self.spawn_timer = 0

    def spawn_point(self):
        return (random.randint(self.spawn_area.left, self.spawn_area.right), self.spawn_area.top)

    def select_enemy(self):
        _number = random.randint(0, 100)
        if _number < 60:
            return "WhiteEnemyFighter"
        elif _number < 80:
            return "BlackEnemyFighter"
        else:
            return "YellowEnemyFighter"

    def spawn_enemy(self):
        _choice = self.select_enemy()
        if _choice == "WhiteEnemyFighter":
            enemy = WhiteEnemyFighter(*self.spawn_point(), 100, 100, 200, 2, 100)
            self.game_state.drawable.add(enemy)
            self.game_state.updatable.add(enemy)
            self.game_state.enemies.add(enemy)
            return enemy
        elif _choice == "BlackEnemyFighter":
            enemy = BlackEnemyFighter(*self.spawn_point(), 200, 150, 500, 3, 250)
            self.game_state.drawable.add(enemy)
            self.game_state.updatable.add(enemy)
            self.game_state.enemies.add(enemy)
            return enemy
        elif _choice == "YellowEnemyFighter":
            enemy = YellowEnemyFighter(*self.spawn_point(), 300, 175, 600, 4, 500)
            self.game_state.drawable.add(enemy)
            self.game_state.updatable.add(enemy)
            self.game_state.enemies.add(enemy)
            return enemy

    def update(self, dt, game_time):
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = 3
            enemy = self.spawn_enemy()
            return enemy
        return None   