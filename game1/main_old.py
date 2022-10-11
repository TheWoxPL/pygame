from ast import Num
from cmath import rect
from mimetypes import init
from tkinter import Scale
from turtle import back, speed, width
from unittest import skip
import pygame
import sys
from settings import *
import math

window = pygame.display.set_mode(SCREENSIZE)


class Beam:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def tick(self, background):
        self.hitbox = pygame.Rect(
            self.x+background.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(window, (128, 128, 128), self.hitbox)


class Physic:
    def __init__(self, x=0, y=0, width=0, height=0, horizontal_acceleration=0.5, max_horizontal_speed=4, gravity=0.5, max_jump_speed=10):
        self.x = x
        self.x_cord=Num
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

    def physic_tick(self, beams, background):
        # print(self.collision_bottom)
        self.previous_x = self.x
        self.x += self.horizontal_speed
        self.gravity_speed += self.gravity
        self.previous_y = self.y
        self.y += self.gravity_speed
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        for beam in beams:

            if beam.hitbox.colliderect(self.hitbox):      
                self.previouspositon(beam.hitbox, background)

        # hitboxowanie postaci
        self.x_cord=self.x-background.x
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def previouspositon(self, beam, background):

        if self.x+self.width+1 >= beam.x+1 > self.previous_x+self.width:  # prawo
            self.x = self.previous_x
            self.horizontal_speed = 0
            print("prawo")
            print(beam.x, self.x+self.width, self.x-background.x+self.width, self.x_cord+self.width)

        elif self.x-1 <= beam.x+beam.width-1 < self.previous_x:  # lewo
            self.x = self.previous_x
            self.horizontal_speed = 0
            print("lewo")
            print(beam.x+beam.width, self.x, self.x-background.x, self.x_cord)

        elif self.previous_y < self.y <= beam.y-1:  # dół
            self.y = self.previous_y
            self.gravity_speed = 0
            self.collision_bottom = True
            # print("dół")

        elif self.y+1 <= beam.y+beam.height:  # gora
            self.y = self.previous_y
            self.gravity_speed = 0
            print("gora")

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        # print("prawo")
        # print(beam.x)
        # print(self.x+self.width)
        # print(beam.x)
        # print(int(self.x+self.width))
        # print(self.width)
        # print(beam.x)

        # self.x=self.previous_x


class Player(Physic):
    def __init__(self):
        self.player_img = pygame.transform.scale(pygame.image.load("img/player/standing/rzufik1.png"), (102, 44))
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
        super().__init__(self.x_first, self.y_first, self.player_img.get_size()[0], self.player_img.get_size()[1], 0.5, MAXHORIZONTALSPEED, 0.5, MAXJUMPSPEED)
        # self.player_physic=Physic(self.x_first, self.y_first, self.player_img.get_size()[0], self.player_img.get_size()[1], 0.5, 0.5, MAXJUMPSPEED)

    def tick(self, beams, background):
        self.physic_tick(beams, background)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.horizontal_speed > (MAXHORIZONTALSPEED)*-1:
            self.horizontal_speed -= self.horizontal_acceleration
        if keys[pygame.K_d] and self.horizontal_speed < MAXHORIZONTALSPEED:
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
            self.player_img = pygame.transform.scale(pygame.image.load(
                f"img/player/standing/rzufik{self.imgnumber}.png"), (102, 44))
            self.imgnumber += 1
            if self.imgnumber == 6:
                self.imgnumber = 1
        self.animationi += 1
        # print(self.y)

        # self.hitbox=pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(window, (128, 18, 128), self.hitbox)
        window.blit(self.player_img, (self.x, self.y))


class Enemy(Physic):
    def __init__(self, player, x, y, src, fps, horizontal_acceleration, max_horizontal_speed):
        self.img = pygame.image.load(("img/enemies/enemy1/img1.png"))
        self.img = pygame.transform.scale(pygame.image.load(src), (40, 46))
        self.fps = fps
        self.player=player
        self.delay_jump_count=0
        super().__init__(x,y,self.img.get_size()[0],self.img.get_size()[1],horizontal_acceleration, max_horizontal_speed, 0.5,10)

    def tick(self,beams,player, background):
        
        self.physic_tick(beams, background)

        # print(math.floor(player.x), math.floor(player.x_cord), math.floor(player.x-background.x))

        if player.x_cord+player.width/2>self.x+self.width/2:
            self.physic_move_right()
        if player.x_cord+player.width/2<self.x+self.width/2:
            self.physic_move_left()
        if player.y+player.height<self.y:
            self.delay_jump_count+=1
            if self.delay_jump_count>60:
                self.physic_jump()
                self.delay_jump_count=0

        # self.collision_with_player()
        
    def collision_with_player(self):
        while False:
            if self.hitbox.colliderect(self.player.hitbox):
                self.previouspositon(self.player.hitbox)

    

    def draw(self, background):
        window.blit(self.img, (self.x+background.x, self.y))


class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.background_img = pygame.image.load(
            "img/background/background1.png")

    def tick(self, player):
        if player.x >= SCREENSIZE[0]/2:
            # player.x = SCREENSIZE[0]/2
            player.x=SCREENSIZE[0]/2
            self.x -= player.horizontal_speed
            # print("kocham  beatke")

        if player.x <= SCREENSIZE[0]/8 and self.x < -5:
            # player.x = SCREENSIZE[0]/8
            player.x=SCREENSIZE[0]/8
            self.x -= player.horizontal_speed
            

        player.hitbox = pygame.Rect(
            player.x, player.y, player.width, player.height)
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
        Beam(1230, 640, 60, 50),
        Beam(1430, 640, 60, 50),
        Beam(1630, 640, 60, 50),
        Beam(1830, 640, 60, 50),
        Beam(650, 415, 500, 50)
    ]

    enemies = [
        # Enemy(player, 0, 500, "img/enemies/enemy1/img1.png", 1, 0.1, 3)
    ]
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
            player.tick(beams, background)
            background.tick(player)
            for beam in beams:
                beam.tick(background)

            # rysowanie nowej klatki
            for beam in beams:
                beam.draw()

            for enemy in enemies:
                enemy.tick(beams, player, background)
                enemy.draw(background)

            player.draw()

            # odświeżanie nowej klatki

            # print(player.collision_bottom)
            pygame.display.update()


if __name__ == "__main__":
    main()
