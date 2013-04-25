# prototype class: sprite
class sprite:
    def __init__(self, image, position, surface):
		# sprite specific variables
        self.sprite_sheet = image
        self.x_coordinate = position[0]
		self.y_coordinate = position[1]
		self.surface = surface

    def update(self, target_posn):
		# prototype update logic
		self.x_coordinate = target_posn[0]
		self.y_coordinate = target_posn[1]
    def draw(self):
        self.surface.blit(self.sprite_sheet, (self.x_coordinate, self.y_coordinate))

# player character sprite subclass of class sprite
class player_character_sprite(sprite):
	def __init__(self, img, posn, surface)
		super(player_character_sprite, self).__init__(self, img, posn)
		# player character specific variables
	def update(self):
		# player character specific update logic
		# input
		# gravity
		# velocity
		# momentum
		target_x = self.x_coordinate + 0
		target_y = self.y_coordinate + 0
		super(player_character_sprite, self).update((target_x, target_y))
	def draw(self):
		super(player_character_sprite, self).draw()

# non player character sprite subclass of class sprite
class non_player_character_sprite(sprite):
	def __init__(self, img, posn, surface)
		super(non_player_character_sprite, self).__init__(self, img, posn)
		# non player character specific variables
	def update(self):
		# non player character specific update logic
		# ai
		# gravity
		# velocity
		# momentum
		target_x = self.x_coordinate + 0
		target_y = self.y_coordinate + 0
		super(non_player_character_sprite, self).update((target_x, target_y))
	def draw(self):
		super(non_player_character_sprite, self).draw()
		
# projectile_sprite subcless of class sprite
class projectile_sprite(sprite):
	def __init__(self, img, posn, surface)
		super(projectile_sprite, self).__init__(self, img, posn)
		# projectile specific variables
	def update(self):
		# projectile specific update logic
		target_x = 0
		target_y = 0
		super(projectile_sprite, self).update((target_x, target_y))
	def draw(self):
		super(projectile_sprite, self).draw()
