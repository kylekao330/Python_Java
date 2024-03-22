import pygame

from config import *
class Coin(pygame.sprite.Sprite):
    COIN_SUFFIX = ["1","2","3"]

    def __init__(self,x,y,screen):
        super().__init__()
        self.x = x
        self.y = y
        self.screen = screen

        self.images = []


        for suffix in Coin.COIN_SUFFIX:
            image = pygame.image.load(f"assets/images/coin_{suffix}.png")
            self.images.append(image)

        self.img_index = 0
        self.flip_timer = COIN_FLIP_DELAY
        self.rect = pygame.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())


    def update(self):
        self.x -= TUBE_SPEED
        if TESTING:
             pygame.draw.rect(self.screen, (255, 0, 255), self.rect)
        image = self.next_costume()
        self.rect.y = self.y
        self.rect.x = self.x
        self.screen.blit(image, (self.x, self.y))


    def next_costume(self):
        self.flip_timer -= 1
        if self.flip_timer == 0:
            self.flip_timer = COIN_FLIP_DELAY
            self.img_index += 1
            if self.img_index == len(self.images):
                self.img_index = 0
        return self.images[self.img_index]