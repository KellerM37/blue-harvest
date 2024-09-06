import pygame


# Reusing the circular collision detection from a previous project
# This will be used until I have player and enemy classes

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, health_capacity):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.health_capacity = health_capacity
        self.current_health = health_capacity
    
    def get_sprite(self, image):
        pass

    def draw(self, screen):
        pass

    def update(self, dt):
        pass
