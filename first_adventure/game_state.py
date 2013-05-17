import sys
import pygame
from pygame.locals import *
from system_constants import *
from entity import *
from wave_manager import *

# base class: Game_state
class Game_state( object ):
    def __init__(self, main_surface, game_states, start_time):
        # initialize constants, append this state to stack of game states
        self.main_surface = main_surface
        self.state_surface = main_surface.convert_alpha()
        self.is_active = True
        self.game_states = game_states
        self.game_states.append( self )
        self.run_time = 0
        self.start_time = start_time
        pygame.mouse.set_visible( True )
    def load_data(self):
        # load all art assets
        pass
    def get_input(self):
        # get user input
        pass
    def update_logic(self):
        # update game logic based on one tick
        pass
    def draw(self):
        # draw to state surface, blit state surface onto main surface
        pass
    def free_data(self):
        # free all art assets
        pass
    def run(self, main_playtime):
        # main loop for game state, return True if state still active
        # run for 1 game tick: get input, update logic, draw
        pass

# class Play_state extends base Game_state
class Play_state( Game_state ):
    def __init__(self, main_surface, game_states, start_time, player_selection ):
        Game_state.__init__(self, main_surface, game_states, start_time)
        # initialize player variables
        self.player_invulnerable = False
        self.space_pressed = False
        self.space_pressed_time = 0
        self.player_score = 0
        self.projectiles = []

        # initialize enemies
        self.enemies = []
        self.dead_enemies = []
        
        # initialize wave variables
        if player_selection == KITTEN:
            self.smart_enemy_selection = POLAR_BEAR_SPRITE
            self.dumb_enemy_selection = KITTEN_SPRITE
            self.projectile_color = COLOR_RED
        elif player_selection == POLAR_BEAR:
            self.smart_enemy_selection = KITTEN_SPRITE
            self.dumb_enemy_selection = POLAR_BEAR_SPRITE
            self.projectile_color = COLOR_BLUE
        self.wave_manager = Wave_manager( self.smart_enemy_selection, self.dumb_enemy_selection )
        self.last_spawn_time = 0
        self.wave_start_time = self.start_time
        self.wave_1 = True
        self.wave_2 = False
        self.wave_3 = False
        self.wave_4 = False
        self.wave_4_count = 0
        self.boss_started = False

        # hide mouse for gameplay
        pygame.mouse.set_visible( False )

        self.load_data( player_selection )

    def load_data(self, player_selection ):
        # load all art assets
        self.player_entity = Player_entity( player_selection )

        # score
        self.font_score = pygame.font.SysFont( None, TEXT_SCORE_SIZE ) # (font[none=sysdefault],size)
        self.text_score = self.font_score.render( 'SCORE: ' + str(self.player_score),
                                                  ANTI_ALIASING, COLOR_WHITE, COLOR_BLACK )
        self.text_score_rect = self.text_score.get_rect()
        self.text_score_rect.bottomleft = ( 15, SCREEN_HEIGHT - 15 )

    def get_input(self):
        # get user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.dict['key']
                if key == K_UP:
                    self.player_entity.move_up = True
                    self.player_entity.move_down = False
                elif key == K_DOWN:
                    self.player_entity.move_down = True
                    self.player_entity.move_up = False
                elif key == K_LEFT:
                    self.player_entity.move_left = True
                    self.player_entity.move_right = False
                elif key == K_RIGHT:
                    self.player_entity.move_right = True
                    self.player_entity.move_left = False
                elif key == K_SPACE:
                    self.player_entity.move_shoot = True
                    self.space_pressed = True
                    self.space_pressed_time = self.run_time
                    # generate a new projectile if there aren't too many on screen
                    if len(self.projectiles) < PROJECTILE_NUMBER:
                        new_projectile = Projectile_entity(self.player_entity.get_projectile_position(), 
                                                           self.projectile_color)
                        self.projectiles.append( new_projectile )
                elif key == K_ESCAPE:
                    self.terminate()
            elif event.type == KEYUP:
                key = event.dict['key']
                if key == K_UP:
                    self.player_entity.move_up = False
                elif key == K_DOWN:
                    self.player_entity.move_down = False
                elif key == K_LEFT:
                    self.player_entity.move_left = False
                elif key == K_RIGHT:
                    self.player_entity.move_right = False
                elif key == K_SPACE:
                    self.player_entity.move_shoot = False
                    self.space_pressed = False
    def update_logic(self):
        # update game logic based on one tick
        # update based on priority!
        # update player
        self.player_entity.update()
        
        if self.space_pressed:
            if self.run_time - self.space_pressed_time >= SHOOT_RELOAD_TIME:
                if len(self.projectiles) < PROJECTILE_NUMBER:
                    new_projectile = Projectile_entity(self.player_entity.get_projectile_position(), self.projectile_color)
                    self.projectiles.append( new_projectile ) 
                    self.space_pressed_time = self.run_time

        # check to reset invulnerability
        if self.player_invulnerable and ( self.run_time - self.invulnerable_start_time ) >= PLAYER_INVULNERABLE_TIME :
            self.player_invulnerable = False

        # update enemies, check for collisions between player
        for enemy in self.enemies[:]:
            if enemy.update( self.player_entity.position[1] ):
                self.enemies.extend( self.wave_manager.get_wave_random() )
            if enemy.rectangle.colliderect( self.player_entity.get_hitbox() ):
                if self.player_invulnerable == False: # only hurt player if not invulnerable
                    if self.player_entity.health > 0:
                        # the player has been hit!
                        self.player_entity.health -= 1
                        self.player_score -= 200
                        self.player_invulnerable = True
                        self.invulnerable_start_time = self.run_time
                        if self.player_entity.health == 0:
                            # the player is dead!
                            self.terminate( GAME_LOSE )
                    else:
                        # initiate lose screen
                        self.terminate( GAME_LOSE )
            elif enemy.rectangle.right <= 0: # delete enemy since off screen
                self.enemies.remove( enemy )
                del enemy

        # check for collisions between projectiles and enemies
        for projectile in self.projectiles[:]:
            for enemy in self.enemies[:]:
                if projectile.rectangle.colliderect( enemy.rectangle ):
                    # insert code here to de-activate enemy, initiate death animation, update player score
                    if enemy.is_boss:
                        if enemy.health <= 0: # boss is dead
                            enemy.is_dead( self.run_time )
                            self.player_score += 500
                            self.enemies.remove( enemy )
                            self.dead_enemies.append( enemy )
                        else:
                            enemy.health -= 1
                    else: # normal npc
                        enemy.is_dead( self.run_time )
                        if enemy.smart == True:
                            self.player_score += 50
                        elif enemy.smart == False:
                            self.player_score += 10
                        self.enemies.remove( enemy )
                        self.dead_enemies.append( enemy )
                    projectile.is_active = False
            if projectile.is_active == False:
                self.projectiles.remove( projectile )
                del projectile

        # update projectiles, delete if reached the edge of the screen
        for projectile in self.projectiles[:]:
            if projectile.update() == False:
                self.projectiles.remove( projectile )
                del projectile

        # update dead enemies, delete if animation is over
        for dead_enemy in self.dead_enemies[:]:
            if dead_enemy.is_done( self.run_time ):
                self.dead_enemies.remove( dead_enemy )
                del dead_enemy

        # spawn new enemies
        time_elapsed = self.run_time - self.wave_start_time
        time_since_last_spawn = self.run_time - self.last_spawn_time
        if self.wave_1 == True:
            if time_since_last_spawn >= WAVE_1_TIME:
                if time_elapsed >= ( WAVE_1_TIME * 4 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_6s() )
                    # this wave is complete, start next wave
                    self.wave_1 = False
                    self.wave_2 = True
                    self.wave_start_time = self.run_time
                elif time_elapsed >= ( WAVE_1_TIME * 3 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3d3s() )
                elif time_elapsed >= ( WAVE_1_TIME * 2):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3s() )
                elif time_elapsed >= ( WAVE_1_TIME * 1 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_6d() )
                elif time_elapsed >= 0:
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3d() )
        elif self.wave_2 == True:
            if time_since_last_spawn >= WAVE_2_TIME:
                if time_elapsed >= ( WAVE_2_TIME * 4 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_6s() )
                    # this wave is complete, start next wave
                    self.wave_2 = False
                    self.wave_3 = True
                    self.wave_start_time = self.run_time
                elif time_elapsed >= ( WAVE_2_TIME * 3 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3d3s() )
                elif time_elapsed >= ( WAVE_2_TIME * 2):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3s() )
                elif time_elapsed >= ( WAVE_2_TIME * 1 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_6d() )
                elif time_elapsed >= 0:
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3d() )
        elif self.wave_3 == True:
            if time_since_last_spawn >= WAVE_3_TIME:
                if time_elapsed >= ( WAVE_3_TIME * 4 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_6s() )
                    # this wave is complete, start next wave
                    self.wave_3 = False
                    self.wave_4 = True
                    self.wave_start_time = self.run_time
                elif time_elapsed >= ( WAVE_3_TIME * 3 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3d3s() )
                elif time_elapsed >= ( WAVE_3_TIME * 2):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3s() )
                elif time_elapsed >= ( WAVE_3_TIME * 1 ):
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_6d() )
                elif time_elapsed >= 0:
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_3d() )
        elif self.wave_4 == True:
            if time_since_last_spawn >= WAVE_4_TIME:
                self.wave_4_count += 1
                if self.wave_4_count < WAVE_4_LENGTH:
                    self.last_spawn_time = self.run_time
                    self.enemies.extend( self.wave_manager.get_wave_random() )
                else:
                    if self.boss_started == False:
                        boss_entity = Boss_entity()
                        self.enemies.append( boss_entity )
                        self.boss_started = True
                    else:
                        # last wave complete, check for win
                        if self.enemies == []:
                            self.terminate( GAME_WIN )
                        
    def draw(self):
        # draw to the main surface
        # draw in priority of importance on screen!
        if self.player_invulnerable and ( self.run_time - self.invulnerable_start_time <= INVULNERABLE_ANIMATION_TIME ):
            self.state_surface.fill( COLOR_RED )
        else:
            self.state_surface.fill( COLOR_BLACK )

        # draw player score
        self.text_score = self.font_score.render( 'SCORE: ' + str(self.player_score),
                                                  ANTI_ALIASING, COLOR_WHITE, COLOR_BLACK )
        self.state_surface.blit( self.text_score, self.text_score_rect )

        # draw dead enemies
        for dead_enemy in self.dead_enemies:
            dead_enemy.draw( self.state_surface )

        # draw projectiles
        for projectile in self.projectiles:
            projectile.draw( self.state_surface )

        # draw enemies
        for enemy in self.enemies:
            enemy.draw( self.state_surface )

        # draw player
        self.player_entity.draw( self.state_surface )

        # blit surface to main display
        self.main_surface.blit( self.state_surface, (0,0) )
        pygame.display.flip()
    def free_data(self):
        # free all art assets
        pass
    def terminate(self, condition = ''):
        self.is_active = False
        pygame.mouse.set_visible( True )
        if condition == GAME_LOSE or condition == GAME_WIN:
            game_over_state = Game_over_state( self.main_surface, self.game_states, self.run_time, 
                                               self.player_score, condition )
        else:
            # neither win nor lose, just pressed 'esc'
            pass
    def run(self, main_playtime):
        # main loop for game state, return True if state still active
        # run for 1 game tick: get input, update logic, draw
        self.run_time = main_playtime
        self.get_input()
        self.update_logic()
        self.draw()
        return self.is_active

# class Menu_state extends base Game_state
class Menu_state( Game_state ):
    def __init__(self, main_surface, game_states, start_time):
        Game_state.__init__(self, main_surface, game_states, start_time)
        self.load_data()
        self.mouse_over_start = False
    def load_data(self):
        # load all art assets
        self.font_title = pygame.font.SysFont( None, TEXT_TITLE_SIZE ) # (font[none=sysdefault],size)
        self.font_start = pygame.font.SysFont( None, TEXT_SELECTION_SIZE )
        self.font_info = pygame.font.SysFont( None, TEXT_INFO_SIZE )
        self.text_title = self.font_title.render( SCREEN_CAPTION, ANTI_ALIASING, COLOR_BLUE, COLOR_BLACK )
        # ( Text, Anti-Aliasing, Foreground Color, Background Color )
        self.text_title_rect = self.text_title.get_rect()
        self.text_title_rect.centerx = SCREEN_WIDTH / 2
        self.text_title_rect.centery = SCREEN_HEIGHT / 4
        self.text_start = self.font_start.render( "START", ANTI_ALIASING, COLOR_RED, COLOR_BLACK )
        self.text_start_green = self.font_start.render( "START", ANTI_ALIASING, COLOR_GREEN, COLOR_BLACK )
        self.text_start_rect = self.text_start.get_rect()
        self.text_start_rect.centerx = SCREEN_WIDTH / 2
        self.text_start_rect.centery = (SCREEN_HEIGHT * 3) / 4
        self.text_info = self.font_info.render( GAME_INSTRUCTIONS, ANTI_ALIASING, COLOR_WHITE, COLOR_BLACK )
        self.text_info_rect = self.text_info.get_rect()
        self.text_info_rect.centerx = SCREEN_WIDTH / 2
        self.text_info_rect.centery = SCREEN_HEIGHT / 2
    def get_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.text_start_rect.collidepoint(event.pos): # if user clicked on START
                    # self.is_active = False # comment out to return to main menu later
                    character_select_state = Character_select_state( self.main_surface, 
                                                                     self.game_states,
                                                                     self.run_time )
                    self.mouse_over_start = False
            elif event.type == MOUSEMOTION:
                if self.text_start_rect.collidepoint(event.pos):
                    self.mouse_over_start = True
                else:
                    self.mouse_over_start = False
            elif event.type == KEYDOWN:
                key = event.dict['key']
                if key == K_ESCAPE:
                    self.is_active = False
    def update_logic(self):
        # update game logic based on one tick
        pass
    def draw(self):
        # draw to the main surface
        self.state_surface.fill( COLOR_BLACK )
        self.state_surface.blit( self.text_title, self.text_title_rect )
        self.state_surface.blit( self.text_info, self.text_info_rect )
        if self.mouse_over_start == True:
            self.state_surface.blit( self.text_start_green, self.text_start_rect )
        else:
            self.state_surface.blit( self.text_start, self.text_start_rect )
        self.main_surface.blit( self.state_surface, (0,0) )
        pygame.display.flip()
    def free_data(self):
        # free all art assets
        pass
    def run(self, main_playtime):
        # main loop for game state, return True if state still active
        self.run_time = main_playtime
        self.get_input()
        self.update_logic()
        self.draw()
        return self.is_active

# class Character_select_state extends base Game_state
class Character_select_state( Game_state ):
    def __init__(self, main_surface, game_states, start_time):
        Game_state.__init__(self, main_surface, game_states, start_time)
        self.load_data()
        self.mouse_over_start = False
        self.character_selected = ''
    def load_data(self):
        # load all art assets
        self.font_title = pygame.font.SysFont( None, TEXT_TITLE_SIZE ) # (font[none=sysdefault],size)
        self.font_start = pygame.font.SysFont( None, TEXT_SELECTION_SIZE )
        self.text_title = self.font_title.render( "CHOOSE YOUR CHARACTER", ANTI_ALIASING, COLOR_BLUE, COLOR_BLACK )
        # ( Text, Anti-Aliasing, Foreground Color, Background Color )
        self.text_title_rect = self.text_title.get_rect()
        self.text_title_rect.centerx = SCREEN_WIDTH / 2
        self.text_title_rect.centery = SCREEN_HEIGHT / 5
        self.text_start = self.font_start.render( "PLAY!", ANTI_ALIASING, COLOR_RED, COLOR_BLACK )
        self.text_start_green = self.font_start.render( "PLAY!", ANTI_ALIASING, COLOR_GREEN, COLOR_BLACK )
        self.text_start_rect = self.text_start.get_rect()
        self.text_start_rect.centerx = SCREEN_WIDTH / 2
        self.text_start_rect.centery = (SCREEN_HEIGHT * 4) / 5
        # load characters to select
        player_sprite_sheet = Sprite_sheet( os.path.join( os.pardir, DATA, PLAYER_SPRITE_SHEET ) )
        # small kitten jump (move up)
        rects = [ (202,88,111,78), 
                  (315,88,127,66), 
                  (2,173,107,77), 
                  (111,173,91,87) ]
        frames = 10
        flipped = True
        looped = False
        # idle animation loops once on open screen (Loop = False)
        kitten_images = player_sprite_sheet.images_at( rects, -1, flipped )
        kitten_images_2x = []
        for image in kitten_images:
            kitten_images_2x.append( pygame.transform.scale2x( image ).convert_alpha() )
        self.kitten_idle = Animated_sprite_sheet( kitten_images_2x, frames, looped )
        frames = 20
        looped = True
        # selected animation loops while selected (Loop = True)
        self.kitten_selected = Animated_sprite_sheet( kitten_images_2x, frames, looped )

        # small bear jump (move up)
        frames = 10
        flipped = False
        looped = False
        rects = [ (2,2,92,76), 
                  (96,2,82,80), 
                  (180,2,99,56), 
                  (281,2,90,84) ]
        bear_images = player_sprite_sheet.images_at( rects, -1, flipped )
        bear_images_2x = []
        for image in bear_images:
            bear_images_2x.append( pygame.transform.scale2x( image ).convert_alpha() )
        self.bear_idle = Animated_sprite_sheet( bear_images_2x, frames, False )
        frames = 10
        looped = True
        self.bear_selected = Animated_sprite_sheet( bear_images_2x, frames, True )
        self.bear_y = ( SCREEN_HEIGHT * 4 ) / 7
        self.bear_x = ( SCREEN_WIDTH * 2 ) / 7
        self.kitten_x = ( SCREEN_WIDTH * 5 ) / 7
        self.kitten_y = ( SCREEN_HEIGHT * 4 ) / 7
        self.bear_rect = pygame.Rect( self.bear_x, self.bear_y, 
                                      self.bear_idle.rectangle.width, 
                                      self.bear_idle.rectangle.height )
        self.bear_rect.centerx = self.bear_x
        self.bear_rect.centery = self.bear_y
        self.kitten_rect = pygame.Rect( self.kitten_x, self.kitten_y, 
                                        self.kitten_idle.rectangle.width, 
                                        self.kitten_idle.rectangle.height )
        self.kitten_rect.centerx = self.kitten_x
        self.kitten_rect.centery = self.kitten_y

        del rects, bear_images, bear_images_2x, kitten_images, kitten_images_2x
    def get_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.text_start_rect.collidepoint(event.pos): # if user clicked on START
                    if self.character_selected == POLAR_BEAR or self.character_selected == KITTEN:
                        self.is_active = False
                        game_play_state = Play_state( self.main_surface, self.game_states, 
                                                      self.run_time, self.character_selected )
                        self.mouse_over_start = False
                if self.bear_rect.collidepoint(event.pos): # user clicked on bear
                    self.character_selected = POLAR_BEAR
                if self.kitten_rect.collidepoint(event.pos): # user clicked on kitten
                    self.character_selected = KITTEN
            elif event.type == MOUSEMOTION:
                if self.text_start_rect.collidepoint(event.pos):
                    self.mouse_over_start = True
                else:
                    self.mouse_over_start = False
            elif event.type == KEYDOWN:
                key = event.dict['key']
                if key == K_ESCAPE:
                    self.is_active = False
    def update_logic(self):
        # update game logic based on one tick
        pass
    def draw(self):
        # draw to the main surface
        # draw background
        self.state_surface.fill( COLOR_BLACK )
        # draw title
        self.state_surface.blit( self.text_title, self.text_title_rect )
        # draw play if a character has been selected
        if self.character_selected == POLAR_BEAR or self.character_selected == KITTEN:
            if self.mouse_over_start == True:
                self.state_surface.blit( self.text_start_green, self.text_start_rect )
            else:
                self.state_surface.blit( self.text_start, self.text_start_rect )
        # draw bear
        if self.character_selected == POLAR_BEAR:
            self.state_surface.blit( self.bear_selected.get_image(), self.bear_rect.topleft )
        else:
            self.state_surface.blit( self.bear_idle.get_image(), self.bear_rect.topleft )
        # draw kitten
        if self.character_selected == KITTEN:
            self.state_surface.blit( self.kitten_selected.get_image(), self.kitten_rect.topleft )
        else:
            self.state_surface.blit( self.kitten_idle.get_image(), self.kitten_rect.topleft )
        self.main_surface.blit( self.state_surface, (0,0) )
        pygame.display.flip()
    def free_data(self):
        # free all art assets
        pass
    def run(self, main_playtime):
        # main loop for game state, return True if state still active
        self.run_time = main_playtime
        self.get_input()
        self.update_logic()
        self.draw()
        return self.is_active

# class Game_over_state extends base Game_state
class Game_over_state( Game_state ):
    def __init__(self, main_surface, game_states, start_time, player_score, game_outcome = ''):
        Game_state.__init__(self, main_surface, game_states, start_time)
        self.player_score = player_score
        self.mouse_over_start = False
        self.game_outcome = game_outcome
        self.load_data()
    def load_data(self):
        # load all art assets
        self.font_title = pygame.font.SysFont( None, TEXT_MESSAGE_SIZE ) # (font[none=sysdefault],size)
        self.font_start = pygame.font.SysFont( None, TEXT_SELECTION_SIZE )
        self.font_info = pygame.font.SysFont( None, TEXT_INFO_SIZE )
        if self.game_outcome == GAME_LOSE:
            self.text_title = self.font_title.render( "YOU LOSE", ANTI_ALIASING, COLOR_RED, COLOR_BLACK )
        elif self.game_outcome == GAME_WIN:
            self.text_title = self.font_title.render( "YOU WIN", ANTI_ALIASING, COLOR_GREEN, COLOR_BLACK )
        else:
            self.text_title = self.font_title.render( "GAME OVER?", ANTI_ALIASING, COLOR_BLUE, COLOR_BLACK )
        # ( Text, Anti-Aliasing, Foreground Color, Background Color )
        self.text_title_rect = self.text_title.get_rect()
        self.text_title_rect.centerx = SCREEN_WIDTH / 2
        self.text_title_rect.centery = SCREEN_HEIGHT / 4
        self.text_start = self.font_start.render( "RETRY?", ANTI_ALIASING, COLOR_RED, COLOR_BLACK )
        self.text_start_green = self.font_start.render( "RETRY!", ANTI_ALIASING, COLOR_GREEN, COLOR_BLACK )
        self.text_start_rect = self.text_start.get_rect()
        self.text_start_rect.centerx = SCREEN_WIDTH / 2
        self.text_start_rect.centery = (SCREEN_HEIGHT * 3) / 4

        # read high score
        high_score = open( os.path.join( os.pardir, DATA, HIGH_SCORE ), 'r' )
        high_scores = high_score.readlines()
        high_score.close()
        old_high_score = high_scores[0]
        # check if new high score
        if( self.player_score > int(old_high_score) ):
            # write player score to high score
            high_score = open( os.path.join( os.pardir, DATA, HIGH_SCORE ), 'w' )
            high_score.write( str( self.player_score ) )
            high_score.close()

        self.text_score_old = self.font_info.render( 'HIGH SCORE: ' + old_high_score, 
                                                     ANTI_ALIASING, COLOR_WHITE, COLOR_BLACK )
        self.text_score_old_rect = self.text_score_old.get_rect()
        self.text_score_old_rect.centerx = SCREEN_WIDTH / 2
        self.text_score_old_rect.centery = (SCREEN_HEIGHT * 2) / 5

        self.text_score_new = self.font_info.render( 'YOUR SCORE: ' + str(self.player_score),
                                                     ANTI_ALIASING, COLOR_WHITE, COLOR_BLACK )
        self.text_score_new_rect = self.text_score_new.get_rect()
        self.text_score_new_rect.centerx = SCREEN_WIDTH / 2
        self.text_score_new_rect.centery = (SCREEN_HEIGHT * 3) / 5

    def get_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.text_start_rect.collidepoint(event.pos): # if user clicked on RETRY
                    # clear this state, return to menu state (still on stack)
                    self.is_active = False
                    self.mouse_over_start = False
            elif event.type == MOUSEMOTION:
                if self.text_start_rect.collidepoint(event.pos):
                    self.mouse_over_start = True
                else:
                    self.mouse_over_start = False
            elif event.type == KEYDOWN:
                key = event.dict['key']
                if key == K_ESCAPE:
                    self.is_active = False
    def update_logic(self):
        # update game logic based on one tick
        pass
    def draw(self):
        # draw to the main surface
        self.state_surface.fill( COLOR_BLACK )
        self.state_surface.blit( self.text_title, self.text_title_rect )
        self.state_surface.blit( self.text_score_old, self.text_score_old_rect )
        self.state_surface.blit( self.text_score_new, self.text_score_new_rect )
        if self.mouse_over_start == True:
            self.state_surface.blit( self.text_start_green, self.text_start_rect )
        else:
            self.state_surface.blit( self.text_start, self.text_start_rect )
        self.main_surface.blit( self.state_surface, (0,0) )
        pygame.display.flip()
    def free_data(self):
        # free all art assets
        pass
    def run(self, main_playtime):
        # main loop for game state, return True if state still active
        self.run_time = main_playtime
        self.get_input()
        self.update_logic()
        self.draw()
        return self.is_active
