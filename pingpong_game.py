import pygame
import numpy as np
from collections import namedtuple

from enum import Enum
import random

pygame.init()

BLOCK_HEIGHT = 10
BLOCK_WIDTH = 100

BALL_WIDTH = 10
BALL_HEIGHT = 10
SPEED = 60

WHITE = (255, 255, 255)

font = pygame.font.SysFont("comicsans", 25)

Point = namedtuple("Point", ["x", "y"])

class Paddle_dir(Enum):
    STAY = 0
    LEFT = 1
    RIGHT = 2

class Game():
    def __init__(self, w=800, h=600):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        #self.ball = Point(x=self.w/2, y=BALL_WIDTH)
        #self.paddle = Point(x=self.w/2, y=self.h-BLOCK_HEIGHT)
        #self.ball_move_val_x = random.randrange(-8, 8)
        #self.ball_move_val_y = 10
        self.reset()
    
    def reset(self):
        self.score = 0

        self.ball = Point(x=self.w/2, y=0)
        self.paddle = Point(x=self.w/2, y=self.h-BLOCK_HEIGHT)
        self.direction = Paddle_dir.STAY

        self.ball_move_val_x = random.randrange(-10, 10, 3)
        self.ball_move_val_y = 10
        self.move_ball()

        self.frame_iteration = 0

    def update_window(self):
        self.display.fill((0, 0, 0))

        pygame.draw.rect(self.display, WHITE, pygame.Rect(self.paddle.x, self.paddle.y, BLOCK_WIDTH, BLOCK_HEIGHT))
        pygame.draw.rect(self.display, WHITE, pygame.Rect(self.ball.x, self.ball.y, BALL_WIDTH, BALL_HEIGHT))

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def move_paddle(self, action):
        #[right, left, stay]
        x = self.paddle.x
        y = self.paddle.y
        if np.array_equal(action, [1, 0, 0]) and self.paddle.x + BLOCK_WIDTH < self.w:
            #x += 10
            self.direction = Paddle_dir.RIGHT
        elif np.array_equal(action, [0, 1, 0]) and self.paddle.x > 0:
            #x -= 10
            self.direction = Paddle_dir.LEFT
        elif np.array_equal(action, [0, 0, 1]) or self.paddle.x >= 0 or self.paddle.x + BLOCK_WIDTH >= self.w:
            #x = x
            self.direction = Paddle_dir.STAY

        if self.direction == Paddle_dir.RIGHT:
            x += 10
        elif self.direction == Paddle_dir.LEFT:
            x -= 10
        elif self.direction == Paddle_dir.STAY:
            x = x

        self.paddle = Point(x, y)
        #print(self.direction)

    def user_move_paddle(self):
        x = self.paddle.x
        y = self.paddle.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= 10
        elif keys[pygame.K_RIGHT]:
            x += 10
        
        self.paddle = Point(x, y)

    def move_ball(self):
        y = self.ball.y
        x = self.ball.x
        x += self.ball_move_val_x
        y += self.ball_move_val_y

        self.ball = Point(x, y)

    def handle_collision(self):
        #y = self.ball.y
        #x = self.ball.x
        if self.has_collided() or self.ball.y <= 0:
            self.ball_move_val_y *= (-1)
        if self.ball.x < 0 or self.ball.x > self.w - BALL_HEIGHT:
            self.ball_move_val_x *= (-1)
        #self.ball = Point(x, y)
    
    def has_collided(self):
        if self.ball.y == self.paddle.y - BLOCK_HEIGHT and self.ball.x in range(int(self.paddle.x), int(self.paddle.x + BLOCK_WIDTH + 1)):
            return True
        return False
        

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self.move_ball()
        self.handle_collision()
        self.move_paddle(action)

        reward = 0
        game_over = False

        if self.ball.y == self.h: #self.h % self.ball_move_val_y must be 0
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        if self.has_collided():
            self.score += 1
            reward = 10
        
        self.update_window()
        self.clock.tick(40)
        return reward, game_over, self.score
        

def main():
    game = Game()
    run = True
    while run:
        reward, game_over, score = game.play_step(action=[0, 0, 1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        if game_over:
            game.reset()

#main()
