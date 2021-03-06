import os
import pygame
from sprite_sheet import *
from system_constants import *

class Entity(object):
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self,target_surface):
        pass

class Player_entity(Entity):
    def __init__(self, player_selection):
        # player stats
        self.health = PLAYER_HEALTH
        self.position = ( 0, SCREEN_HEIGHT/1.5 )
        self.move_speed = PLAYER_MOVE_SPEED

        # movement variables
        self.facing = RIGHT
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.move_shoot = False

        # animations
        self.load_data( player_selection )

    def load_data(self, player_selection ):
        flipped = False
        player_sprite_sheet = Sprite_sheet( os.path.join( os.pardir, DATA, PLAYER_SPRITE_SHEET ) )

        if player_selection == CAT:
            frames = 10
            # small cat jump part (shoot)
            rects = [ (315,88,127,66) ]
            self.shoot_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            # 127, 33 based on cat sprite
            self.projectile_position = ( 127, 33 )
            # small cat jump (move up)
            rects = [ (202,88,111,78),
                      (315,88,127,66),
                      (2,173,107,77),
                      (111,173,91,87) ]
            self.move_up_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            # small cat jump (move down)
            rects = [ (202,88,111,78),
                      (315,88,127,66),
                      (2,173,107,77),
                      (111,173,91,87) ]
            self.move_down_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            # small cat run (right)
            rects = [ (204,173,80,82),
                      (286,173,112,77),
                      (400,173,84,84) ]
            self.move_right_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            # small cat run (left)
            flipped = True
            rects = [ (204,173,80,82),
                      (286,173,112,77),
                      (400,173,84,84) ]
            self.move_left_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            flipped = False
            rects = [ (400,173,84,84) ]
            self.idle_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            self.current_animation = self.idle_animation
        elif player_selection == BEAR:
            frames = 10
            # small bear jump part (shoot)
            rects = [ (180,2,99,56) ]
            # 99, 28 based on bear sprite
            self.projectile_position = ( 99, 28 )
            self.shoot_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            # small bear jump (move up)
            rects = [ (2,2,92,76),
                      (96,2,82,80),
                      (180,2,99,56),
                      (281,2,90,84) ]
            self.move_up_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            # small bear jump (move down)
            rects = [ (2,2,92,76),
                      (96,2,82,80),
                      (180,2,99,56),
                      (281,2,90,84) ]
            self.move_down_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            # small bear run (right)
            rects = [ (373,2,92,76),
                      (2,88,92,83),
                      (96,88,104,67) ]
            self.move_right_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            # small bear run (left)
            rects = [ (373,2,92,76),
                      (2,88,92,83),
                      (96,88,104,67) ]
            flipped = True
            self.move_left_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            flipped = False
            # small bear idle
            rects = [ (2,2,92,76) ]
            self.idle_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
            self.current_animation = self.idle_animation
        del player_sprite_sheet
        del rects

    def update(self):
        # move the player to a new position
        if self.move_left:
            self.current_animation = self.move_left_animation
            if self.position[0] > 0:
                self.position = ( self.position[0] - self.move_speed, self.position[1] )
                self.current_animation.rectangle.topleft = self.position
        if self.move_right:
            self.current_animation = self.move_right_animation
            x_limiter = self.position[0] + self.current_animation.rectangle.width
            if x_limiter < SCREEN_WIDTH:
                self.position = ( self.position[0] + self.move_speed, self.position[1] )
                self.current_animation.rectangle.topleft = self.position
        if self.move_up:
            self.current_animation = self.move_up_animation
            if self.position[1] > 0:
                self.position = ( self.position[0], self.position[1] - self.move_speed )
                self.current_animation.rectangle.topleft = self.position
        if self.move_down:
            self.current_animation = self.move_down_animation
            y_limiter = self.position[1] + self.current_animation.rectangle.height
            if y_limiter < SCREEN_HEIGHT:
                self.position = ( self.position[0], self.position[1] + self.move_speed )
                self.current_animation.rectangle.topleft = self.position
        if self.move_shoot:
            self.current_animation = self.shoot_animation
        else:
            self.current_animation = self.idle_animation
        # update the player animation
        if self.move_right:
            self.current_animation = self.move_right_animation
        elif self.move_left:
            self.current_animation = self.move_left_animation
        elif self.move_up:
            self.current_animation = self.move_up_animation
        elif self.move_down:
            self.current_animation = self.move_down_animation
        elif self.move_shoot:
            self.current_animation = self.shoot_animation
        else:
            self.current_animation = self.idle_animation
    def draw(self,target_surface):
        # draw player
        target_surface.blit( self.current_animation.get_image(), self.position )
        # draw player health
        # draw red health bars
        for i in range( self.health ):
            pygame.draw.rect( target_surface, COLOR_RED, ( 15, 5 + ( 10 * PLAYER_HEALTH ) - i * 10, 20, 10 ) )
        # draw white outlines
        for i in range( PLAYER_HEALTH ):
            pygame.draw.rect( target_surface, COLOR_WHITE, ( 15, 5 + ( 10 * PLAYER_HEALTH ) - i * 10, 20, 10 ), 1 )
    def get_projectile_position(self):
        return ( self.position[0] + self.projectile_position[0], self.position[1] + self.projectile_position[1] )
    def get_rectangle(self):
        return ( self.position[0], self.position[1],
                 self.current_animation.rectangle.width, self.current_animation.rectangle.height )
    def get_hitbox(self):
        rect = self.get_rectangle()
        rect = ( rect[0] - PLAYER_HITBOX_BUFFER,
                 rect[1] - PLAYER_HITBOX_BUFFER,
                 rect[2] - PLAYER_HITBOX_BUFFER,
                 rect[3] - PLAYER_HITBOX_BUFFER )
        return rect

class Enemy_entity(Entity):
    def __init__(self, position, sprite, smart = False):
        self.position = position
        if smart:
            self.move_speed_x = SMART_NPC_MOVE_SPEED_X
            self.move_speed_y = SMART_NPC_MOVE_SPEED_Y
        else:
            self.move_speed_x = DUMB_NPC_MOVE_SPEED
            self.move_speed_y = DUMB_NPC_MOVE_SPEED
        self.image = pygame.image.load( os.path.join( os.pardir, DATA, sprite ) ).convert_alpha()
        self.image = pygame.transform.flip( self.image, True, False )
        self.rectangle = self.image.get_rect()
        self.smart = smart
        self.is_boss = False
        self.is_alive = True
        self.death_time = 0
        self.load_data( sprite )
    def load_data(self, sprite):
        images = []
        image = pygame.image.load( os.path.join( os.pardir, DATA, sprite ) ).convert_alpha()
        images.append( image )
        image = pygame.transform.rotozoom( image, -90.0, 0.75 ).convert_alpha()
        images.append( image )
        image = pygame.transform.rotozoom( image, -90.0, 0.75 ).convert_alpha()
        images.append( image )
        image = pygame.transform.rotozoom( image, -90.0, 0.75 ).convert_alpha()
        images.append( image )
        self.death_animation = Animated_sprite_sheet( images, 15, False )
        del images
    def update(self, player_y):
        if self.is_alive:
            if self.smart: # run towards player
                new_x = self.position[0] - self.move_speed_x
                if player_y > self.position[1]:
                    new_y = self.position[1] + self.move_speed_y
                elif player_y < self.position[1]:
                    new_y = self.position[1] - self.move_speed_y
                else:
                    new_y = self.position[1]
                new_position = ( new_x, new_y )
            else: # run left like an idiot
                new_position = ( self.position[0] - self.move_speed_x, self.position[1] )
            # update position
            self.position = new_position
            self.rectangle.left = new_position[0]
            self.rectangle.top = new_position[1]
        else: # enemy is dead, don't move any more
            pass
        return False
    def is_done(self, run_time):
        done = ( run_time - self.death_time >= 1.0 )
        return done
    def is_dead(self, run_time):
        self.is_alive = False
        self.death_time = run_time
    def draw(self,target_surface):
        if self.is_alive:
            target_surface.blit( self.image, self.position )
        else:
            target_surface.blit( self.death_animation.get_image(), self.position )

class Projectile_entity(Entity):
    def __init__(self, pos, color):
        self.rectangle = pygame.Rect( pos[0], pos[1], PROJECTILE_SIZE, PROJECTILE_SIZE )
        self.color = color
        self.is_active = True
    def update(self):
        new_position = self.rectangle.centerx + PROJECTILE_SPEED
        if new_position <= SCREEN_WIDTH:
            self.rectangle.left = new_position
            return True
        else:
            return False
    def draw(self,target_surface):
        pygame.draw.circle( target_surface, self.color,
                            (self.rectangle.centerx, self.rectangle.centery),
                            PROJECTILE_SIZE, 0 )

class Boss_entity(Entity):
    def __init__(self):
        self.health = BOSS_HEALTH
        self.move_left = False
        self.move_right = False
        self.move_up = True
        self.move_down = False

        self.is_alive = True
        self.death_time = 0
        self.smart = True
        self.is_boss = True
        self.load_data()

        self.rectangle = self.current_animation.get_image().get_rect()
        self.rectangle.centerx = SCREEN_WIDTH - BOSS_SPACE_BUFFER
        self.rectangle.centery = SCREEN_HEIGHT / 2
        self.position = self.rectangle.topleft
    def load_data(self):
        flipped = False
        frames = 20
        boss_sprite_sheet = Sprite_sheet( os.path.join( os.pardir, DATA, PLAYER_SPRITE_SHEET ) )
        rects = [ (2,262,58,113),
                  (62,262,57,112),
                  (121,262,61,112) ]
        images = boss_sprite_sheet.images_at( rects, -1, flipped )
        images_zoomed = []
        for image in images:
            images_zoomed.append( pygame.transform.scale2x( image ).convert_alpha() )
        self.move_right_animation = Animated_sprite_sheet( images_zoomed, frames )
        flipped = True
        images_2 = boss_sprite_sheet.images_at( rects, -1, flipped )
        images_zoomed_2 = []
        for image in images_2:
            images_zoomed_2.append( pygame.transform.scale2x( image ).convert_alpha() )
        self.move_left_animation = Animated_sprite_sheet( images_zoomed_2, frames )
        self.move_down_animation = self.move_right_animation
        self.move_up_animation = self.move_left_animation
        self.current_animation = self.move_up_animation
        del images, images_2, images_zoomed, images_zoomed_2, rects
    def update(self, player_position): # return True if we should spawn a new wave
        if self.is_alive:
            if self.move_left:
                if self.position[0] <= BOSS_SPACE_BUFFER:
                    self.move_left = False
                    self.move_down = True
                    self.current_animation = self.move_down_animation
                    return True
                else:
                    new_x = self.position[0] - BOSS_MOVE_SPEED
                    self.position = ( new_x, self.position[1] )
                    self.rectangle.topleft = self.position
            elif self.move_right:
                if self.position[0] >= (SCREEN_WIDTH - BOSS_SPACE_BUFFER - self.rectangle.width):
                    self.move_right = False
                    self.move_up = True
                    self.current_animation = self.move_up_animation
                    return True
                else:
                    new_x = self.position[0] + BOSS_MOVE_SPEED
                    self.position = ( new_x, self.position[1] )
                    self.rectangle.topleft = self.position
            elif self.move_up:
                if self.position[1] <= BOSS_SPACE_BUFFER:
                    self.move_up = False
                    self.move_left = True
                    self.current_animation = self.move_left_animation
                    return True
                else:
                    new_y = self.position[1] - BOSS_MOVE_SPEED
                    self.position = ( self.position[0], new_y )
                    self.rectangle.topleft = self.position
            elif self.move_down:
                if self.position[1] >= (SCREEN_HEIGHT - BOSS_SPACE_BUFFER - self.rectangle.height):
                    self.move_down = False
                    self.move_right = True
                    self.current_animation = self.move_right_animation
                    return True
                else:
                    new_y = self.position[1] + BOSS_MOVE_SPEED
                    self.position = ( self.position[0], new_y )
                    self.rectangle.topleft = self.position
        else:
            # dead, do not move anymore
            pass
        return False
    def is_done(self, run_time):
        done = ( run_time - self.death_time >= 1.0 )
        return done
    def is_dead(self, run_time):
        self.is_alive = False
        self.death_time = run_time
        images = []
        image = self.current_animation.get_image()
        images.append( image )
        image = pygame.transform.rotozoom( image, -90.0, 0.75 ).convert_alpha()
        images.append( image )
        image = pygame.transform.rotozoom( image, -90.0, 0.75 ).convert_alpha()
        images.append( image )
        image = pygame.transform.rotozoom( image, -90.0, 0.75 ).convert_alpha()
        images.append( image )
        self.death_animation = Animated_sprite_sheet( images, 15, False )
        self.current_animation = self.death_animation
        del images
    def draw(self,target_surface):
        target_surface.blit( self.current_animation.get_image(), self.position )
