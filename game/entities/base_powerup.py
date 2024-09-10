import pygame

class BasePowerup(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name):
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.image = image
        self.name = name
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, screen_bounds):
        self.position.y += self.speed * dt
        self.rect.y = self.position.y
        if self.position.y > screen_bounds.height:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.position.y > self.screen_bounds.height:
            self.kill()

    def apply(self, player):
        pass