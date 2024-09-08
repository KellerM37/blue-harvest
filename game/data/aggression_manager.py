import pygame

class AggressionManager():
    def __init__(self, game_time, ui_manager, state_manager, enemy_factory, powerup_factory):
        self.game_time = game_time
        self.ui_manager = ui_manager
        self.state_manager = state_manager
        self.enemy_factory = enemy_factory
        self.powerup_factory = powerup_factory

        self.aggression = 0


    def update(self, dt, elapsed):
        self.game_time = elapsed
        self.aggression += dt / 1000
        self.increase_aggression()

    def increase_aggression(self):
        self.enemy_factory.speed_boost += self.aggression

    def reset_aggression(self):
        pass