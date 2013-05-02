# #!/usr/bin/python
# ^ location of python (system constant) makes file executable

# filename: first_adventure
# copyright holder
# desc:

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
import player_sprite
# end internal classes

# end project wide import

def main():
    # start game setup
    pygame.init() # prepare the pygame module for use
	
    # initialize clock
    main_clock = pygame.time.Clock()	
	
    # initialize display
    main_surface = pygame.display.set_mode((system_constants.SCREEN_WIDTH,system_constants.SCREEN_HEIGHT))
    pygame.display.set_caption(system_constants.SCREEN_CAPTION)
	
    # load images
	
    # initialize sprites
    main_sprites = []
    # main_sprites.append(sprite)
    # make 2 player characters for now, let them move around in 2d space
    polar_bear_sprite = player_character_sprite(POLAR_BEAR_SPRITE_SHEET, posn, surface)
    main_sprites.append(polar_bear_sprite)
    #kitten_sprite = player_character_sprite(KITTEN_SPRITE_SHEET, posn, surface)
    #main_sprites.append(kitten_sprite)
	
    # initialize game constants
	
    # initialize game music
    #pygame.mixer.music.load( pbSong )
    #pygame.mixer.music.play(-1, 0.0) # (-1) = loop infinitely, 0.0 from time 0.0
	
    # initialize game logic
    main_phase = 0
    # end game setup
	
    main_done = False
    # start game loop (while done == False)
    while main_done == False:
        # poll and handle events (check for input)
        # start event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    player.moveup()
                elif event.key == K_DOWN:
                    player.movedown()
                elif event.key == K_LEFT:
                    player.movedown()
                elif event.key == K_RIGHT:
                    player.movedown()					
            elif event.type == pygame.KEYUP:
                player.moveup()
            # end event processing
	
            # update game elements (move objects)
            # start game logic
            for sprite in main_sprites:
                # update based on game time passed in tick form (main_phase)
                sprite.update(main_phase)
            # end game logic
	
            # draw surface
            # start render
            # draw background
            main_surface.fill(0,0,0) # black stage background
            # draw objects (find a way to draw only what's changed)
            for sprite in main_sprites:
                sprite.draw()
            # end render	
	
            # show surface (update screen)
            pygame.display.flip()
		
            # Increase game tick
            main_phase += 1
		
            main_clock.tick(GAME_SPEED)
            # milliseconds = main_clock.tick(GAME_SPEED) # stores milliseconds since last frame
            # playtime += milliseconds / 1000.0 # adds seconds to playtime
    # end game loop
    # close game
    #pygame.mixer.music.stop()
    pygame.quit()
	
	
# run game
main()