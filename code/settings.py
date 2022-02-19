# game setup
from distutils.log import error


WIDTH = 1280
HEIGHT = 720
FPS    = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30,'graphic':'../graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
    'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'},
}
# magic
magic_data = {
    'flame': {'strength': 5,'cost': 20,'graphic':'../graphics/particles/flame/fire.png'},
    'heal' : {'strength': 20,'cost': 10,'graphic':'../graphics/particles/heal/heal.png'}
}

# enemy
monster_data = {
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}
}

# status
status_list = ['up','down','left','right',
          'up_idle','down_idle','left_idle','right_idle',
          'up_attack','down_attack','left_attack','right_attack'
         ]

class Status:
    def __init__(self,status):
        self.status_list = status_list
        self.status = status if status in self.status_list else error("status not defined")

    def set(self,status):
        self.status = status if status in self.status_list else error("status not defined")

    def get(self):
        return self.status

    def is_attack(self):
        return 'attack' in self.status

    def is_idle(self):
        return 'idle' in self.status

    def make_idle(self):
        if('up' in self.status):
            self.status = 'up_idle'
        elif('down' in self.status):
            self.status = 'down_idle'
        elif('left' in self.status):
            self.status = 'left_idle'
        elif('right' in self.status):
            self.status = 'right_idle'
        else:
            pass

    def make_attack(self):
        if('up' in self.status):
            self.status = 'up_attack'
        elif('down' in self.status):
            self.status = 'down_attack'
        elif('left' in self.status):
            self.status = 'left_attack'
        elif('right' in self.status):
            self.status = 'right_attack'
        else:
            pass
