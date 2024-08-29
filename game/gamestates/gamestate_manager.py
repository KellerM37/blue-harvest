from game.gamestates.main_menu import MainMenu
from game.gamestates.settings_menu import SettingsMenu

class GamestateManager:
    def __init__(self):
        self.states = {}
        self.active_state = None

    # Loads all gamestates, can be recalled to update gamestates
    def load_states(self, ui_manager, gamestate_manager):
        SettingsMenu(ui_manager, gamestate_manager)
        MainMenu(ui_manager, gamestate_manager)

    # Ensure manager sees gamestates
    def register_state(self, state):
        if state.name not in self.states:
            self.states[state.name] = state

    # As long as we have an active state, stay in the gameloop. Otherwise, exit the loop
    def run(self, screen, dt):
        if self.active_state is not None:
            self.active_state.run(screen, dt)
            # If any state calls for the game to quit, exit gameloop
            if self.active_state.transition:
                self.active_state.transition = False
                to_state = self.active_state.new_state
                self.active_state.end()
                self.active_state = self.states[to_state]
                self.active_state.start()
                print(f"Transitioning to {to_state}")
            if self.active_state.time_to_quit:
                return False
        return True

    # Called AFTER all states have been loaded and sets the initial gamestate
    def set_initial_state(self, name):
        if name in self.states:
            self.active_state = self.states[name]
            self.active_state.start()