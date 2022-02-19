import imp


import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super(Weapon,self).__init__(groups)
        direction = player.status.get().split('_')[0]
        self.weapon_offset_vert = pygame.math.Vector2(0,16)
        self.weapon_offset_up = pygame.math.Vector2(-10,0)
        self.weapon_offset_down = pygame.math.Vector2(10,0)

        # graphic
        full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        self.sprite_type = 'weapon'

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + self.weapon_offset_vert)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + self.weapon_offset_vert)
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + self.weapon_offset_up)
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + self.weapon_offset_down)