import pygame
import random as r
from config import *

class Bird(pygame.sprite.Sprite):

    # BIRD_TYPES is static variable, there is only one instance of this in your program
    BIRD_TYPES = ["01", "02", "03","04"]
    BIRD_SUFFIX = ["A", "B"]
    def __init__(self,x,y,size, direction, screen):
        super().__init__()

        self.x = x
        self.y = y
        self.direction = direction
        self.size = size
        self.screen = screen
        bird_type = r.choice(Bird.BIRD_TYPES)
        self.images = []

        for suffix in Bird.BIRD_SUFFIX:
            image = pygame.image.load(f"assets/bird{bird_type}_{suffix}.png")
            image = pygame.transform.scale(image, (int(1.3*self.size),self.size))
            if self.direction == LEFT:
                image = pygame.transform.flip(image, True, False)
            self.images.append(image)

        self.speed = r.randint(1,6)

        self.img_index = 0
        self.bird_flap_timer = CREATE_FLAP_DELAY
        #below is the bird hitbox
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(),self.images[0].get_height())

    def update(self):
        if self.direction == RIGHT:
            self.x += self.speed
        else:
            self.x -= self.speed
        self.rect.x = self.x
        image = self.next_costume()
        if TESTING:
            pygame.draw.rect(self.screen, (255, 0, 255), self.rect)
        self.screen.blit(image, (self.x,self.y))

        if self.x < 0 or self.x > WIDTH:
            self.kill()

    def next_costume(self):
        self.bird_flap_timer -= 1
        if self.bird_flap_timer == 0:
            self.bird_flap_timer = CREATE_FLAP_DELAY
            self.img_index += 1
            if self.img_index == len(self.images):
                self.img_index = 0
        image = self.images[self.img_index]
        return image