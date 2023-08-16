import pygame, random

pygame.init()

clock=pygame.time.Clock()
winX, winY = 1000, 700
pygame.display.set_caption('Pong')
screen=pygame.display.set_mode((winX,winY))

started_once = False

white = (255, 255, 255)

def display_text(text, pos, size, isItalic=False):
    font = pygame.font.SysFont("couriernew", size, bold=True, italic=isItalic)
    screen_text = font.render(text, True, white)
    screen.blit(screen_text, pos)

class Player():
    def __init__(self, x, y):
        self.top = y
        self.rect =  pygame.Rect(x,y,20,150)
        self.score=0
    
    def update(self, up, down, pos):
        dy=0
        keys=pygame.key.get_pressed()

        if keys[up]:
            dy -= 8
        elif keys[down]:
            dy += 8
        
        self.rect.y += dy

        self.rect.top=max(self.rect.top, 0)
        self.rect.bottom=min(self.rect.bottom, winY)

        display_text(str(self.score), (pos, 30), 70)

        pygame.draw.rect(screen,'white', self.rect)
        

# Initializing Players
stick_posY = (winY - 150)//2

player1 = Player(0, stick_posY)
player2 = Player(winX-20, stick_posY)

class Wall():
    def __init__(self, dir):
        self.dir=dir
        self.rect = pygame.Rect(self.dir[0], self.dir[1], winX-44, 20)

    def drop(self):
        pygame.draw.rect(screen, 'brown', self.rect)

# Putting the Walls
wallUp = Wall([22, 0])
wallDown = Wall([22, winY-20])


class Ball():
    def __init__(self, x, y):
        self.size = 15
        self.new_game = False
        self.rect = pygame.Rect(x, y, self.size, self.size)

        # differential change in position of the block
        self.dx = 7
        self.dy = 7
        #random.randint(-1,1) * random.randint(3,5)

    def move(self):
        # collision detection with all the objects
        if (self.rect.bottom) >= wallDown.rect.top or (self.rect.y) <= wallUp.rect.bottom:
            self.dy = -self.dy

        if self.rect.colliderect(player1.rect) or self.rect.colliderect(player2.rect):
            self.dx = -self.dx
        
        
        #if self.rect.topright

        if self.rect.left <= 0 or self.rect.right >= winX:
            self.check = player2 if self.rect.left <= 0 else player1
            self.check.score += 1
            self.rect.center = (winX//2, winY//2)
            self.dx *= random.choice([-1,1])
            self.dy *= random.choice([-1,1])

        self.rect.x += self.dx
        self.rect.y += self.dy


    def update(self):
        pygame.draw.ellipse(screen, (78, 89, 35), self.rect)

# Placing the Ball
ball = Ball(500, 350)

class Button:
    def __init__(self, text):
        self.text = text
        self.font = pygame.font.SysFont('couriernew', 36)
    
    def draw(self):

        text_surface = self.font.render(self.text, True, white)
        text_width, text_height = text_surface.get_size()

        rect_left = (winX - text_width) // 2
        rect_top = (winY - text_height) // 2

        screen.blit(text_surface, (rect_left, rect_top))

        self.rect = pygame.Rect(rect_left - 10, rect_top - 10, text_width + 20, text_height + 20)
        pygame.draw.rect(screen, white, self.rect, width=2)

        if not started_once:
            display_text('Player 1', (100, 200), 33)

            display_text('w \n a', (130,  rect_top+200), 30)

            display_text('Player 2', (winX//2+200, 200), 33)

            display_text('↑ \n ↓', (winX//2+240,  rect_top+200), 30)

            display_text('CONTROLS',  (rect_left-10, rect_top+200), 25, True)
    
    #def controls(self):

# placing 'the start to play' button
play_btn = Button('start')

start = False
game_end = False
winner = None
max_score = 10 # setting the score to win

run=True

while run:

    if game_end:
        start = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_btn.rect.collidepoint(event.pos):
               start = True
               game_end = False
               player1.score = player2.score = 0
            

    screen.fill((26, 18, 18))
    wallUp.drop()
    wallDown.drop()

    player1.update(pygame.K_w, pygame.K_a, 200)
    player2.update(pygame.K_UP, pygame.K_DOWN, 800)

    if not start:
        play_btn.draw()
        if started_once and winner is not None:
            display_text(winner, (winX//2-150, winY//2-160), 40)
    else:
        started_once = True
        winner = None
        
        ball.move()
        ball.update()
    
        if winner is None and player1.score == max_score and player2.score < max_score:
            winner = 'Player 1 won'
        elif winner is None and player2.score == max_score and player1.score < max_score:
            winner = 'Player 2 won' 

        if winner is not None:
            game_end = True
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()