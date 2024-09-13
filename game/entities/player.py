import pygame
import pygame_gui
import random

from pygame_gui.elements import UIImage
from game.data.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from game.entities.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, ui_manager, game_state):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.ui_manager = ui_manager
        self.game_state = game_state
        
        self.bullets = pygame.sprite.Group()
        self._allies = pygame.sprite.Group()
        self.image, self.rect = self.get_sprite(pygame.image.load("ui/game_assets/Ships maybe/destroyer.png").convert_alpha())
        self.rect.center = self.position
        self.heart_bool, self.speed_bool, self.weapon_bool = False, False, False
        self.screen_bounds = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.playable_area = pygame.Rect(50, 150, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200)

        self.lives = 3
        self.hearts = []
        self.score = 0
        self.player_speed = 400
        self.current_health = 100
        self.health_capacity = 100

        self.shot_timer = 0
        self.bullet_speed = -700
        
        self.boost_timer = 0
        self.boost = 0
        self.bombs = 1
        self.bomb_timer = 0
        self.bombs_ui = []
        self.has_powerup = False
        self.allies = []

    def get_sprite(self, image):
        ship_sprite = pygame.transform.scale(image, (100, 95))
        ship_sprite = pygame.transform.rotate(ship_sprite, 90)
        ship_rect = ship_sprite.get_rect(center=self.position)
        return ship_sprite, ship_rect 
       
    def draw(self, screen):   
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

    def move_vert(self, dt, direction):
        self.position.y += direction * self.player_speed * dt
        self.rect.y = self.position.y

    def move_hor(self, dt, direction):
        self.position.x += direction * self.player_speed * dt
        self.rect.x = self.position.x
                
    def shoot(self):
        if self.shot_timer <= 0:
            bullet = Bullet(self.position.x, self.position.y, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0, 50)
            bullet.velocity = pygame.Vector2(0, self.bullet_speed)
            self.bullets.add(bullet)
            self.shot_timer = 0.3
            for ally in self.allies:
                ally.shoot()
    
    def hit_by_bullet(self, damage):
        self.current_health -= damage
        self.check_alive(self.game_state)
    
    def hit_enemy_ship(self):
        self.current_health -= 50
        self.check_alive(self.game_state)

    def check_alive(self, game_state):
        if self.current_health <= 0:
            if  self.lives == 0:
                game_state.game_length = game_state.elapsed_time
                game_state.new_state = "game_over"
                game_state.transition = True
            else:
                self.lives -= 1
                self.current_health += self.health_capacity
                self.update_hearts(game_state)

    def update_hearts(self, game_state):
        self.heart_image = pygame.image.load("ui/game_assets/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))
        for heart_ui in self.hearts:
            heart_ui.kill()
        self.hearts.clear()
        for i in range(self.lives):
            heart_ui = UIImage(pygame.Rect(55 + i * 20, 2, 30, 30),
                               self.heart_image,
                               self.ui_manager,
                               parent_element=game_state.lives_display,
                               anchors={"centery": "centery", "left": "left", "centery_target": game_state.lives_display})   
            self.hearts.append(heart_ui)
        for i, heart_ui in enumerate(self.hearts):
            if i < self.lives:
                heart_ui.show()
            else:
                heart_ui.hide()

    def update_bombs(self, game_state):
        self.bomb_image = pygame.image.load("ui/game_assets/bomb64.png").convert_alpha()
        self.bomb_image = pygame.transform.scale(self.bomb_image, (22, 22))
        for bomb_ui in self.bombs_ui:
            bomb_ui.kill()
        self.bombs_ui.clear()
        for i in range(self.bombs):
            bomb_ui = UIImage(pygame.Rect(i * 25, -5, 30, 30),
                               self.bomb_image,
                               self.ui_manager,
                               parent_element=game_state.bomb_display,
                               anchors={"centery": "centery", "left": "left", "centery_target": game_state.bomb_display, "left_target": game_state.bomb_display})   
            self.bombs_ui.append(bomb_ui)
        for i, bomb_ui in enumerate(self.bombs_ui):
            if i < self.bombs:
                bomb_ui.show()
            else:
                bomb_ui.hide()

    def kill_boost(self):
        if self.speed_bool == True:
            print("Speed powerup removed")
            self.speed_bool = False
            self.player_speed -= self.boost
            self.boost = 0

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_vert(dt, -1)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_vert(dt, 1)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_hor(dt, -1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_hor(dt, 1)
        if keys[pygame.K_b] and self.bombs > 0:
            if self.bomb_timer <= 0:
                self.bomb_timer = 1
                self.bombs -= 1
                self.game_state.detonate_bomb()
        if keys[pygame.K_SPACE] and self.shot_timer <= 0:
            for ally in self._allies:
                ally.shoot()
            self.shoot()

    def update(self, dt, screen_bounds):
        self.shot_timer -= dt
        self.boost_timer -= dt
        self.bomb_timer -= dt

        if self.boost_timer <= 0:
            self.kill_boost()
            self.boost_timer = 0
        
        self._allies.update(dt, self)
        self.handle_input(dt)
        self.bullets.update(dt, self.screen_bounds)
        self.position.x = max(self.playable_area.left, min(self.position.x, self.playable_area.right))
        self.position.y = max(self.playable_area.top, min(self.position.y, self.playable_area.bottom))
        self.rect.center = self.position


class Wingman(pygame.sprite.Sprite):
    def __init__(self, x, y, player, game_state, offset):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.player = player
        self.game_state = game_state
        self.image = pygame.image.load("ui/game_assets/Ships maybe/destroyer.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=self.position)
        self.rotation = -90
        self.bullet_speed = -700
        self.health = 50
        self.x_offset = offset

    def shoot(self):
        bullet = Bullet(self.position.x, self.position.y, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0, 50)
        bullet.velocity = pygame.Vector2(0, self.bullet_speed)
        self.player.bullets.add(bullet)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt, player):
        self.position.x = player.position.x + self.x_offset
        self.position.y = player.position.y + 60
        self.rect.center = self.position