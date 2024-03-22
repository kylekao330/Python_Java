import pygame
from config import *
import player
class Fireball (pygame.sprite.Sprite):
    def __init__(self,x,y,size, direction,screen):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction
        self.screen = screen
        self.speed = 7

        self.right_images = []
        self.left_images = []

        self.image = pygame.image.load(f"assets/bullet.png")
        self.image = pygame.transform.scale(self.image, (int(1.8*self.size), self.size))

        if self.direction == LEFT:
           self.image = pygame.transform.flip(self.image, True, False)
        #below is the fireball hitbox
        self.rect = pygame.Rect(self.x,self.y,self.image.get_width(),self.image.get_height())




    def update(self):
        if self.direction == RIGHT:
            self.x += self.speed
        if self.direction == LEFT:
            self.x -= self.speed
        if self.x < -100 or self.x > WIDTH:
            self.kill()
        if TESTING:
            pygame.draw.rect(self.screen, (255, 0, 255), self.rect)
        self.rect.x = self.x
        self.rect.y = self.y

        self.screen.blit(self.image, (self.x, self.y))