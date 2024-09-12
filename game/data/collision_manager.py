import pygame

from game.data.settings import *

class CollisionManager():
    def __init__(self, game_state, player, enemies, powerups):
        self.game_state = game_state
        self.player = player
        self.enemies = enemies
        self.powerups = powerups

    def check_collisions(self):
        self.check_player_enemy_collisions()
        self.check_player_powerup_collisions()
        self.check_bullet_enemy_collisions()
        self.check_bullet_player_collisions()

    def check_player_enemy_collisions(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.hit_enemy_ship()
                enemy.kill()
    
    def check_player_powerup_collisions(self):
        for powerup in self.powerups:
            if self.player.rect.colliderect(powerup.rect):
                self.process_powerup(powerup)

    def check_bullet_enemy_collisions(self):
        for enemy in self.enemies:
            for bullet in self.player.bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.enemy_damaged(enemy, self.game_state, bullet.damage)
                    bullet.kill()

    def check_bullet_player_collisions(self):
        for enemy in self.enemies:
            for bullet in enemy.bullets:
                if self.player.rect.colliderect(bullet.rect):
                    self.player.hit_by_bullet(bullet.damage)
                    bullet.kill()
        for bullet in self.game_state.enemy_bullets:
            if self.player.rect.colliderect(bullet.rect):
                self.player.hit_by_bullet(bullet.damage)
                bullet.kill()

    def process_powerup(self, powerup):
        if powerup.name == "speed_powerup":
            self.player.speed_bool = True
            self.player.boost = powerup.boost
            powerup.apply(self.player)
        elif powerup.name == "heart_powerup":
            powerup.apply(self.player)
            self.player.update_hearts(self.game_state)
        elif powerup.name == "bomb_powerup":
            powerup.apply(self.player)
            self.player.update_bombs(self.game_state)
        powerup.kill()