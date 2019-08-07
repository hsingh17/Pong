import pygame
import math
import random

class Paddle:
    def __init__(self, x, top_y, face):
        self.x = x
        self.top_y = top_y
        self.bottom_y = top_y + 80
        self.face = face

    def draw(self):
        pygame.draw.rect(window, WHITE, (self.x, self.top_y, 20, 80))

    def move(self, dy):
        if self.bottom_y + dy <= SCREEN_HEIGHT and self.top_y + dy >= 0:
            self.top_y += dy
            self.bottom_y += dy

    def get_face_cords(self):
        cords = []
        if self.face == 'E':
            for i in range(81):
                cords.append((self.x + 20, self.top_y + i))
        elif self.face == 'W':
            for i in range(81):
                cords.append((self.x, self.top_y + i))
        return cords

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v_x = 5
        self.v_y = -2
        
    def draw(self):
        pygame.draw.rect(window, WHITE, (self.x, self.y, 10, 10))

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

    def get_cords(self):
        cords = []
        for i in range(2):
            for z in range(11):
                cords.append((self.x + 10 * i, self.y + z))
        return cords
        
    def check_collision(self, paddle):    
        for p_cord in paddle.get_face_cords():
            for b_cord in self.get_cords():
                if b_cord[1] <= 0 or b_cord[1] >= 500:
                    self.v_y *= -1
                    break
                elif p_cord == b_cord:
                    self.v_x *= -1
                    break

def check_point(ball):
    if ball.x >= 500 or ball.x <= 0:
        return 1
    else:
        return 0

def display_score(p1_score, p2_score):
    p1_msg = LARGE_FONT.render(f'{p1_score}', True, GRAY)
    window.blit(p1_msg, (140,30))

    p2_msg = LARGE_FONT.render(f'{p2_score}', True, GRAY)
    window.blit(p2_msg, (330,30))

def create_stripes():
    for i in range(0, 500, 25):
        pygame.draw.rect(window, GRAY, (SCREEN_WIDTH/2 - 5, i + 5, 10, 10))

def check_win(p1_score, p2_score):
    if p1_score == WIN_CONDITION or p2_score == WIN_CONDITION:
        return True
    return False

def winner_message(p1_score, p2_score):
    if p1_score == WIN_CONDITION:
        message = MEDIUM_FONT.render('Player 1 Wins!', True, WHITE)
    else:
        message = MEDIUM_FONT.render('Player 2 Wins!', True, WHITE)

    window.blit(message, (100,200))
    play_again = SMALL_FONT.render('Press Q to Exit or R to Restart!', True, WHITE)
    window.blit(play_again, (75, 250))

def game_loop():
    clock = pygame.time.Clock()
    FPS = 60
    movement = 900 / FPS    
    player1 = Paddle(30,210,'E')
    player2 = Paddle(450,210,'W')
    ball = Ball(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    p1_score = 0
    p2_score = 0

    run = True
    winner = False
    while run:

        #loop runs only when there is a winner
        while winner:
            winner_message(p1_score, p2_score)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_loop()
                    elif event.key == pygame.K_q:
                        run = False
                        winner = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #constantly check when keys are held down
        pressed_keys = pygame.key.get_pressed() 
        if pressed_keys[pygame.K_w]:
            player1.move(-movement)
        elif pressed_keys[pygame.K_s]:
            player1.move(movement)

        if pressed_keys[pygame.K_UP]:
            player2.move(-movement)
        elif pressed_keys[pygame.K_DOWN]:
            player2.move(movement)
            
        #check collision with paddle or top and bottom
        if ball.v_x > 0:
            ball.check_collision(player2)
        else:
            ball.check_collision(player1)

        #check if ball has made it to one of the end goals
        if check_point(ball):
            new_ball = Ball(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
            if ball.x <= 0:
                p2_score += 1
                new_ball.v_x = -5
            elif ball.x >= 500:
                p1_score += 1
                new_ball.v_x = 5

            ball_y = random.randrange(-5,5)
            while ball_y == 0:
                ball_y = random.randrange(-5,5)

            new_ball.v_y = ball_y
            ball = new_ball

        ball.move()
        window.fill((0,0,0))

        create_stripes()
        player1.draw()
        player2.draw()
        ball.draw()
        display_score(p1_score, p2_score)
        
        #sets winner to True so that winner message can appear
        if check_win(p1_score, p2_score):
            winner = True

        clock.tick(FPS)
        pygame.display.update()

pygame.font.init()
pygame.init()

#constants for easy changes
LARGE_FONT = pygame.font.SysFont("Bit5x3 Regular", 100)
MEDIUM_FONT = pygame.font.SysFont("Bit5x3 Regular", 50)
SMALL_FONT = pygame.font.SysFont("Bit5x3 Regular", 25)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WHITE = (255,255,255)
GRAY = (128,128,128)
WIN_CONDITION = 10

window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
game_loop()
