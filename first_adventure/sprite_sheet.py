import pygame, sys
from pygame.locals import *

# usage: load sprite sheet: my_sprite_sheet = Sprite_sheet( os.path.join( 'data', filename ) )
# get list of images based on rects (x,y,w,h): images[] = my_sprite_sheet.images_at( rect1, rect2 )
class Sprite_sheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None, flipped = False):
        "Loads image from x,y,x+offset,y+offset"
        image = self.sheet.subsurface(rectangle)
        if flipped:
            image = pygame.transform.flip(image, True, False)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None, flipped = False):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey, flipped) for rect in rects]

# returns an animation based on a list of images, get_image cycles through frames
class Animated_sprite_sheet(object):
    # images is a list of images to animate, frames is how long to leave each image on the screen
    def __init__(self, images, frames, loop = True):
        self.images = images
        self.frames = frames
        self.count = 0 # loop through for frames
        self.image_index = 0 # which image to display
        self.loop = loop
        self.rectangle = self.images[0].get_rect()
    def get_image(self):
        image = self.images[self.image_index]
        self.rectangle = image.get_rect()
        self.count += 1
        if self.count >= self.frames:
            self.count = 0
            self.image_index += 1
            if self.image_index >= len(self.images):
                if self.loop == True:
                    self.image_index = 0
                elif self.loop == False:
                    self.image_index = len(self.images) - 1
        return image
