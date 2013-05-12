from entity import *
from system_constants import *

class Wave_manager( object ):
    def __init__(self, smart_enemy_selection, dumb_enemy_selection):
        self.smart_enemy_selection = smart_enemy_selection
        self.dumb_enemy_selection = dumb_enemy_selection
    def get_wave_1(self):
        # Enemy_entity( position, sprite, smart )
        position_1 = ( SCREEN_WIDTH, SCREEN_HEIGHT / 6)
        position_2 = ( SCREEN_WIDTH, (SCREEN_HEIGHT * 2)/ 6)
        position_3 = ( SCREEN_WIDTH, (SCREEN_HEIGHT * 3)/ 6)
        position_4 = ( SCREEN_WIDTH, (SCREEN_HEIGHT * 4)/ 6)
        position_5 = ( SCREEN_WIDTH, (SCREEN_HEIGHT * 5)/ 6)
        
        enemy_1 = Enemy_entity( position_1, self.dumb_enemy_selection, False )
        enemy_2 = Enemy_entity( position_2, self.dumb_enemy_selection, False )
        enemy_3 = Enemy_entity( position_3, self.dumb_enemy_selection, False )
        enemy_4 = Enemy_entity( position_4, self.dumb_enemy_selection, False )
        enemy_5 = Enemy_entity( position_5, self.dumb_enemy_selection, False )
        wave_1 = [ enemy_1, enemy_2, enemy_3, enemy_4, enemy_5 ]
        return wave_1
    def get_wave_2(self):
        wave_2 = []
        return wave_2
    def get_wave_3(self):
        wave_3 = []
        return wave_3
