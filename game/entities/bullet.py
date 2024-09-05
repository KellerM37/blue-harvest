import pygame

from data import settings

from .base_entity import BaseEntity

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_area, rotation=0):
        super().__init__()
        self.surface = pygame.Surface((10, 10))
        self.rotation = rotation
        self.surface.fill((255, 255, 255))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, -300).rotate(rotation)
        self.bullet_area = bullet_area
        self.radius = 5

        self.image, self.rect = self.get_sprite(pygame.image.load("ui/game_assets/missile00.png").convert_alpha())

    def update(self, dt):
        self.rect.y += self.velocity.y * dt
        if not self.bullet_area.colliderect(self.rect):
            self.kill()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def get_sprite(self, bullet_image):
        rotated_image = pygame.transform.rotate(bullet_image, self.rotation)
        bullet_rect = rotated_image.get_rect(center=self.position)
        return rotated_image, bullet_rect 
    