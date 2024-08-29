class BaseGamestate:
    def __init__(self, name, state_manager):
        self.name = name
        self.state_manager = state_manager
        self.transition = False
        self.new_state = None
        self.time_to_quit = False
        self.state_manager.register_state(self)

    def transitioning(self, transition_to):
        self.transition = True

    # To be overridden
    def start(self):
        pass

    # To be overridden
    def run(self):
        pass

    # To be overridden
    def end(self):
        pass