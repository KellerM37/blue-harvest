import pygame

from data import settings

from .base_entity import BaseEntity

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_area):
        super().__init__()
        self.surface = pygame.Surface((10, 10))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(center=(x, y))
        self.velocity = pygame.Vector2(0, -300)
        self.bullet_area = bullet_area
        self.radius = 5

    def update(self, dt, enemies):
        self.rect.y += self.velocity.y * dt

        for enemy in enemies:
            if self.collides_with(enemy):
                enemy.kill()
                self.kill()
                print("Debug: Bullet hit enemy, deleting")

        if not self.bullet_area.colliderect(self.rect):
            self.kill()
            print("Debug: Bullet out of bounds, deleting")

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def collides_with(self, enemy):
        # Calculate if the bullet collides with a given enemy
        circle_radius = enemy.radius
        closest_x = max(enemy.rect.left, min(self.rect.centerx, enemy.rect.right))
        closest_y = max(enemy.rect.top, min(self.rect.centery, enemy.rect.bottom))
        distance_x = self.rect.centerx - closest_x
        distance_y = self.rect.centery - closest_y
        distance_squared = distance_x**2 + distance_y**2
        return distance_squared < circle_radius**2


    