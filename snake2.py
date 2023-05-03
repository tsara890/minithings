import pygame
import random
pygame.font.init()

WIN_WIDTH, WIN_HEIGHT = 500, 500
FONT = pygame.font.SysFont("comicsans", 20)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
SQUARE_WIDTH, SQUARE_HEIGHT = 10, 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Square:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, SQUARE_WIDTH, SQUARE_HEIGHT)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        return False
    
class Snake:
    def __init__(self, square_x, square_y):
        self.square_x = square_x
        self.square_y = square_y
        self.square_num = 3
        self.score = 0
        self.squares = []

    def draw_snake(self):
        for i in range(self.square_num):
            square = Square(self.square_x, self.square_y, WHITE)
            self.square_x += 15
            self.squares.append(square)
    
    def add_square(self, x, y):
        square = Square(x, y, WHITE)
        self.squares.append(square)

    def move(self, up=False, down=False, left=False, right=False):
        if up:
            self.squares[0].rect.x = self.squares[-1].rect.x
            self.squares[0].rect.y = self.squares[-1].rect.y - 15
            self.squares.append(self.squares[0])
            self.squares.remove(self.squares[0])
        if down:
            self.squares[0].rect.x = self.squares[-1].rect.x
            self.squares[0].rect.y = self.squares[-1].rect.y + 15
            self.squares.append(self.squares[0])
            self.squares.remove(self.squares[0])
        if right:
            self.squares[0].rect.x = self.squares[-1].rect.x + 15
            self.squares[0].rect.y = self.squares[-1].rect.y
            self.squares.append(self.squares[0])
            self.squares.remove(self.squares[0])
        if left:
            self.squares[0].rect.x = self.squares[-1].rect.x - 15
            self.squares[0].rect.y = self.squares[-1].rect.y
            self.squares.append(self.squares[0])
            self.squares.remove(self.squares[0])

    def off_screen_up(self):
        if self.squares[-1].rect.y < 0:
            return True
        return False
    def off_screen_down(self):
        if self.squares[-1].rect.y > WIN_HEIGHT:
            return True
        return False
    def off_screen_left(self):
        if self.squares[-1].rect.x < 0:
            return True
        return False
    def off_screen_right(self):
        if self.squares[-1].rect.x > WIN_WIDTH:
            return True
        return False
    
    def display_score(self, win):
        score_label = FONT.render("Score: " + str(self.score), 1, WHITE)
        win.blit(score_label, (10, 10))

    
def main():
    clock = pygame.time.Clock()
    FPS = 10
    run = True

    move_up = False
    move_down = False
    move_left = False
    move_right = False

    red_squares = []

    def add_red_squares(square_num):
        for i in range(square_num):
            red_square = Square(random.randrange(10, WIN_WIDTH-10), random.randrange(10, WIN_HEIGHT-10), RED)
            red_squares.append(red_square)
    
    snake = Snake(random.randrange(50, WIN_WIDTH-100), random.randrange(50, WIN_HEIGHT-100))

    snake.draw_snake()
    add_red_squares(1)
    
    while run:
        pygame.init()

        snake.display_score(WIN)

        for square in snake.squares:
            square.draw(WIN)

        for red_square in red_squares:
            red_square.draw(WIN)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not move_down:
            move_up = True
            move_down = False
            move_right = False
            move_left = False
        elif keys[pygame.K_DOWN] and not move_up:
            move_up = False
            move_down = True
            move_right = False
            move_left = False
        elif keys[pygame.K_LEFT] and not move_right:
            move_up = False
            move_down = False
            move_right = False
            move_left = True
        elif keys[pygame.K_RIGHT] and not move_left:
            move_up = False
            move_down = False
            move_right = True
            move_left = False
        
        if move_up:
            snake.move(up=True)
        elif move_down:
            snake.move(down=True)
        elif move_left:
            snake.move(left=True)
        elif move_right:
            snake.move(right=True)
        
        for red_square in red_squares:
            if red_square.collide(snake.squares[-1]):
                red_squares.remove(red_square)
                snake.add_square(snake.squares[-1].rect.x, snake.squares[-1].rect.y)
                snake.score += 1
        
        if len(red_squares) == 0:
            add_red_squares(1)

        squares_cpy = snake.squares[0:-2]
        for square in squares_cpy:
            if snake.squares[-1].collide(square):
                move_up = False
                move_down = False
                move_left = False
                move_right = False
                while len(snake.squares) != 3:
                    snake.squares.pop()
                snake.score = 0
        
        if snake.off_screen_up():
            snake.squares[-1].rect.y += WIN_HEIGHT
        elif snake.off_screen_down():
            snake.squares[-1].rect.y -= WIN_HEIGHT
        elif snake.off_screen_left():
            snake.squares[-1].rect.x += WIN_WIDTH
        elif snake.off_screen_right():
            snake.squares[-1].rect.x -= WIN_WIDTH
        
        pygame.display.update()
        WIN.fill(BLACK)
        clock.tick(FPS)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    
    quit()
main()