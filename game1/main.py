from ast import Num
from cgi import test
from cmath import rect
from mimetypes import init
from tkinter import Scale
from turtle import back, register_shape, speed, width
from unittest import skip
import pygame
import sys
from settings import *
import math

window = pygame.display.set_mode(SCREENSIZE)

class Bullet:
    def __init__(self, x, y, bullet_size, bullet_speed, direction, entity_type, bullet_damage):
        self.bullet_x=x
        self.bullet_y=y
        self.bullet_size=bullet_size
        self.bullet_speed=bullet_speed
        self.bullet_left_direction=direction
        if self.bullet_left_direction:
            self.bullet_speed*=-1
            self.bullet_x-=65

        self.entity_type=entity_type
        self.bullet_damage=bullet_damage
        self.bullet_img=pygame.image.load("img/player/weapon/bullets/bullet.png")
        self.bullet_img=pygame.transform.scale(self.bullet_img, (self.bullet_img.get_size()[0]*self.bullet_size, self.bullet_img.get_size()[1]*self.bullet_size))
    
        self.bullet_width=self.bullet_img.get_size()[0]
        self.bullet_height=self.bullet_img.get_size()[1]
        self.bullet_hitbox=pygame.Rect(self.bullet_x+1,self.bullet_y,self.bullet_width,self.bullet_height)
    def tick(self, beams, player, bullets, enemies):
        self.bullet_hitbox=pygame.Rect(self.bullet_x+1,self.bullet_y,self.bullet_width,self.bullet_height)
        self.bullet_x+=self.bullet_speed
        for beam in beams:
            if self.bullet_hitbox.colliderect(beam.hitbox):
                bullets.remove(self)
                continue
        if self.entity_type=="Player":
            for enemy in enemies:
                if self.bullet_hitbox.colliderect(enemy.hitbox):
                    enemy.health_get_damage(self.bullet_damage, enemies)
                    bullets.remove(self)
                    continue
        if self.entity_type=="Enemy":
            if self.bullet_hitbox.colliderect(player.hitbox):
                player.health_get_damage(self.bullet_damage)
                bullets.remove(self)
                             

    def draw(self, background):
        # pygame.draw.rect(window, (12,122,12), self.bullet_hitbox)
        window.blit(self.bullet_img, (self.bullet_x+background.x, self.bullet_y))
    
class Weapon:
    
    def __init__(self, name, damage, shooting_speed, bullet_size, bullet_speed, reload_time, magazin_capacity, bullet_time_life):
        self.weapon_name=name
        self.weapon_damage=damage
        self.weapon_shooting_speed=shooting_speed
        self.weapon_bullet_size=bullet_size
        self.weapon_bullet_speed=bullet_speed
        self.weapon_reload_time=reload_time
        self.weapon_magazin_capacity=magazin_capacity
        self.weapon_bullet_time_life=bullet_time_life
        self.weapon_img=None
        self.weapon_shooting_speed_counter=self.weapon_shooting_speed

    def weapon_tick(self, bullets):
        self.weapon_img=pygame.transform.scale(pygame.image.load("img/player/weapon/basic/pulled_out/weapon1.png"),(102,44))
        if self.weapon_shooting_speed_counter<TPS/self.weapon_shooting_speed:
            self.weapon_shooting_speed_counter+=1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and TPS/self.weapon_shooting_speed==self.weapon_shooting_speed_counter:
            self.weapon_shooting_speed_counter=0
            bullets.append(Bullet(self.x+self.width*0.7, (self.y+self.height/4), self.weapon_bullet_size, self.weapon_bullet_speed, self.left_direction, self.entity_type, self.weapon_damage))          
        

class Health:
    def __init__(self, hp=100, reg_hp=0, reg_tps=0, hp_max=100):
        self.hp=hp
        self.reg_hp=reg_hp
        self.reg_tps=reg_tps
        self.hp_max=hp_max
        self.reg_tps_counter=0

    def health_tick(self, enemies):
        self.reg_tps_counter+=1
        if self.hp<self.hp_max and self.reg_tps!=0:
            if self.reg_tps_counter==self.reg_tps:
                self.reg_tps_counter=0
                self.hp+=self.reg_hp
        
        if self.hp<=0 and self.entity_type=="Player":
            print("koniec gry")
        if self.hp<=0 and self.entity_type=="Enemy":
            enemies.remove(self)

    def health_get_damage(self, damage, enemies):
        self.hp-=damage
        if self.hp<=0 and self.entity_type=="Player":
            print("koniec gry")
        if self.hp<=0 and self.entity_type=="Enemy":
            enemies.remove(self)

    def health_draw(self, background):
        x=self.x+background.x
        width=self.width*self.hp/self.hp_max
        height=20
        y=self.y-height-5
        life_bar=(x,y,width,height)
        pygame.draw.rect(window, (255, 1, 1), life_bar)
        font = pygame.font.SysFont('Calibri', height-2)
        textsurface = font.render(f"{self.hp}/{self.hp_max}", False, (200, 200, 200))
        window.blit(textsurface,(x+2,y+1,width,height))

class Beam:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def tick(self, background):
        self.hitbox = pygame.Rect(
            self.x, self.y, self.width, self.height)

    def draw(self,background):
        
        pygame.draw.rect(window, (128, 128, 128), (self.x+background.x, self.y, self.width, self.height))


class Physic:
    def __init__(self, x=0, y=0, width=0, height=0, horizontal_acceleration=0.5, max_horizontal_speed=4, gravity=0.5, max_jump_speed=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.horizontal_acceleration = horizontal_acceleration
        self.max_horizontal_speed=max_horizontal_speed
        self.horizontal_speed = 0
        self.gravity = gravity
        self.gravity_speed = 0
        self.max_jump_speed = max_jump_speed
        self.jump_speed = 0
        self.previous_x = Num
        self.previous_y = Num
        self.w_pressed = False
        self.collision_right=False
        self.collision_left=False
        self.collision_bottom = False
        self.moving=False
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def physic_move_left(self):
        if self.horizontal_speed > (self.max_horizontal_speed)*-1:
            self.horizontal_speed -= self.horizontal_acceleration
            self.moving=True

    def physic_move_right(self):
        if self.horizontal_speed < self.max_horizontal_speed:
            self.horizontal_speed += self.horizontal_acceleration
            self.moving=True

    def physic_jump(self):
        if self.collision_bottom == True:
            self.collision_bottom = False
            self.gravity_speed = -MAXJUMPSPEED
    
    def physic_not_moving(self):
        # if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if self.horizontal_speed > 0:
                self.horizontal_speed -= self.horizontal_acceleration
            if self.horizontal_speed < 0:
                self.horizontal_speed += self.horizontal_acceleration
            if math.fabs(self.horizontal_speed)<0.2:
                    self.horizontal_speed=0
            

    def physic_tick(self, beams, background):
        # print(self.collision_bottom)
        self.previous_x = self.x
        self.x += self.horizontal_speed
        self.gravity_speed += self.gravity
        self.previous_y = self.y
        self.y += self.gravity_speed
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        self.collision_left=False
        self.collision_right=False
        for beam in beams:

            if beam.hitbox.colliderect(self.hitbox):      
                self.previouspositon(beam, background)

        # hitboxowanie postaci
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def previouspositon(self, beam, background):

        # if self.x+self.width>=beam.x+1>self.previous_x+self.width:
        #     self.collision_right=True
        #     self.x=self.previous_x
        #     self.horizontal_speed=0
        # if self.x<=beam.x+beam.width-1<self.previous_x:
        #     self.collision_left=True
        #     self.x=self.previous_x
        #     self.horizontal_speed=0
        # if self.y+self.height>=beam.y+1>self.previous_y+self.height:
        #     self.collision_bottom=True
        #     self.y=self.previous_y
        #     self.gravity_speed=0
        # if self.y<=beam.y+beam.height-1<self.previous_y:
        #     self.y=self.previous_y
        #     self.gravity_speed=0
        
        # print(self.x)
        if not (self.previous_y < self.y <= beam.y-1):
            # print(self.x, beam.x+beam.width)
            pass

        if self.x+self.width+1 >= beam.x+1 > self.previous_x+self.width:  # prawo
            # print(beam.x, self.x+self.width, self.x-background.x+self.width, self.x+self.width)
            self.x = self.previous_x
            # self.x = self.previous_x
            self.horizontal_speed = 0
            self.collision_right=True
            # print("prawo")

        elif self.x-1 <= beam.x+beam.width-1 < self.previous_x:  # lewo
            # print(beam.x+beam.width, self.x, self.x-background.x, self.x)
            self.x = self.previous_x
            # self.x = self.previous_x
            self.horizontal_speed = 0
            self.collision_left=True
            # print("lewo")

        elif self.y<= beam.y+beam.height<self.previous_y:  # gora
            self.y = self.previous_y
            self.gravity_speed = 0
            # print("gora")

        elif self.previous_y < beam.y <=self.y+self.height :  # dół
            self.y = self.previous_y
            self.gravity_speed = 0
            self.collision_bottom = True
            # print("dół")

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        # print("prawo")
        # print(beam.x)
        # print(self.x+self.width)
        # print(beam.x)
        # print(int(self.x+self.width))
        # print(self.width)
        # print(beam.x)

        # self.x=self.previous_x


class Player(Physic, Health, Weapon):
    def __init__(self):
        self.player_img = [pygame.transform.scale(pygame.image.load("img/player/standing/rzufik1.png"), (102, 44))]
        self.x_first = 0
        # self.previous_x=Num
        self.y_first = 0
        # self.previous_y=Num
        # self.width = self.player_img.get_size()[0]
        # self.height = self.player_img.get_size()[1]
        self.animationi = 0
        self.imgnumber = 1
        # self.horizontal_speed = 0
        # self.horizontal_acceleration = 0.5
        # self.gravity_speed = 0
        # self.gravity = 0.5
        # self.w_pressed=False
        # self.jump_speed=0
        # self.collision_bottom=False
        # self.hitbox=pygame.Rect(self.x, self.y, self.width, self.height)
        self.left_direction=False
        self.right_direction=True
        self.entity_type="Player"
        Health.__init__(self, 20, 1, 60, 100)
        Physic.__init__(self,self.x_first, self.y_first, self.player_img[0].get_size()[0], self.player_img[0].get_size()[1], 0.5, MAXHORIZONTALSPEED, 0.5, MAXJUMPSPEED)
        Weapon.__init__(self, "basic", 10, 5, 2, 10, 5, 32, 5)
        
        # self.player_physic=Physic(self.x_first, self.y_first, self.player_img.get_size()[0], self.player_img.get_size()[1], 0.5, 0.5, MAXJUMPSPEED)

    def tick(self, beams, background, bullets, enemies):
        self.physic_tick(beams, background)
        self.health_tick(enemies)
        self.weapon_tick(bullets)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.horizontal_speed > (MAXHORIZONTALSPEED)*-1:
            self.left_direction=True
            self.right_direction=False
            self.horizontal_speed -= self.horizontal_acceleration
        if keys[pygame.K_d] and self.horizontal_speed < MAXHORIZONTALSPEED:
            self.right_direction=True
            self.left_direction=False
            self.horizontal_speed += self.horizontal_acceleration
        if keys[pygame.K_w] and self.collision_bottom == True:
            self.collision_bottom = False
            self.gravity_speed = -MAXJUMPSPEED
        if keys[pygame.K_s]:
            pass
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if self.horizontal_speed > 0:
                self.horizontal_speed -= self.horizontal_acceleration
            if self.horizontal_speed < 0:
                self.horizontal_speed += self.horizontal_acceleration

        # print(self.collision_bottom)

        # animation

        if self.animationi == 8:
            self.animationi -= 8
            self.player_img[0] = pygame.transform.scale(pygame.image.load(
                f"img/player/standing/rzufik{self.imgnumber}.png"), (102, 44))
            self.imgnumber += 1
            if self.imgnumber == 6:
                self.imgnumber = 1
        self.animationi += 1
        # print(self.y)

        #adding other images to player like weapon etc
        

    def draw(self, background):
        # self.hitbox[0]=self.x+background.x
        # pygame.draw.rect(window, (128, 18, 128), (self.x+background.x, self.y, self.width, self.height))
        self.player_img.append(self.weapon_img)

        for img in self.player_img:
            if self.left_direction:
                img=pygame.transform.flip(img,True, False)
            window.blit(img, (self.x+background.x, self.y))
        self.health_draw(background)
        self.player_img=[self.player_img[0]]
        
        


class Enemy(Physic, Health):
    def __init__(self, player, x, y, src, fps, horizontal_acceleration, max_horizontal_speed, damage, damage_delay, range_detection):
        self.img = pygame.image.load(("img/enemies/enemy1/img1.png"))
        self.img = pygame.transform.scale(pygame.image.load(src), (40, 46))
        self.fps = fps
        self.player=player
        self.delay_jump_count=0
        self.damage_hp=damage
        self.damage_delay=damage_delay
        self.damage_counter=self.damage_delay
        self.range_detection=range_detection
        self.entity_type="Enemy"
        Physic.__init__(self,x,y,self.img.get_size()[0],self.img.get_size()[1],horizontal_acceleration, max_horizontal_speed, 0.5,10)
        Health.__init__(self, 30, 5, 120, 60)

    def tick(self,beams,player, background, enemies):
        
        
        self.physic_tick(beams, background)
        self.health_tick(enemies)

        # print(math.floor(player.x), math.floor(player.x), math.floor(player.x-background.x))

        # if self.x==self.previous_x and (self.x+self.width<player.x or self.x>player.x+player.width):
        #     self.physic_jump()
        dist = pygame.math.Vector2(player.x, player.y).distance_to((self.x, self.y))
        if dist<=self.range_detection:
            if player.x-1>self.x:
                self.physic_move_right()
                if self.collision_right:
                    self.physic_jump()
                    # print("prawo")
            elif player.x+player.width+1<self.x+self.width:
                self.physic_move_left()
                if self.collision_left:
                    self.physic_jump()
                    # print("lewo")
            else:
                self.physic_not_moving()

            if player.y+player.height<self.y:
                self.delay_jump_count+=1
                if self.delay_jump_count>60:
                    self.physic_jump()
                    self.delay_jump_count=0

            self.damage_with_player(player)
        else:
            self.physic_not_moving()


    
    def damage_with_player(self, player):
        if self.damage_counter<self.damage_delay:
            self.damage_counter+=1
        if self.damage_counter==self.damage_delay:
            if player.hitbox.colliderect(self.hitbox):
                player.hp-=self.damage_hp
                self.damage_counter=0

    

    def draw(self, background):
        window.blit(self.img, (self.x+background.x, self.y))
        self.health_draw(background)


class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.background_img = pygame.image.load(
            "img/background/background1.png")

    def tick(self, player):
        # if player.x > SCREENSIZE[0]/2:
        #     # player.x = SCREENSIZE[0]/2
        #     player.x=SCREENSIZE[0]/2
        #     self.x -= player.horizontal_speed
        #     # print("kocham  beatke")

        # if player.x < SCREENSIZE[0]/8 and self.x < -5:
        #     # player.x = SCREENSIZE[0]/8
        #     player.x=SCREENSIZE[0]/8
        #     self.x -= player.horizontal_speed
            

        # player.hitbox = pygame.Rect(
        #     player.x, player.y, player.width, player.height)
        # window.blit(self.background_img, (self.x, self.y))
        if player.x > SCREENSIZE[0]/2 and player.x!=player.previous_x:
            self.x -= player.horizontal_speed
            # print(self.x)
        
            # player.x-=self.x

        # if player.x < SCREENSIZE[0]/8:
        #     self.x -= player.horizontal_speed
            # player.x-=self.x

        # player.hitbox = pygame.Rect(
        #     player.x-self.x, player.y, player.width, player.height)
        window.blit(self.background_img, (self.x, self.y))
            
def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    player = Player()
    background = Background()
    
    beams = [
        Beam(0, window.get_size()[1]-20, 12280, 20),
        Beam(200, 605, 60, 50),
        Beam(425, 510, 60, 50),
        Beam(430, 620, 60, 50),
        Beam(530, 620, 60, 50),
        Beam(730, 620, 60, 50),
        Beam(830, 620, 60, 50),
        Beam(930, 620, 60, 50),
        Beam(1231.5, 640, 60, 50),
        Beam(1431.5, 640, 60, 50),
        Beam(1631.5, 640, 60, 50),
        Beam(1831.5, 640, 60, 50),
        Beam(1941.5, 640, 90, 50),
        Beam(2051.5, 640, 90, 50),
        Beam(2161.5, 640, 90, 50),
        Beam(2271.5, 640, 90, 50),
        Beam(2381.5, 640, 90, 50),
        Beam(2431, 640, 90, 50),
        Beam(650, 415, 500, 50)
    ]

    enemies = [
        Enemy(player, 0, 500, "img/enemies/enemy1/img1.png", 1, 0.1, 3, 10, 120, 400)
    ]
    bullets=[]
    i=0
    j=0
    while True:

        # obsługa eventów, klawiszy itp
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

        dt += clock.tick()
        
        if dt >= 1000 / TPS:
            dt -= 1000 / TPS
            i+=1
            if(i==15):
                i=0
                print(j)
                j+=1
            # ticking


            player.tick(beams, background, bullets, enemies)
            # print(player.x, beams[11].x)
            background.tick(player)

            for beam in beams:
                beam.tick(background)

            for bullet in bullets:
                bullet.tick(beams, player, bullets, enemies)

            # rysowanie nowej klatki
            for beam in beams:
                beam.draw(background)

            for enemy in enemies:
                enemy.tick(beams, player, background, enemies)
                enemy.draw(background)

            player.draw(background)

            for bullet in bullets:
                bullet.draw(background)


            # odświeżanie nowej klatki

            # print(player.collision_bottom)
            pygame.display.update()


if __name__ == "__main__":
    main()
