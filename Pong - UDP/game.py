import pygame
from network import Network
import pickle

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.font.init()
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

class Player():

    def __init__(self, startx, starty, width, height, color=WHITE):
        self.x = self.original_x = startx
        self.y = self.original_y = starty
        self.width = width
        self.height = height
        self.velocity = 3
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Ball:
    MAX_VEL = 3
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

def draw(win, HEIGHT, WIDTH, paddles, ball, left_score, right_score):

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) -
                                right_score_text.get_width()//2, 20))

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h             
        self.canvas = Canvas(self.width, self.height, "Pong")
        self.ready = 0
        self.left_score = 0
        self.right_score = 0

    def run(self):
        clock = pygame.time.Clock()

        PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
        BALL_RADIUS = 7

        self.player = Player(10, self.height//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, (255,0,0))
        self.player2 = Player(self.width - 10 - PADDLE_WIDTH, self.height//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, (0,0,139))    
        self.ball = Ball(self.width // 2, self.height//2, BALL_RADIUS)

        keys = "None"
        run = True
        
        while run:

            clock.tick(FPS)

            keys = pygame.key.get_pressed()

            rec = self.send_data(keys)
            self.parse_data(self, rec)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            if not self.ready:
                font = pygame.font.SysFont("comicsans", 50)
                text = font.render("Esperando por jogador...", 1, (255,0,0), True)
                self.canvas.get_canvas().blit(text, (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2))
                pygame.display.update()
            else: 
                # Update Canvas
                self.canvas.draw_background()
                draw(self.canvas.get_canvas(), self.height, self.width, [self.player, self.player2], self.ball, self.left_score, self.right_score)
                self.player.draw(self.canvas.get_canvas())
                self.player2.draw(self.canvas.get_canvas())
                self.canvas.update()

        pygame.quit()

    def send_data(self, keys):

        #print("ID: ", self.net.id, "  é o primeiro: ", self.net.id == '0')
        if self.net.id == '0':
            data =  f'{self.net.id},{0 if keys == "None" else int(keys[pygame.K_w])},{0 if keys == "None" else int(keys[pygame.K_s])}'
        else:
             data =  f'{self.net.id},{0 if keys == "None" else int(keys[pygame.K_UP])},{0 if keys == "None" else int(keys[pygame.K_DOWN])}'

        return self.net.send(data)

    @staticmethod
    def parse_data(self, data):
        
        d = data.split(",")
        self.ready = int(float(d[1]))
        self.player.x = int(float(d[2]))
        self.player.y = int(float(d[3]))
        self.player2.x = int(float(d[4]))
        self.player2.y = int(float(d[5]))
        self.ball.x = int(float(d[6]))
        self.ball.y = int(float(d[7]))
        self.ball.x_vel = int(float(d[8]))
        self.ball.y_vel = int(float(d[9]))
        self.left_score = int(float(d[10]))
        self.right_score = int(float(d[11]))
        #print("d[0]", d[0], "d[1]", d[1], "d[2]", d[2], "d[3]", d[3], "d[4]", d[4], "d[5]", d[5], "d[6]", d[6], "d[7]", d[7], "d[8]", d[8], "d[9]", d[9], "d[10]", d[10])


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill(BLACK)
