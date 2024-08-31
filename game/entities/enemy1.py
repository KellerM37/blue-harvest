import pygame
from .base_entity import BaseEntity

class TestEnemy(BaseEntity):
    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, radius=25)
        self.tmp_red = (255, 0, 0)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 100)
        self.enemy_speed = 100
        self.screen_bounds = screen_bounds
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)  # Bounding box for the circle

    def draw(self, screen):
        pygame.draw.circle(screen, self.tmp_red, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt, bullets):
        self.position += self.velocity * dt

        for bullet in bullets:
            if self.collides_with(bullet):
                bullet.kill()
                self.kill()
                print("Debug: Bullet hit enemy, deleting")

        if self.position.y > self.screen_bounds.height:
            self.kill()
            print("Debug: Enemy out of bounds, deleting")
    
    def collides_with(self, bullet):
        # Calculate if the enemy is hit by a bullet
        circle_radius = bullet.radius
        closest_x = max(bullet.rect.left, min(self.rect.centerx, bullet.rect.right))
        closest_y = max(bullet.rect.top, min(self.rect.centery, bullet.rect.bottom))
        distance_x = self.rect.centerx - closest_x
        distance_y = self.rect.centery - closest_y
        distance_squared = distance_x**2 + distance_y**2
        return distance_squared < circle_radius**2