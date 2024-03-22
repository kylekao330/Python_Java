import pygame
import random as r
from bird import Bird
from cloud import Cloud
from player import Player
from config import *
from fireball import Fireball

class Birdie():

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.project_name = "Birdie"

        pygame.display.set_caption(self.project_name)

        # Loop until the user clicks the close button.
        self.running = True

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        # Below is how you load an image from your computer to the memory
        self.background = pygame.image.load("assets/scene.png")
        self.title = pygame.image.load("assets/birdie_title.png")
        self.play_button = pygame.image.load("assets/play_button.png")

        self.bird_group = pygame.sprite.Group()
        bird = Bird(200,100,50,RIGHT,self.screen)
        self.bird_group.add(bird)
        self.bird_create_timer = CREATE_BIRD_DELAY


        self.cloud_group = pygame.sprite.Group()
        cloud = Cloud(200, 100, RIGHT, self.screen)
        self.cloud_group.add(cloud)

        self.cloud_create_timer = CREATE_CLOUD_DELAY

        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player(PLAYER_SPAWN_X,PLAYER_SPAWN_Y,50,RIGHT,self.screen)

        self.fireball_group = pygame.sprite.Group()

        self.launch_giant_fb_timer = LAUNCH_GIANT_FIREBALL_COOLDOWN
        self.giant_fireball_group = pygame.sprite.Group()

        self.launch_fb_timer = LAUNCH_FIREBALL_COOLDOWN
        self.score = 0
        self.score_font = pygame.font.SysFont("Arial", 30)
        self.game_mode = GAME_LANDING_PAGE

        # background music
        pygame.mixer.music.load("assets/background.mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        # sound effect
        self.pop_sfx = pygame.mixer.Sound("assets/plop.wav")
        self.pop_sfx.set_volume(1)

    def draw_score(self):
        score_text = self.score_font.render(f"Score {self.score}", 1, BLACK)
        self.screen.blit(score_text, (30,30))

    def draw_giant_fireball_cooldown_indicator(self):
        color = BLACK
        if self.launch_giant_fb_timer <= 0 :
            text = "Giant Fireball Ready"
            color = (r.randint(0,255), r.randint(0,255), r.randint(0,255))
        else:
            text = f"Giant Fireball Cooldown {self.launch_giant_fb_timer}"
        text_image = self.score_font.render(text, 1, color)
        self.screen.blit(text_image, (WIDTH-400,30))
    def launch_fireball(self):
        self.launch_fb_timer -= 1

        if self.launch_fb_timer <= 0:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                self.launch_fb_timer = LAUNCH_FIREBALL_COOLDOWN
                fireball = Fireball(self.player.x, self.player.y, 50, self.player.direction,  self.screen)
                self.fireball_group.add(fireball)

    def launch_giant_fireball(self):
        self.launch_giant_fb_timer -= 1
        if self.launch_giant_fb_timer <= 0:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_b]:
                self.launch_giant_fb_timer = LAUNCH_GIANT_FIREBALL_COOLDOWN
                if self.player.direction == RIGHT:
                    fireball = Fireball(self.player.x + 65, self.player.y - 50, 150, self.player.direction, self.screen)
                else:
                    fireball = Fireball(self.player.x - 270, self.player.y - 50, 150, self.player.direction, self.screen)
                self.giant_fireball_group.add(fireball)

    def create_bird(self):

        self.bird_create_timer -= 1
        if self.bird_create_timer == 0:
            self.bird_create_timer = CREATE_BIRD_DELAY

            y = r.randint(0, 500)
            direction = r.choice(DIRECTIONS)
            x = 0
            if direction == LEFT:
                x = WIDTH
            bird = Bird(x, y, 50,direction, self.screen)
            self.bird_group.add(bird)


    def create_cloud(self):
        self.cloud_create_timer -= 1
        if self.cloud_create_timer == 0:
            self.cloud_create_timer = CREATE_CLOUD_DELAY

            direction = r.choice(DIRECTIONS)
            y = r.randint(0, 500)
            x = -627
            if direction == LEFT:
                x = WIDTH
            cloud = Cloud(x,y, direction,self.screen)
            self.cloud_group.add(cloud)

    def fireball_bird_collision(self, fireball, bird):
        if fireball.rect.colliderect(bird.rect):
            self.score += bird.speed
            self.pop_sfx.play()
            print(f"score {self.score}")
            return True
        else:
            return False

    def giant_fireball_bird_collision(self, giant_fireball, bird):
        if giant_fireball.rect.colliderect(bird.rect):
            self.score += bird.speed
            self.pop_sfx.play()
            print(f"score {self.score}")
            return True
        else:
            return False
    def player_bird_collision(self, player, bird):
        if player.rect.colliderect(bird.rect):
            self.game_mode = GAME_LANDING_PAGE
            self.pop_sfx.play()
            return True
        else:
            return False



    def game_loop(self):
        # -------- Main Program Loop -----------
        while self.running:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False



            pygame.display.flip()
            if self.game_mode == GAME_IN_SESSION:
                self.game_in_session()
            elif self.game_mode == GAME_LANDING_PAGE:
                self.game_landing_page()
            #print(f"bird count = {len(self.bird_group.sprites())}")
            #print(f"cloud count = {len(self.cloud_group.sprites())}")
            #print(f"fireball count = {len(self.fireball_group.sprites())}")
            # --- Limit to 60 frames per second
            self.clock.tick(FPS)
            current_fps = str(self.clock.get_fps())
            pygame.display.set_caption(f'{self.project_name}, fps: {current_fps}')

        # Close the window and quit.
        pygame.quit()

    def game_landing_page(self):
        self.screen.blit(self.background, (0,0))
        self.draw_play_button_and_title()
        self.create_bird()
        self.bird_group.update()
        self.create_cloud()
        self.cloud_group.update()

    def draw_play_button_and_title(self):
        middle_x = WIDTH /2
        middle_y = HEIGHT /2

        play_button_x = middle_x - (self.play_button.get_width()/2)
        play_button_y = middle_y - (self.play_button.get_height() / 2)

        self.screen.blit(self.play_button, (play_button_x, play_button_y))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if play_button_x <= mouse_x <= play_button_x + self.play_button.get_width():
            if play_button_y <= mouse_y <= play_button_y + self.play_button.get_height():
                if pygame.mouse.get_pressed()[0]:
                    self.bird_group.empty()
                    self.player_group.add(self.player)
                    self.score = 0
                    self.player.set_location(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
                    # the clouds is covering the play button and the bird title
                    self.game_mode = GAME_IN_SESSION

        title_x = middle_x - (self.title.get_width()/2)
        title_y = middle_y - (self.title.get_height()/2)- 140
        self.screen.blit(self.title, (title_x, title_y))

    def game_in_session(self):
        self.screen.blit(self.background, (0, 0))
        self.create_cloud()
        self.launch_fireball()
        self.launch_giant_fireball()
        self.create_bird()

        self.cloud_group.update()
        self.bird_group.update()
        self.player_group.update()
        self.fireball_group.update()
        self.giant_fireball_group.update()

        self.draw_giant_fireball_cooldown_indicator()
        self.draw_score()
        pygame.sprite.groupcollide(self.fireball_group, self.bird_group, True, True, self.fireball_bird_collision)
        pygame.sprite.groupcollide(self.player_group, self.bird_group, True, True, self.player_bird_collision)
        pygame.sprite.groupcollide(self.giant_fireball_group, self.bird_group, False, True, self.giant_fireball_bird_collision)

if __name__ == '__main__':
    sb = Birdie()
    sb.game_loop()


