import pygame
import pygame_gui
from game.data.settings import *

from game.data.gamestate_manager import GamestateManager


def main():
    # Initializing pygame, window, delta_time, and UI master
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
    icon = pygame.image.load("ui/LOGO.jpeg")
    pygame.display.set_caption(f"{TITLE} Version: {VERSION}")
    pygame.display.set_icon(icon)
    ui_manager = pygame_gui.UIManager(screen.get_size(), "ui/ui_theme.json")
    clock = pygame.time.Clock()
    dt = 0
    is_running = True

    # Initializing the Gamestate Manager and setting main_menu as the initial state.
    gamestate_manager = GamestateManager()
    gamestate_manager.load_states(ui_manager, gamestate_manager)
    gamestate_manager.set_initial_state(INITIAL_STATE)

    # The almighty game loop
    while is_running:
        dt = clock.tick(60) / 1000
        is_running = gamestate_manager.run(screen, dt)
        pygame.display.flip()
    # We've left the loop. Have a good life
    pygame.quit()


if __name__ == "__main__":
    main()
