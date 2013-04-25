class player_character_sprite(pygame.sprite.DirtySprite):
    def __init__(self):
        super(player_character_sprite, self).__init__()
        self.display = pygame.display.get_surface()

        frame_1 = pygame.image.load("data/images/ninja_frame1.png").convert_alpha()
        frame_2 = pygame.image.load("data/images/ninja_frame2.png").convert_alpha()
        frame_3 = pygame.image.load("data/images/ninja_frame3.png").convert_alpha()
        self.frame_set = [frame_1, frame_2, frame_3, frame_2]
        self.current_frame = 0
        self.timer = time.clock()

        self.image = self.frame_set[self.current_frame]
        self.rect = pygame.Rect((0, 0), (self.image.get_width(), self.image.get_height()))
        self.pos_x = 0
        self.pos_y = self.display.get_height() - (100 + self.rect.height)
        self.is_jumping = False
        self.max_jump_height = 256
        self.current_jump = 0
        self.is_falling = True
