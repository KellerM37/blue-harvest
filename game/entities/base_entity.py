import pygame


# Reusing the circular collision detection from a previous project
# This will be used until I have player and enemy classes

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, health_capacity):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.health_capacity = health_capacity

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt):
        pass
    
    # Check if two entities are colliding
    def collision(self, other):
        return pygame.math.Vector2.distance_to(self.position, other.position) <= self.radius + other.radius