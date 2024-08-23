class GamestateManager:
    def __init__(self):
        self.states = {}
        self.active_state = None

    # Ensure manager sees gamestates
    def register_state(self, state):
        if state.name not in self.states:
            self.states[state.name] = state

    # As long as we have an active state, stay in the gameloop. Otherwise, exit the loop
    def run(self, screen, dt):
        if self.active_state is not None:
            self.active_state.run(screen, dt)
            # If any state calls for the game to quit, exit gameloop
            if self.active_state.time_to_quit:
                return False
        return True

    # Called AFTER all states have been loaded and sets the initial gamestate
    def set_initial_state(self, name):
        if name in self.states:
            self.active_state = self.states[name]
            self.active_state.start()