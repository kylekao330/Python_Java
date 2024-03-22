import pygame
from player import Player
import random as r
from coin import Coin
from config import *
from tube import Tube

class FlappyDuck():
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Set the width and height of the screen [width, height]
    WIDTH = 1000
    HEIGHT = 643

    # FPS is Frame Per Second
    FPS = 40


    TARGET_WIDTH = 10

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.project_name = 'Flappy Duck'

        pygame.display.set_caption(self.project_name)

        # Loop until the user clicks the close button.
        self.running = True

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("assets/images/Background-01.png")


        self.play_button = pygame.image.load("assets/images/Play.png")
        self.credit_button  = pygame.image.load("assets/images/credit_button.png")
        self.title = pygame.image.load("assets/images/FlappyBirdLogo.png")
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player(200, 200, 50,self.screen)
        self.player_group.add(self.player)

        self.coin_group = pygame.sprite.Group()
        self.tube_group = pygame.sprite.Group()
        self.tube_create_timer = CREATE_TUBE_DELAY

        self.tube_create_timer = 1
        self.score = 0
        self.score_font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 80)

        self.collect5_sfx = pygame.mixer.Sound("assets/audio/collect5.wav")
        self.collect5_sfx.set_volume(1)

        self.pop_sfx = pygame.mixer.Sound("assets/audio/plop.wav")
        self.pop_sfx.set_volume(1)
        self.game_mode = GAME_LANDING_PAGE

        self.start_time = 0

    def draw_text(self,x,y, text, color):
        text_image = self.score_font.render(text, 1, color)
        self.screen.blit(text_image, (x,y))

    def draw_score(self):
        self.draw_text(30,30, f"Score {self.score}", BLACK)
        score_text = self.score_font.render(f"Score {self.score}", 1, BLACK)
        self.screen.blit(score_text, (30,30))

    def draw_big_text(self,x,y,text):
        big_score = self.big_font.render(f"{text}", 30, BLACK)
        self.screen.blit(big_score, (x,y))

    def draw_count_down(self):
        # how long_you_play_game = current_time (6pm) - Start_time (9am)
        # count_down = DURATION - how_long_you_played_the_game

        how_long_you_play_game = pygame.time.get_ticks() - self.start_time
        count_down = GAME_DURATION_IN_SECOND - how_long_you_play_game/1000
        count_down = int(count_down)

        if count_down <= 0:
            self.game_mode = GAME_WIN
        count_down_image = self.score_font.render(f"Countdown {count_down}", 1, BLACK)
        self.screen.blit(count_down_image, (WIDTH-300, 30))


    def create_tube(self):
        self.tube_create_timer -= 1
        if self.tube_create_timer == 0:
            self.tube_create_timer = CREATE_TUBE_DELAY
            tube1_y = r.choice([-200,-225,-250])
            tube = Tube(WIDTH, tube1_y, DOWNWARD, self.screen)
            self.tube_group.add(tube)

            tube1_height = tube.get_img_height() + tube1_y

            tube_2_y = tube1_height + GAP
            tube = Tube(WIDTH, HEIGHT-200, UPWARD, self.screen)
            self.tube_group.add(tube)

            coin = Coin(WIDTH + 300, 100, self.screen)
            self.coin_group.add(coin)



    def bird_coin_collision(self, player, coin):
        if coin.rect.colliderect(player.rect):
            self.score += 1
            self.collect5_sfx.play()
            print(f"score {self.score}")
            return True
        else:
            return False

    def player_tube_collision(self, player, tube):
        if tube.rect.colliderect(player.rect) and player.mode == FLYING_MODE:
            player.start_dizzy_mode()
            self.pop_sfx.play()
            return True
        else:
            return False


    def game_in_session(self):

        self.detect_player_location()
        self.create_tube()
        self.tube_group.update()
        self.player_group.update()
        self.coin_group.update()
        self.draw_count_down()
        pygame.sprite.groupcollide(self.player_group, self.coin_group, False, True, self.bird_coin_collision)
        pygame.sprite.groupcollide(self.player_group, self.tube_group, False, False, self.player_tube_collision)

    def game_landing_page(self):
        middle_x = WIDTH / 2
        middle_y = HEIGHT / 2

        title_x = middle_x - (self.title.get_width()/2)
        title_y = middle_y - (self.title.get_height()/2)
        self.screen.blit(self.title, (title_x, title_y - 175))
        self.handle_play_and_credit_buttons()


    def game_over_page(self):
        middle_x = WIDTH / 2
        middle_y = HEIGHT / 2
        self.draw_big_text(middle_x-250,middle_y-150, "GAME OVER")
        self.handle_play_and_credit_buttons()

    def game_win_page(self):
        middle_x = WIDTH / 2
        middle_y = HEIGHT / 2
        self.draw_big_text(middle_x-250,middle_y-150, "GAME WIN!")
        self.handle_play_and_credit_buttons()


    def handle_play_and_credit_buttons(self, y_adjustment=0):
        middle_x = WIDTH / 2
        middle_y = HEIGHT / 2
        play_button_x = middle_x - (self.play_button.get_width() / 2)-170
        play_button_y = middle_y - (self.play_button.get_height() / 2) + y_adjustment
        credit_button_x = middle_x - (self.credit_button.get_width() / 2)+170
        credit_button_y = middle_y - (self.credit_button.get_height() / 2)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.screen.blit(self.play_button, (play_button_x, play_button_y))
        self.screen.blit(self.credit_button, (credit_button_x, credit_button_y))
        if credit_button_x <= mouse_x <= credit_button_x + self.credit_button.get_width():
            if credit_button_y <= mouse_y <= credit_button_y + self.credit_button.get_height():
                if pygame.mouse.get_pressed()[0]:
                    self.game_mode = GAME_CREDIT
        if play_button_x <= mouse_x <= play_button_x + self.play_button.get_width():
            if play_button_y <= mouse_y <= play_button_y + self.play_button.get_height():
                if pygame.mouse.get_pressed()[0]:
                    self.tube_group.empty()
                    self.coin_group.empty()
                    self.score = 0
                    self.player.set_location(200,200)
                    self.game_mode = GAME_IN_SESSION
                    self.start_time = pygame.time.get_ticks() # current time in milliseconds


    def detect_player_location(self):
        if self.player.y > HEIGHT:
            self.pop_sfx.play()
            self.game_mode = GAME_OVER
    def game_credit_page(self):
        middle_x = WIDTH/2
        credit_x = middle_x - 200
        self.draw_text(credit_x, 20 ,"Game Developer: Kyle Kao", RED)
        self.draw_text(credit_x, 70, "Game Developer: Kyle Kao", RED)
        self.draw_text(credit_x, 120, "Game Developer: graphicriver.net", RED)
        self.draw_text(credit_x, 170, "Game Developer: audiojungle.net", RED)
        self.draw_text(credit_x, 220, "Game Advisor: Gamas Chang", RED)
        self.draw_text(credit_x, 270, "School: AYCLOGIC.COM", RED)
        self.handle_play_and_credit_buttons(100)
    def game_loop(self):
        # -------- Main Program Loop -----------
        while self.running:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
            self.screen.blit(self.background,(0,0))

            if self.game_mode == GAME_IN_SESSION:
                self.game_in_session()
            elif self.game_mode == GAME_LANDING_PAGE:
                self.game_landing_page()
            elif self.game_mode == GAME_OVER:
                self.game_over_page()
            elif self.game_mode == GAME_WIN:
                self.game_win_page()
            elif self.game_mode == GAME_CREDIT:
                self.game_credit_page()

            self.draw_score()

            # --- Limit to 60 frames per second
            self.clock.tick(FPS)

            current_fps = str(self.clock.get_fps())
            pygame.display.set_caption(f'{self.project_name}, fps: {current_fps}')



        # Close the window and quit.
        pygame.quit()

if __name__ == '__main__':
    sb = FlappyDuck()
    sb.game_loop()


