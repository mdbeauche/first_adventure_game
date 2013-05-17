# #!/usr/bin/python
# ^ location of python (system constant) makes file executable

# filename: main
# desc: overall program wrapper
# copyright holder

# start project wide import
import sys, os
import pygame
# start system wide definitions
# import colors constants
# import system constants
from system_constants import *
# import game constants
# end system wide definitions

# start internal classes
# import classes
from game_state import *
#import player_sprite
# end internal classes

# end project wide import

def main():
    pygame.init()

    # initialize main surface
    main_surface = pygame.display.set_mode( (SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32 )
    pygame.display.toggle_fullscreen()
    pygame.display.set_caption( SCREEN_CAPTION )
    pygame.display.set_icon( pygame.image.load( os.path.join( os.pardir, DATA, WINDOW_ICON ) ).convert_alpha() ) # 32x32
    main_surface.fill( COLOR_BLACK )

    # initialize stack of game states
    game_states = []

    # initialize game clock
    main_clock = pygame.time.Clock()
    main_playtime = 0

    # initialize music
    #pygame.mixer.init()
    #pygame.mixer.music.load( os.path.join( os.pardir, DATA, BG_MUSIC ) )
    #pygame.mixer.music.play( 0, 0.0 )

    # initialize first game state, place on stack of game states (done by init)
    # pass game_states so that this game state can add new game states to the stack
    game_menu_state = Menu_state( main_surface, game_states, main_playtime )

    # begin evaluation of stack of game states
    while( game_states != [] ):
        # take top game state off the stack
        current_game_state = game_states.pop()
        
        # place game state back on the stack
        # each game state may add new game states on top of the stack
        # therefore place game state back on stack so stack abstract is maintained
        game_states.append( current_game_state )

        # run game state for a tick ( GAME_SPEED )
        current_game_state_is_active = current_game_state.run( main_playtime )
        
        # take game state off the stack if no longer active
        if( current_game_state_is_active == False ):
            game_states.remove( current_game_state )
            del current_game_state

        milliseconds = main_clock.tick( GAME_SPEED ) # stores milliseconds since last frame
        main_playtime += milliseconds / 1000.0 # adds seconds to playtime

    # exit
    pygame.quit()
    sys.exit()
		
# run game
if __name__ == '__main__':
    main()
