import pygame
import random
pygame.font.init()

#all of the global variables
RECT_WIDTH = 20
RECT_HEIGHT = 100
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
        #self.mask = pygame.mask.Mask((BALL_WIDTH, BALL_HEIGHT))
        
        #self.mask.fill()

    def draw(self, WIN):
        pygame.draw.rect(WIN, (255, 255, 255), self.rect)

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        return False

class Board():
    def __init__(self, x, y, label_x, label_y):
        self.label_x = label_x
        self.label_y = label_y
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, RECT_WIDTH, RECT_HEIGHT)
        self.score = 0
        #self.mask = pygame.mask.Mask((RECT_WIDTH, RECT_HEIGHT))
        
        #self.mask.fill()
    
    def draw(self, WIN):
        pygame.draw.rect(WIN, (255, 255, 255), self.rect)

    def move_up(self):
        self.rect.y -= RECT_VEL
    
    def move_down(self):
        self.rect.y += RECT_VEL

    def display_score(self):
        score_label = FONT.render("Score: " + str(self.score), 1, (255, 255, 255))
        WIN.blit(score_label, (self.label_x, self.label_y))



def main():
    clock = pygame.time.Clock()
    FPS = 60

    board1 = Board(5, WIN_HEIGHT/2 - RECT_HEIGHT/2, WIN_WIDTH/2 - 250, 10)
    board2 = Board(WIN_WIDTH - RECT_WIDTH - 5, WIN_HEIGHT/2 - RECT_HEIGHT/2, WIN_WIDTH/2 + 100, 10)
    ball = Ball(WIN_WIDTH/2 - BALL_WIDTH/2, WIN_HEIGHT/2)

    ball_vel_for_x = [4,-4]
    ball_vel_for_y = [1,-1]


    run = True
    while run:
        pygame.init()
        WIN.fill((0, 0, 0))

        board1.draw(WIN)
        board2.draw(WIN)
        ball.draw(WIN)

        board1.display_score()
        board2.display_score()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and board1.rect.y > 0:
            board1.move_up()
        if keys[pygame.K_DOWN] and board1.rect.y < WIN_HEIGHT - RECT_HEIGHT:
            board1.move_down()
        
        if keys[pygame.K_w] and board2.rect.y > 0:
            board2.move_up()
        if keys[pygame.K_s] and board2.rect.y < WIN_HEIGHT - RECT_HEIGHT:
            board2.move_down()

        ball.rect.y += ball_vel_for_y[0]
        ball.rect.x += ball_vel_for_x[0]

        collision_rect1 = ball.rect.clip(board1.rect)
        collision_rect2 = ball.rect.clip(board2.rect)

        collision_point1_y = collision_rect1.y
        collision_point2_y = collision_rect2.y

        if ball.collide(board2):
            ball_vel_for_x = [-4, 4]
            if collision_point2_y > board2.rect.y + RECT_HEIGHT/2:
                ball_vel_for_y = [-1, 1]
            elif collision_point2_y < board2.rect.y + RECT_HEIGHT/2:
                ball_vel_for_y = [1, -1]
        
        elif ball.collide(board1):
            ball_vel_for_x = [4, -4]
            if collision_point1_y > board1.rect.y + RECT_HEIGHT/2:
                ball_vel_for_y = [-1, 1]
            elif collision_point1_y < board1.rect.y + RECT_HEIGHT/2:
                ball_vel_for_y = [1, -1]
        
        elif ball.rect.y < 0:
            ball_vel_for_y = [1, -1]
        
        elif ball.rect.y > WIN_HEIGHT - BALL_HEIGHT:
            ball_vel_for_y = [-1, 1]
        
        elif ball.rect.x < 0:
            board2.score += 1
            ball.rect.y = random.randrange(50, WIN_HEIGHT-50)
            ball.rect.x = WIN_WIDTH/2 - BALL_WIDTH/2
        
        elif ball.rect.x > WIN_WIDTH:
            board1.score += 1
            ball.rect.y = random.randrange(50, WIN_HEIGHT - 50)
            ball.rect.x = WIN_WIDTH/2 - BALL_WIDTH/2


        pygame.display.update()
        clock.tick(FPS)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    
    
    quit()

main()
        

    







