import pygame
import random as r
from config import *

class Player(pygame.sprite.Sprite):

    # BIRD_TYPES is static variable, there is only one instance of this in your program
    BIRD_SUFFIX = ["1","2","3","4"]

    def __init__(self,x,y,size, direction, screen):
        super().__init__()

        self.x = x
        self.y = y
        self.direction = direction
        self.size = size
        self.screen = screen
        self.right_images = []
        self.left_images = []

        for suffix in Player.BIRD_SUFFIX:
            image = pygame.image.load(f"assets/player-{suffix}.png")
            image = pygame.transform.scale(image, (int(1.3*self.size),self.size))
            self.right_images.append(image)

            image = pygame.transform.flip(image,True, False)
            self.left_images.append(image)

        self.speed = 6
        self.img_index = 0
        self.bird_flap_timer = CREATE_FLAP_DELAY
        self.rect = pygame.Rect(self.x, self.y, self.right_images[0].get_width(), self.right_images[0].get_height())

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if TESTING:
             pygame.draw.rect(self.screen, (255, 0, 255), self.rect)
        if keys_pressed[pygame.K_w]:
            self.y -= self.speed

        if keys_pressed[pygame.K_s]:
            self.y += self.speed

        if keys_pressed[pygame.K_d]:
            self.direction = RIGHT
            self.x += self.speed

        if keys_pressed[pygame.K_a]:
            self.direction = LEFT
            self.x -= self.speed
        self.rect.y = self.y
        self.rect.x = self.x
        image = self.next_costume()
        self.screen.blit(image, (self.x, self.y))

    def set_location(self,x,y):
        self.x = x
        self.y = y

    def next_costume(self):
        self.bird_flap_timer -= 1
        if self.bird_flap_timer == 0:
            self.bird_flap_timer = CREATE_FLAP_DELAY
            self.img_index += 1
            if self.img_index == len(self.right_images):
                self.img_index = 0
        if self.direction == LEFT:
                return self.left_images[self.img_index]
        else:
                return self.right_images[self.img_index]