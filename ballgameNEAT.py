#Config feedforward file and NEAT algorithm implementation code taken from: https://www.youtube.com/watch?v=2f6TmKm7yx0&t=4032s&pp=ygUNcGluZ3BvbmcgbmVhdA%3D%3D

import pygame
import random
import neat
import time
import os
import pickle
pygame.font.init()

#all of the global variables
RECT_WIDTH = 20
RECT_HEIGHT = 30
RECT_VEL = 5

BALL_WIDTH = 10
BALL_HEIGHT = 10

WIN_WIDTH, WIN_HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

FONT = pygame.font.SysFont("comicsans", 20)

class Ball:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, BALL_WIDTH, BALL_HEIGHT)
        self.ball_vel_for_x = [4, -4]
        self.ball_vel_for_y = [1, -1]
        #self.mask = pygame.mask.Mask((BALL_WIDTH, BALL_HEIGHT))
        
        #self.mask.fill()

    def draw(self, WIN):
        pygame.draw.rect(WIN, (255, 255, 255), self.rect)

    def move(self):
        self.rect.y += self.ball_vel_for_y[0]
        self.rect.x += self.ball_vel_for_x[0]
    
    def reset(self):
        self.rect.y = random.randrange(50, WIN_HEIGHT-50)
        self.rect.x = WIN_WIDTH/2 - BALL_WIDTH/2

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        return False
    
    def handle_collision(self, board1, board2):

        collision_rect1 = self.rect.clip(board1.rect)
        collision_rect2 = self.rect.clip(board2.rect)

        collision_point1_y = collision_rect1.y
        collision_point2_y = collision_rect2.y

        if self.collide(board2):
            self.ball_vel_for_x = [-4, 4]
            if collision_point2_y > board2.rect.y + RECT_HEIGHT/2:
                self.ball_vel_for_y = [-1, 1]
            elif collision_point2_y < board2.rect.y + RECT_HEIGHT/2:
                self.ball_vel_for_y = [1, -1]
        
        elif self.collide(board1):
            self.ball_vel_for_x = [4, -4]
            if collision_point1_y > board1.rect.y + RECT_HEIGHT/2:
                self.ball_vel_for_y = [-1, 1]
            elif collision_point1_y < board1.rect.y + RECT_HEIGHT/2:
                self.ball_vel_for_y = [1, -1]
        
        elif self.rect.y < 0:
            self.ball_vel_for_y = [1, -1]
        
        elif self.rect.y > WIN_HEIGHT - BALL_HEIGHT:
            self.ball_vel_for_y = [-1, 1]

class Board():
    def __init__(self, x, y, label_x, label_y):
        self.label_x = label_x
        self.label_y = label_y
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, RECT_WIDTH, RECT_HEIGHT)
        #self.mask = pygame.mask.Mask((RECT_WIDTH, RECT_HEIGHT))
        
        #self.mask.fill()
    
    def draw(self, WIN):
        pygame.draw.rect(WIN, (255, 255, 255), self.rect)
    
    def move(self, up=True):
        if up:
            self.rect.y -= RECT_VEL
        else:
            self.rect.y += RECT_VEL
    
    def reset(self, left=True):
        if left:
            self.rect.x = 5
            self.rect.y = WIN_HEIGHT/2 - RECT_HEIGHT/2
        else:
            self.rect.x = WIN_WIDTH - RECT_WIDTH - 5
            self.rect.y = WIN_WIDTH - RECT_WIDTH - 5, WIN_HEIGHT/2 - RECT_HEIGHT/2

    #def display_score(self):
        #score_label = FONT.render("Score: " + str(self.score), 1, (255, 255, 255))
        #WIN.blit(score_label, (self.label_x, self.label_y))
class GameInfo:
    def __init__(self, board1_score, board2_score):
        self.board1_score = board1_score
        self.board2_score = board2_score



class Game:
    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height

        self.board1 = Board(5, WIN_HEIGHT/2 - RECT_HEIGHT/2, WIN_WIDTH/2 - 250, 10)
        self.board2 = Board(WIN_WIDTH - RECT_WIDTH - 5, WIN_HEIGHT/2 - RECT_HEIGHT/2, WIN_WIDTH/2 + 100, 10)
        self.ball = Ball(WIN_WIDTH/2 - BALL_WIDTH/2, WIN_HEIGHT/2)

        self.board1_score = 0
        self.board2_score = 0

    def draw_score(self, window):
        board1_score_label = FONT.render("Score: " + str(self.board1_score), 1, (255, 255, 255))
        board2_score_label = FONT.render("Score: " + str(self.board2_score), 1, (255, 255, 255))

        window.blit(board1_score_label, (self.board1.label_x, self.board1.label_y))
        window.blit(board2_score_label, (self.board2.label_x, self.board2.label_y))

    def draw(self):
        self.window.fill((0, 0, 0))
        self.draw_score(self.window)

        for board in [self.board1, self.board2]:
            board.draw(self.window)

        self.ball.draw(self.window)

    def move_board(self, left=True, up=True):
        if left:
            if up and self.board1.rect.y - RECT_VEL < 0:
                return False
            if not up and self.board1.rect.y + RECT_HEIGHT > self.window_height:
                return False
            self.board1.move(up)
        else:
            if up and self.board2.rect.y - RECT_VEL < 0:
                return False
            if not up and self.board2.rect.y + RECT_HEIGHT > self.window_height:
                return False
            self.board2.move(up)

        return True
    
    def loop(self):
        self.ball.move()
        self.ball.handle_collision(self.board1, self.board2)

        if self.ball.rect.x < 0:
            self.ball.reset()
            self.board2_score += 1
        elif self.ball.rect.x > self.window_width:
            self.ball.reset()
            self.board1_score += 1

        game_info = GameInfo(self.board1_score, self.board2_score)
        return game_info
    
    def reset(self):
        self.ball.reset()
        self.board1.reset()
        self.board2.reset(False)
        self.board1_score = 0
        self.board2_score = 0

class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(WIN, WIN_WIDTH, WIN_HEIGHT)
        self.board1 = self.game.board1
        self.board2 = self.game.board2
        self.ball = self.game.ball

    def test_ai(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.game.move_board(left=True, up=True)
            if keys[pygame.K_DOWN]:
                self.game.move_board(left=True, up=False)

            game_info = self.game.loop()
            print(game_info.board1_score, game_info.board2_score)
            self.game.draw()
            pygame.display.update()
    
    def train_ai(self, genome1, genome2, config):
            net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
            net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                
                output1 = net1.activate((self.board1.rect.y, self.ball.rect.y, abs(self.board1.rect.x - self.ball.rect.x)))
                decision1 = output1.index(max(output1))
                output2 = net2.activate((self.board2.rect.y, self.ball.rect.y, abs(self.board2.rect.x - self.ball.rect.x)))
                decision2 = output2.index(max(output2))

                if decision1 == 0:
                    pass
                elif decision1 == 1:
                    self.game.move_board(left=True, up=True)
                else:
                    self.game.move_board(left=True, up=False)
                
                if decision2 == 0:
                    pass
                elif decision2 == 1:
                    self.game.move_board(left=False, up=True)
                else:
                    self.game.move_board(left=False, up=False)

                game_info = self.game.loop()
                self.game.draw()
                pygame.display.update()

                if game_info.board1_score >= 1 or game_info.board2_score >= 1 or game_info.board1_score > 50:
                    self.calculate_fitness(genome1, genome2, game_info)
                    break
            
    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.board1_score
        genome2.fitness += game_info.board2_score


def eval_genomes(genomes, config):
    width, height = 700, 500
    window = pygame.display.set_mode

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes)-1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(WIN, WIN_WIDTH, WIN_HEIGHT)
            game.train_ai(genome1, genome2, config)


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    run_neat(config)
        
            




        