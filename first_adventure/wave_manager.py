import random
from entity import *
from system_constants import *

class Wave_manager( object ):
    def __init__(self, smart_enemy_selection, dumb_enemy_selection):
        self.smart_enemy_selection = smart_enemy_selection
        self.dumb_enemy_selection = dumb_enemy_selection
    def get_wave_6d(self): # 6 dumb enemies
        # Enemy_entity( position, sprite, smart )
        wave = []
        max_num = 6
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num )
            enemy = Enemy_entity( position, self.dumb_enemy_selection, False )
            wave.append( enemy )
        return wave
    def get_wave_3s(self): # 3 smart enemies
        wave = []
        max_num = 3
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num )
            enemy = Enemy_entity( position, self.smart_enemy_selection, True )
            wave.append( enemy )
        return wave
    def get_wave_3d3s(self): # 3 dumb enemies, 3 smart enemies
        wave = []
        max_num = 6
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num )
            if i % 2 == 0:
                enemy = Enemy_entity( position, self.dumb_enemy_selection, False )
            else:
                enemy = Enemy_entity( position, self.smart_enemy_selection, True )
            wave.append( enemy )
        return wave
    def get_wave_3d(self): # 3 dumb enemies
        wave = []
        max_num = 3
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num )
            enemy = Enemy_entity( position, self.dumb_enemy_selection, False )
            wave.append( enemy )
        return wave
    def get_wave_6s(self): # 6 smart enemies
        # Enemy_entity( position, sprite, smart )
        wave = []
        max_num = 6
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num )
            enemy = Enemy_entity( position, self.smart_enemy_selection, True )
            wave.append( enemy )
        return wave
    def get_wave_9d(self): # 9 dumb enemies
        wave = []
        max_num = 9
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num )
            enemy = Enemy_entity( position, self.dumb_enemy_selection, False )
            wave.append( enemy )
        return wave
    def get_wave_9s(self): # 9 smart enemies
        wave = []
        max_num = 9
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num )
            enemy = Enemy_entity( position, self.smart_enemy_selection, True )
            wave.append( enemy )
        return wave
    def get_wave_5d4s(self): # 5 dumb enemies, 4 smart enemies
        wave = []
        max_num = 9
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num)
            if i % 2 == 0:
                enemy = Enemy_entity( position, self.dumb_enemy_selection, False )
            else:
                enemy = Enemy_entity( position, self.smart_enemy_selection, True )
            wave.append( enemy )
        return wave
    def get_wave_random(self): # 3-6 random enemies
        wave = []
        max_num = random.randint( 3, 6 )
        for i in range(max_num):
            position = ( SCREEN_WIDTH, 0 + ( SCREEN_HEIGHT * i )/ max_num)
            random_int = random.randint( 0, 1 )
            if random_int == 0:
                enemy = Enemy_entity( position, self.smart_enemy_selection, True )
            else:
                enemy = Enemy_entity( position, self.dumb_enemy_selection, False )
            wave.append( enemy )
        return wave
