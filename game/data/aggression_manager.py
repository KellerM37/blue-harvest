import pygame

class AggressionManager():
    def __init__(self, game_time, ui_manager, state_manager, enemy_factory, powerup_factory):
        self.game_time = game_time
        self.ui_manager = ui_manager
        self.state_manager = state_manager
        self.enemy_factory = enemy_factory
        self.powerup_factory = powerup_factory

        self.aggression = 0
        self.last_checked_time = 0


    def update(self, dt, elapsed):
        self.aggression += dt / 1000
        self.game_time = elapsed
        self.check_timers()

    def increase_aggression(self):
        self.enemy_factory.speed_boost += 20
        self.enemy_factory.spawn_rate -= 0.25 if self.enemy_factory.spawn_rate > 0.5 else 0
        self.enemy_factory.rarity["WhiteEnemyFighter"] -= 3
        self.enemy_factory.rarity["BlackEnemyFighter"] += 1
        self.enemy_factory.rarity["YellowEnemyFighter"] += 2

    def check_timers(self):
        current_time = int(self.game_time)
        if current_time % 600 == 0 and current_time != self.last_checked_time:
            self.state_manager.states["game_state"].new_state = "game_over"
            self.state_manager.states["game_state"].transition = True
        if current_time % 60 == 0 and current_time != self.last_checked_time:
            self.last_checked_time = current_time
            self.enemy_factory.spawn_boss()
        if current_time % 40 == 0 and current_time != self.last_checked_time:
            self.last_checked_time = current_time
            self.enemy_factory.wave += 1
            self.enemy_factory.spawn_wave()
        if current_time % 15 == 0 and current_time != self.last_checked_time:
            self.last_checked_time = current_time
            self.increase_aggression()

    def reset_aggression(self):
        pass