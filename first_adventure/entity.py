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

class Kitten_player_entity(Entity):
    def __init__(self):
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
        flipped = False
        frames = 15
        player_sprite_sheet = Sprite_sheet( os.path.join( os.pardir, DATA, PLAYER_SPRITE_SHEET ) )
        # small kitten jump part (shoot)
        rects = [ (315,88,127,66) ]
        self.shoot_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
        # small kitten jump (move up)
        rects = [ (202,88,111,78), 
                  (315,88,127,66), 
                  (2,173,107,77), 
                  (111,173,91,87) ]
        self.move_up_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
        # small kitten jump (move down)
        rects = [ (202,88,111,78), 
                  (315,88,127,66), 
                  (2,173,107,77), 
                  (111,173,91,87) ]
        self.move_down_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
        # small kitten run (right)
        rects = [ (204,173,80,82),
                  (286,173,112,77),
                  (400,173,84,84) ]
        self.move_right_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
        # small kitten run (left)
        flipped = True
        rects = [ (204,173,80,82),
                  (286,173,112,77),
                  (400,173,84,84) ]
        self.move_left_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
        flipped = False
        rects = [ (400,173,84,84) ]
        self.idle_animation = Animated_sprite_sheet( player_sprite_sheet.images_at( rects, -1, flipped ), frames )
        self.current_animation = self.idle_animation
    def update(self):
        # move the player to a new position
        if self.move_left:
            self.current_animation = self.move_left_animation
            if self.position[0] > 0:
                self.position = ( self.position[0] - self.move_speed, self.position[1] )
                self.current_animation.rectangle.topleft = self.position
        if self.move_right:
            self.current_animation = self.move_right_animation
            if self.position[0] < SCREEN_WIDTH:
                self.position = ( self.position[0] + self.move_speed, self.position[1] )
                self.current_animation.rectangle.topleft = self.position
        if self.move_up:
            self.current_animation = self.move_up_animation
            if self.position[1] > 0:
                self.position = ( self.position[0], self.position[1] - self.move_speed )
                self.current_animation.rectangle.topleft = self.position
        if self.move_down:
            self.current_animation = self.move_down_animation
            if self.position[1] < SCREEN_HEIGHT:
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
        # 127, 33 based on kitten sprite
        return ( self.position[0] + 127, self.position[1] + 33 )

class Enemy_entity(Entity):
    def __init__(self, position):
        self.position = position
        self.move_speed = NPC_MOVE_SPEED
        self.image = pygame.image.load( os.path.join( os.pardir, DATA, POLAR_BEAR_SPRITE ) ).convert_alpha()
        self.image = pygame.transform.flip( self.image, True, False )
        self.rectangle = self.image.get_rect()
    def update(self):
        new_position = ( self.position[0] - self.move_speed, self.position[1] )
        self.position = new_position
        self.rectangle.left = new_position[0]
        self.rectangle.top = new_position[1]
    def draw(self,target_surface):
        target_surface.blit( self.image, self.position )

class Projectile_entity(Entity):
    def __init__(self, pos, color):
        self.bounding_rectangle = pygame.Rect( pos[0], pos[1], PROJECTILE_SIZE, PROJECTILE_SIZE )
        self.color = color
    def update(self):
        new_position = self.bounding_rectangle.centerx + PROJECTILE_SPEED
        if new_position <= SCREEN_WIDTH:
            self.bounding_rectangle.left = new_position
            return True
        else:
            return False
    def draw(self,target_surface):
        pygame.draw.circle( target_surface, self.color, 
                            (self.bounding_rectangle.centerx, self.bounding_rectangle.centery),
                            PROJECTILE_SIZE, 0 )
        
