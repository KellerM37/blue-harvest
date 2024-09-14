import pygame
import random
from game.data import settings

from game.entities.enemy_fighters import WhiteEnemyFighter, BlackEnemyFighter, YellowEnemyFighter
from game.entities.bosses import Boss1

class EnemyFactory():
    def __init__(self, screen_bounds, game_state):
        self.game_state = game_state
        self.enemy_types = ["WhiteEnemyFighter", "BlackEnemyFighter", "YellowEnemyFighter"]
        self.spawn_area = pygame.Rect(0, settings.SCREEN_HEIGHT * -0.1, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT * 0.1)
        self.screen_bounds = screen_bounds
        self.spawn_timer = 3
        self.wave = 0

        self.speed_boost = 0
        self.spawn_rate = 3

        self.rarity = {
            "WhiteEnemyFighter": 75,
            "BlackEnemyFighter": 20,
            "YellowEnemyFighter": 5
        }

    def spawn_point(self):
        return (random.randint(self.spawn_area.left, self.spawn_area.right), self.spawn_area.top)
    
    def add_group(self, enemy):
        self.game_state.drawable.add(enemy)
        self.game_state.updatable.add(enemy)
        self.game_state.enemies.add(enemy)

    def select_enemy(self):
        _number = random.randint(0, 99)
        if _number < self.rarity["WhiteEnemyFighter"]:
            return "WhiteEnemyFighter"
        elif _number < self.rarity["WhiteEnemyFighter"] + self.rarity["BlackEnemyFighter"]:
            return "BlackEnemyFighter"
        else:
            return "YellowEnemyFighter"

    def spawn_enemy(self):
        _choice = self.select_enemy()
        if _choice == "WhiteEnemyFighter":
            enemy = WhiteEnemyFighter(*self.spawn_point())
            self.add_group(enemy)
            return enemy
        elif _choice == "BlackEnemyFighter":
            enemy = BlackEnemyFighter(*self.spawn_point())
            self.add_group(enemy)
            return enemy
        elif _choice == "YellowEnemyFighter":
            enemy = YellowEnemyFighter(*self.spawn_point())
            self.add_group(enemy)
            return enemy
        
    def spawn_wave(self):
        for _ in range(15):
            enemy = self.spawn_enemy()
        return enemy
    
    def spawn_boss(self):
        _spawn = Boss1(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * -0.1)
        self.add_group(_spawn)
        return _spawn

    def update(self, dt, game_time):
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = self.spawn_rate
            enemy = self.spawn_enemy()
            return enemy
        return None  

