import pygame
import random as r
from config import *
class Cloud(pygame.sprite.Sprite):

    # BIRD_TYPES is static variable, there is only one instance of this in your program
    CLOUD_TYPES = ["1", "2", "3"]
    def __init__(self,x,y,direction, screen):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.screen = screen
        cloud_type = r.choice(Cloud.CLOUD_TYPES)
        self.image = pygame.image.load(f"assets/cloud{cloud_type}.png")
        self.speed = r.randint(1,6)


    def update(self):
        if self.direction == RIGHT:
            self.x += self.speed
        else:
            self.x -= self.speed
        self.screen.blit(self.image, (self.x, self.y))
        if self.x < -350 or self.x > WIDTH:
            self.kill()
        #self.x += self.speed
        #self.screen.blit(self.image, (self.x,self.y)