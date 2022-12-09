import socket
from _thread import *
import sys
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#server = '192.168.1.3'
server = '192.168.56.1'
port = 5555

idCount = 0

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Esperando por uma conexão...")


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

def change_position():
    global ready, player, player2, ball, left_score, right_score
    return f'{ready},{player.x},{player.y},{player2.x},{player2.y},{ball.x},{ball.y},{ball.x_vel},{ball.y_vel},{left_score},{right_score}'

def threaded_client(conn, p):
    global pos, idCount, ready, player, player2, ball, left_score, right_score
    
    conn.send(str.encode(str(p)))
    reply = ''

    if(idCount == 2):
        ready = 1
    
    while True:

        try:

            print(f'position:{p}:{ready},{player.x},{player.y},{player2.x},{player2.y},{ball.x},{ball.y},{ball.x_vel},{ball.y_vel},{left_score},{right_score}')

            if ready:
                ball.move()

            if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
                reset()
                ready = 1

            data = conn.recv(4096)
            reply = data.decode('utf-8')

            if not data:
                break

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
            
            conn.sendall(str.encode(change_position()))
        except:
            break

    print("Conexão fechada")

    idCount -= 1
    if idCount == 0:
        reset()

    ready = 0
    conn.close()

while True:
    conn, addr = s.accept()
    print("Conectado: ", addr)

    idCount += 1

    if idCount == 3:
        idCount -= 1
        print("Apenas 2 jogadores por vez")
        conn.close()
        continue

    start_new_thread(threaded_client, (conn, idCount-1))
