import pygame
import pygame_gui
from data.settings import *

def main():
    # Initializing pygame, window, delta_time, and UI master
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"{TITLE} Version: {VERSION}")
    clock = pygame.time.Clock()
    dt = 0
    is_running = True

    while is_running:
        # FPS limit at 60
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        
        screen.fill(("black"))
        pygame.display.flip()


if __name__ == "__main__":
    main()