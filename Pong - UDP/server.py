import socket
from _thread import *
import sys
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = '192.168.1.5'
port = 5555

idCount = 0

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

print("Ouvindo...")


FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Player():

    def __init__(self, startx, starty, width, height, color=WHITE):
        self.x = self.original_x = startx
        self.y = self.original_y = starty
        self.width = width
        self.height = height
        self.velocity = 4
        self.color = color

    def move(self, up=True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VEL = 4
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

ready = 0
left_score = 0
right_score = 0

jogadores = {}
count = 0

width = 700
height = 500
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

ball = Ball(width // 2, height//2, BALL_RADIUS) 
player = Player(10, height//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, (255,0,0))
player2 = Player(width - 10 - PADDLE_WIDTH, height//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, (0,0,139))
WINNING_SCORE = 10

def handle_collision(ball, HEIGHT, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_paddle_movement_player1(up, down, player, HEIGHT):
    
    if up and player.y - player.velocity >= 0:
        player.move(up=True)
    if down and player.y + player.velocity + player.height <= HEIGHT:
        player.move(up=False)

def handle_paddle_movement_player2(up, down, player2, HEIGHT):
    if up and player2.y - player2.velocity >= 0:
        player2.move(up=True)
    if down and player2.y + player2.velocity + player2.height <= HEIGHT:
        player2.move(up=False)


def reset():
    global ready, player, player2, ball, left_score, right_score
    ready = 0
    left_score = 0
    right_score = 0
    ball.reset()
    player.reset()
    player2.reset()

def change_position(addr):
    global ready, player, player2, ball, left_score, right_score
    print(jogadores)
    return f'{jogadores[addr]},{ready},{player.x},{player.y},{player2.x},{player2.y},{ball.x},{ball.y},{ball.x_vel},{ball.y_vel},{left_score},{right_score}'
   

while True:


    

    try:
        data, addr = s.recvfrom(4096)
        reply = data.decode('utf-8')

        print("Teste1: ", reply, addr[0])
        if not reply:
            break
        print(reply == "ID")

        if addr[0] not in jogadores:
            jogadores[addr[0]] = count
            count += 1

        if reply == "ID":
            s.sendto(str.encode(change_position(addr[0])), addr)
            print("Teste2: ", reply, addr)
            continue

        print(f'position:{jogadores[addr[0]]}:{ready},{player.x},{player.y},{player2.x},{player2.y},{ball.x},{ball.y},{ball.x_vel},{ball.y_vel},{left_score},{right_score}')

        if len(jogadores) == 2:
            ready = 1
            ball.move()

        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            reset()

        arr = reply.split(',')
        id = int(arr[0])
        up = int(arr[1])
        down = int(arr[2])
        print("Recebido: " + reply)
        print(f'{id}: {up}, {down}')

        if up or down:
            if id == 0:
                handle_paddle_movement_player1(up, down, player, height)
            else:
                handle_paddle_movement_player2(up, down, player2, height)

        handle_collision(ball, height, player, player2)

        if ball.x < 0:
            right_score += 1
            ball.reset()

        elif ball.x > width:
            left_score += 1
            ball.reset()
        
        s.sendto(str.encode(change_position(addr[0])), addr)
    except:
        if len(jogadores) > 0:
            print("Conexão fechada")
            ready = 0
            jogadores.pop(addr[0])
            if len(jogadores) == 0:
                reset()
        break



    
    
