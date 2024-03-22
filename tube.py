import pygame
from config import *

class Tube(pygame.sprite.Sprite):
    def __init__(self,x,y, type, screen):
        super().__init__()
        self.x = x
        self.y = y
        self.screen = screen
        self.image = pygame.image.load("assets/images/Downward_Tube_2.png")
        if type == UPWARD:
            self.image = pygame.transform.flip(self.image, False, True)

        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def get_img_height(self):
        return self.image.get_height()

    def update(self):
        if TESTING:
            pygame.draw.rect(self.screen, (255, 0, 255), self.rect)
        self.rect.y = self.y
        self.rect.x = self.x
        self.x -= TUBE_SPEED
        self.screen.blit(self.image, (self.x, self.y))
