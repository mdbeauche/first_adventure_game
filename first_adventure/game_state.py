# base class: game_state
class game_state( object ):
    def __init__(self):
        # initialize constants
        self.is_active = False
    def load_data(self):
        # load all art assets
    def update_logic(self):
        # update game logic based on one tick
    def draw(self):
        # draw to the main surface
    def free_data(self):
        # free all art assets

# class play_state extends base game_state
class play_state( game_state ):
    def __init__(self):
        game_state.__init__(self)

# class menu_state extends base game_state
class menu_state( game_state ):
    def __init__(self):
        game_state.__init__(self)

# class video_state extends base game_state
class video_state( game_state ):
    def __init__(self):
        game_state.__init__(self)

# class options_state extends base game_state
class options_state( game_state ):
    def __init__(self):
        game_state.__init__(self)

# class win_state extends base game_state
class win_state( game_state ):
    def __init__(self):
        game_state.__init__(self)
