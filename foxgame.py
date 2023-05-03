import pygame
import os
import random
pygame.font.init()

HEIGHT, WIDTH = 600, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BIRD_IMGS = [pygame.image.load(os.path.join("imgs", "bird1.png")), pygame.image.load(os.path.join("imgs", "bird2.png")), pygame.image.load(os.path.join("imgs", "bird3.png")), pygame.image.load(os.path.join("imgs", "bird2.png"))]
BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")), (WIDTH, HEIGHT))
FOX = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fox.png")), (100, 100))
FOX_BITING = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fox-open-mouth.png")), (100, 100))
FONT = pygame.font.SysFont("comicsans", 20)
BIG_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    ANIMATION_TIME = 5
    IMGS = BIRD_IMGS

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = self.IMGS[0]
        self.img_count = 0
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, win):
        self.img_count += 1

        self.img = self.IMGS[(self.img_count // self.ANIMATION_TIME % 4)]
        win.blit(self.img, (self.x, self.y))

    def get_height(self):
        return self.img.get_height()

    def move(self, vel):
            self.y += vel

    def off_screen(self):
        return self.y > HEIGHT - self.get_height()

class Fox:
    def __init__(self, x, y, img, vel):
        self.x = x
        self.y = y
        self.img = img
        self.vel = vel
        self.birds_eaten = 0
        self.lives = 5
        self.level = 1
        self.mask = pygame.mask.from_surface(self.img)

    def get_height(self):
        return self.img.get_height()
    
    def get_width(self):
        return self.img.get_width()
    
    def open_mouth(self, win):
        win.blit(FOX_BITING, (self.x, self.y))

    def collide(self, obj):
        offset_x = obj.x - self.x
        offset_y = obj.y - self.y
        return self.mask.overlap(obj.mask, (offset_x, offset_y)) != None
    
    def draw(self, win):
        win.blit(FOX, (self.x, self.y))

    def birds_eaten_display(self, win):
        kill_count_label = FONT.render(f"Birds eaten: {self.birds_eaten}", 1, (0, 0, 0))
        win.blit(kill_count_label, (10, 20))
    
    def lives_display(self, win):
        lives_label = FONT.render(f"Lives: {self.lives}", 1, (0, 0, 0))
        win.blit(lives_label, (WIDTH - 100, 20))
    
    def level_display(self, win):
        level_label = FONT.render(f"Level {self.level}", 1, (0, 0, 0))
        win.blit(level_label, (10, 60))

    

def main():
    FPS = 30
    col_count = 0
    bird_number = 5

    lost_label = BIG_FONT.render("You lost :( Press A to try again! :)", 1, (0, 0, 0))

    birds = []
    clock = pygame.time.Clock()

    def spawn_birds(bird_number):
        for i in range(bird_number):
            bird = Bird(random.randrange(0, WIDTH - 50), random.randrange(-300, -100), BIRD_IMGS[0])
            birds.append(bird)

    def win():
        return col_count == bird_number
    
    def lost():
        return fox.lives == 0
    
    def redraw_window(label):
        WIN.blit(BG, (0, 0))
        WIN.blit(label, (WIDTH/2 - label.get_width()/2, HEIGHT/2))
        pygame.display.update()

    fox = Fox(random.randrange(0, WIDTH - 50), HEIGHT - 100, FOX, 6)
    spawn_birds(bird_number)

    run = True
    
    while run:
        pygame.init()
        WIN.blit(BG, (0, 0))
        fox.level_display(WIN)
        fox.birds_eaten_display(WIN)
        fox.lives_display(WIN)
        fox.draw(WIN)

        for bird in birds:
            bird.draw(WIN)
            bird.move(3)
        
            if bird.off_screen() and len(birds) > 0:
                fox.lives -= 1
                birds.remove(bird)
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and fox.y + fox.vel < HEIGHT - fox.get_height():
            fox.y += fox.vel
        if keys[pygame.K_UP] and fox.y - fox.vel > 0:
            fox.y -= fox.vel
        if keys[pygame.K_LEFT] and fox.x - fox.vel > 0:
            fox.x -= fox.vel
        if keys[pygame.K_RIGHT] and fox.x + fox.vel < WIDTH - fox.get_width():
            fox.x += fox.vel
        if keys[pygame.K_SPACE]:
            fox.open_mouth(WIN)
        elif keys[pygame.K_a] and lost():
            main()
        
        for bird in birds:
            if fox.collide(bird) and len(birds) > 0:
                fox.open_mouth(WIN)
                fox.birds_eaten += 1
                col_count += 1
                birds.remove(bird)
        
        if lost():
            redraw_window(lost_label)
        
        elif win() or (len(birds) == 0 and not lost()):

            col_count = 0
            fox.level += 1
            bird_number += 1
            spawn_birds(bird_number)
        
       
        pygame.display.update()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    
    quit()

main()

    
    
