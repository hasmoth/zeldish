from __future__ import annotations
import pygame
from debug import debug
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_weapon,create_magic):
        super(Player,self).__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

        # graphics setup
        self.import_player_assets()
        self.status = Status('down')

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.attack_type = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_weapon
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.weapon_switch_cooldown = 400

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        #self.destroy_magic = destroy_magic
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.magic_cost = magic_data[self.magic]['cost']
        self.magic_switch_cooldown = 400

        #stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_costs = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 500
        self.speed = self.stats['speed']

        # invincibility timer
        self.invincibility_duration = 500

        # sound
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up':[],'down':[],'left':[],'right':[],
                           'up_idle':[],'down_idle':[],'left_idle':[],'right_idle':[],
                           'up_attack':[],'down_attack':[],'left_attack':[],'right_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status.set('up')
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status.set('down')
            else:
                self.direction.y = 0
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status.set('left')
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status.set('right')
            else:
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.attack_type = 'weapon'
                self.create_attack()
                self.weapon_attack_sound.play()

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.attack_type = 'magic'
                strength = magic_data[self.magic]['strength'] + self.stats['magic']
                cost = magic_data[self.magic]['cost']
                self.create_magic(self.magic,strength,cost)

            # switch weapon
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # switch magic
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]
                self.magic_cost = magic_data[self.magic]['cost']

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            self.status.make_idle()

        # attack
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            self.status.make_attack()
        else:
            if self.status.is_attack():
                self.status.make_idle()

    def move(self,speed):
        if self.direction.magnitude() > 1:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction ==  'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        now = pygame.time.get_ticks()

        if self.attacking:
            #this means the player is attacking for the duration of the cooldown!!!
            if self.attack_type == 'weapon':
                cooldown = weapon_data[self.weapon]['cooldown'] + self.attack_cooldown
            elif self.attack_type == 'magic':
                cooldown = self.attack_cooldown
            else:
                cooldown = 0

            if now - self.attack_time >= cooldown:
                self.attacking = False
                self.destroy_attack()
                self.attack_type = None

        if not self.can_switch_weapon:
            if now - self.weapon_switch_time >= self.weapon_switch_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if now - self.magic_switch_time >= self.magic_switch_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if now - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_weapon_damage(self):
        return self.stats['attack'] + weapon_data[self.weapon]['damage']

    def get_magic_damage(self):
        return self.stats['magic'] + magic_data[self.magic]['strength']

    def energy_recovery(self):
        if self.energy <= self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def animate(self):
        animation = self.animations[self.status.get()]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha) # TODO not working with by-pixel alpha img
        else:
            self.image.set_alpha(255)


    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()