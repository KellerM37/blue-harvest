import pygame

from game.entities.player import Wingman

class BasePowerup(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name):
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.image = image
        self.original_image = image
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


class SpeedPowerup(BasePowerup):
    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, pygame.image.load("ui/game_assets/speedup.png").convert_alpha(), "speed_powerup")
        self.screen_bounds = screen_bounds
        self.position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 130
        self.boost = 200

    def update(self, dt, screen_bounds):
        self.position.y += self.speed * dt
        self.rect.y = self.position.y
        if self.position.y > screen_bounds.height:
            print("Powerup missed")
            self.kill()

    def apply(self, player):
        print("Speed powerup applied")
        player.player_speed += self.boost
        player.boost_timer = 30
        player.has_powerup = True


class HeartPowerup(BasePowerup):
    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, pygame.image.load("ui/game_assets/Health.png").convert_alpha(), "heart_powerup")
        self.screen_bounds = screen_bounds
        self.position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 130

    def update(self, dt, screen_bounds):
        self.position.y += self.speed * dt
        self.rect.y = self.position.y
        if self.position.y > screen_bounds.height:
            print("Powerup missed")
            self.kill()

    def apply(self, player):
        player.lives += 1
        self.kill()


class BombPowerup(BasePowerup):
    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, pygame.image.load("ui/game_assets/bomb64.png").convert_alpha(), "bomb_powerup")
        self.screen_bounds = screen_bounds
        self.position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 130

    def update(self, dt, screen_bounds):
        self.position.y += self.speed * dt
        self.rect.y = self.position.y
        if self.position.y > screen_bounds.height:
            self.kill()

    def apply(self, player):
        player.bombs += 1
        self.kill()


class BombExplosion(pygame.sprite.Sprite):
    def __init__(self, position, radius, enemies, player):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.player = player
        self.radius = radius
        self.enemies = enemies
        self.damage = 300
        self.expansion_rate = 1750
        self.is_finished = False
    
    def update(self, dt, screen_bounds):
        self.radius += self.expansion_rate * dt
        if self.radius > 1800:
            self.is_finished = True
            self.kill()
        for enemy in self.enemies:
            if (self.position.distance_to(enemy.position) < self.radius - 50) and enemy.bomb_immunity <= 0:
                enemy.enemy_damaged(enemy, self.player.game_state, self.damage)
                enemy.bomb_immunity = 1
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), int(self.radius), 1)


class WingmanPowerup(BasePowerup):
    def __init__(self, x, y, screen_bounds):
        super().__init__(x, y, pygame.image.load("ui/game_assets/Ships maybe/destroyer.png").convert_alpha(), "wingman_powerup")
        self.screen_bounds = screen_bounds
        self.rotation = 0
        self.position = pygame.math.Vector2(x, y)
        self.image = pygame.transform.scale(self.image, (75, 50))
        self.original_image = self.image
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 130

    def update(self, dt, screen_bounds):
        self.rotation += 1
        if self.rotation == 360:
            self.rotation = 0

        self.position.y += self.speed * dt
        rotated_image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = rotated_image.get_rect(center=self.position)
        self.image = rotated_image

        if self.position.y > screen_bounds.height:
            self.kill()

    def apply(self, player):
        if player.allies.__len__() < 1:
            ally = Wingman(player.position.x - 50, player.position.y, player, player.game_state)
            player._allies.add(ally)
            player.allies.append(ally)
            return ally
        self.kill()