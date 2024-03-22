import pygame

from config import *
class Player(pygame.sprite.Sprite):
    BIRD_SUFFIX = ["1","2"]

    def __init__(self,x,y,size,screen):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.screen = screen

        self.flying_images = []


        for suffix in Player.BIRD_SUFFIX:
            image = pygame.image.load(f"assets/images/Green duck #{suffix}-01.png")
            image = pygame.transform.scale(image, (int(1.3*self.size),self.size))
            self.flying_images.append(image)

        self.img_index = 0
        self.bird_flap_timer = CREATE_FLAP_DELAY
        self.rect = pygame.Rect(self.x, self.y, self.flying_images[0].get_width(), self.flying_images[0].get_height())
        self.fall_speed = 1
        self.gravity = 1

        self.mode = FLYING_MODE
        self.dizzy_image = pygame.image.load("assets/images/Green duck #5-01.png")
        self.dizzy_image = pygame.transform.scale(self.dizzy_image, (self.size, self.size))

    def start_dizzy_mode(self):
        self.mode = DIZZY_MODE

    def start_flying_mode(self):
        self.mode = FLYING_MODE

    def update(self):
        self.fall_speed += self.gravity
        self.y += self.fall_speed
        keys_pressed = pygame.key.get_pressed()

        if self.mode == FLYING_MODE:
            if keys_pressed[pygame.K_SPACE]:
                self.fall_speed = -JUMP_HEIGHT
        if TESTING:
             pygame.draw.rect(self.screen, (255, 0, 255), self.rect)
        image = self.next_costume()
        self.rect.y = self.y
        self.rect.x = self.x
        self.screen.blit(image, (self.x, self.y))

    def set_location(self,x,y):
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.fall_speed = 0
        self.mode = FLYING_MODE

    def next_costume(self):
        if self.mode  == FLYING_MODE:
            self.bird_flap_timer -= 1
            if self.bird_flap_timer == 0:
                self.bird_flap_timer = CREATE_FLAP_DELAY
                self.img_index += 1
                if self.img_index == len(self.flying_images):
                    self.img_index = 0
            return self.flying_images[self.img_index]
        else:
            return self.dizzy_image