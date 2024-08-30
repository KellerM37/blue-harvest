import pygame
import pygame_gui

from game.entities.base_entity import BaseEntity

class Player(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y, radius=20)
        self.tmp_green = (52, 190, 37)

        self.timer = 0
        self.rotation = 180
        self.position = pygame.Vector2(x, y)

        self._player_speed = 200

    # Draw the player as a triangle for now
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.tmp_green, self.triangle())

    def move_vert(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self._player_speed * dt

    def move_hor(self, dt):
        left = pygame.Vector2(1, 0).rotate(self.rotation)
        self.position += left * self._player_speed * dt

    def update(self, dt):
        self.timer -= dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move_vert(dt)
        if keys[pygame.K_s]:
            self.move_vert(-dt)
        if keys[pygame.K_a]:
            self.move_hor(dt)
        if keys[pygame.K_d]:
            self.move_hor(-dt)