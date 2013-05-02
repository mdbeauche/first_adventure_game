# #!/usr/bin/python
# ^ location of python (system constant) makes file executable

# filename: main
# desc: overall program wrapper
# copyright holder

# start project wide import
import pygame
# start system wide definitions
# import colors constants
# import system constants
import system_constants
# import game constants
# end system wide definitions

# start internal classes
# import classes
import game_state
import player_sprite
# end internal classes

# end project wide import

def main():
    # initialize stack of game states
    game_states = []

    # initialize first game state, place on stack of game states
    game_menu_state = menu_state()
    game_states.append( game_menu_state )

    # begin evaluation of stack of game states
    while( game_states != [] ):
        # take top game state off the stack
        current_game_state = game_states.pop()
        
        # run game state for a tick
        # take it off the stack if it returns false, maintain if true
        # pass game_states so that current_game_state can add to the game state stack
        if( current_game_state.run( game_states ) == True ):
            game_states.append( current_game_state )

    # clean up stack of game states, memory

    # exit
		
# run game
main()
