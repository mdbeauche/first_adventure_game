# SYSTEM
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_CAPTION = 'Bears and Cats... in Space!'
GAME_SPEED = 60 # FPS

# TEXT
ANTI_ALIASING = True
TEXT_TITLE_SIZE = 70
TEXT_SELECTION_SIZE = 90
TEXT_MESSAGE_SIZE = 110
TEXT_INFO_SIZE = 40
TEXT_SCORE_SIZE = 30
GAME_INSTRUCTIONS = 'Instructions: Use arrow keys to move, spacebar to shoot, esc to quit'

# DATA
DATA = 'data'
PLAYER_SPRITE_SHEET = 'SmBearTlBearCatSheet.png'
BEAR_SPRITE = 'bearImg.png'
CAT_SPRITE = 'catImg.png'
WINDOW_ICON = 'catImg.png'
BG_MUSIC = 'song.ogg'
PROJECTILE_SOUND_FILE = 'fire.wav'
NPC_HIT_SOUND_FILE = 'death.wav'
PLAYER_HIT_SOUND_FILE = 'killed.wav'
HIGH_SCORE = 'high_score.txt'

# COLORS           R    G    B
COLOR_BLACK    = (  0,   0,   0)
COLOR_WHITE    = (255, 255, 255)
COLOR_RED      = (255,   0,   0)
COLOR_GREEN    = (  0, 255,   0)
COLOR_BLUE     = (  0,   0, 255)

# DIRECTIONS
RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'
SHOOT = 'shoot'

# PLAYER
PLAYER_MOVE_SPEED = 10
PLAYER_HEALTH = 5
PLAYER_INVULNERABLE_TIME = 0.85 # in seconds
INVULNERABLE_ANIMATION_TIME = 0.15 # in seconds
CAT = 'cat'
BEAR = 'bear'
PLAYER_HITBOX_BUFFER = 20
SHOOT_RELOAD_TIME = 0.20
PROJECTILE_SPEED = 14
PROJECTILE_SIZE = 8
PROJECTILE_NUMBER = 7

# NPC
DUMB_NPC_MOVE_SPEED = 8
SMART_NPC_MOVE_SPEED_X = 8
SMART_NPC_MOVE_SPEED_Y = 3
BOSS_HEALTH = 60
BOSS_MOVE_SPEED = 7
BOSS_SPACE_BUFFER = 50

# WAVES
WAVE_1_TIME = 3.25
WAVE_2_TIME = 2
WAVE_3_TIME = 0.85
WAVE_4_TIME = 0.7
WAVE_4_LENGTH = 12

# GAME
GAME_LOSE = 'lose'
GAME_WIN = 'win'
