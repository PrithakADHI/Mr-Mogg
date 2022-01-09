import pygame, time, sys

pygame.init()
width = 1280
height = 672
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()

offset = [0, -482]

pygame.display.set_caption("GHOST GAME MUUAHAHAHHAHAHHA")

prev_time = time.time()
dt = 0

running = True

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50
        self.speedx = 300
        self.speedy = 500
        self.img = pygame.image.load("assets/player/1.png")
        self.imgarr = [ pygame.image.load("assets/player/1.png"), pygame.image.load("assets/player/2.png"), pygame.image.load("assets/player/3.png"), pygame.image.load("assets/player/4.png"), pygame.image.load("assets/player/5.png"), pygame.image.load("assets/player/6.png"), pygame.image.load("assets/player/7.png") ]
        self.hitbox = pygame.Rect(self.x + 13, self.y, self.w - 27, self.h)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def render(self, ori, no):
        img = pygame.transform.scale(self.imgarr[no], (self.w, self.h))
        if ori == "Left":
            img = pygame.transform.flip(img, True, False)

        #pygame.draw.rect(screen, (255,200,100), self.hitbox, 1)
        
        screen.blit(img, ( offset[0] +  self.hitbox.x - 13, offset[1] + self.hitbox.y, self.hitbox.w, self.hitbox.h))

    def move(self, dx, dy, colliders):
        if dx != 0:
            self.move_single_axis(dx, 0, colliders)
        if dy != 0:
            self.move_single_axis(0, dy, colliders)
    
    def move_single_axis(self, dx, dy, colliders):

        self.x += dx
        self.y += dy

        self.rect.x += dx
        self.rect.y += dy

        self.hitbox.x += dx
        self.hitbox.y += dy

        global isGrounded

        for wall in colliders:
            if self.hitbox.colliderect(wall.rect):
                if dx > 0:
                    #self.rect.right = wall.rect.left
                    self.hitbox.right = wall.rect.left
                if dx < 0:
                    #self.rect.left = wall.rect.right
                    self.hitbox.left = wall.rect.right
                
                if dy > 0:
                    #self.rect.bottom = wall.rect.top
                    self.hitbox.bottom = wall.rect.top
                    isGrounded = True
                if dy < 0:
                    #self.rect.top = wall.rect.bottom
                    self.hitbox.top = wall.rect.bottom
            else:
                isGrounded = False


class Object(object):
    def __init__(self, x, y, w, h, no):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.img = pygame.image.load("assets/blocks/" + str(no).strip() + ".png")

    def render(self):
        #Just for testingt
        #pygame.draw.rect(screen, (100,200,255), self.rect, 0)
        img = pygame.transform.scale(self.img, (self.w, self.h))
        screen.blit(img, (offset[0] + self.rect.x, offset[1] + self.rect.y, self.rect.w, self.rect.h) )

def background(dx):
    bg_img = pygame.image.load("assets/background/background.png")

    bg_img = pygame.transform.scale(bg_img, (width, height))
    screen.blit(bg_img, (0,0))

def displayText(txt, x, y):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(txt, True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (x // 2, y // 2)

    screen.blit(text, textRect)

def makeMap(fileName):
    global walls
    with open(fileName) as f:
        #w, h = [int(x) for x in next(f).split()]
        array = [[int(x) for x in line.split()] for line in f]

    for x in array:
        walls.append( Object( x[0], x[1], x[2], x[3], x[4] ) )

ori = "Left"
P = Player(50,500)
walls = []

jump = False
jump_i = 0

no = 0

isGrounded = False

dx = 0
dy = 0

makeMap("map.mp")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(offset)
            pygame.quit()
            sys.exit()

    
    now = time.time()
    dt = now - prev_time
    prev_time = now

    dy = 600 * dt

    k = pygame.key.get_pressed()

    if k[pygame.K_a] == False and k[pygame.K_d] == False:
        no = 0

    if k[pygame.K_ESCAPE]:
        print(offset)
        pygame.quit()
        sys.exit()
    
    if k[pygame.K_a]:
        ori = "Left"
        dx = (P.speedx * -1) * dt
        no += 13 * dt

    if k[pygame.K_d]:
        ori = "Right"
        dx = P.speedx * dt
        no += 13 * dt

    if k[pygame.K_SPACE] and not isGrounded:
        jump = True

    if jump:

        jump_i += 1

        if jump_i <= 23:
            dy = (P.speedy * -1) * dt
        
        if jump_i >= 23:
            dy = (P.speedy) * dt

        if jump_i >= (23+23):
            jump_i = 0
            jump = False



    if k[pygame.K_UP]:
        offset[1] -= 300 * dt
    if k[pygame.K_DOWN]:
        offset[1] += 300 * dt
    if k[pygame.K_LEFT]:
        offset[0] -= 300 * dt
    if k[pygame.K_RIGHT]:
        offset[0] += 300 * dt
    
    if offset[1] >= -482:
        offset[1] = -482

    #background(dx)

    if no > 6:
        no = 0

    m_no = round(no)

    if P.hitbox.x < 0:
        P.hitbox.x = 0

    if P.hitbox.x > 1280 - 23:
        P.hitbox.x = 1280 - 23

    P.render(ori, m_no)
    P.move(dx, dy, walls)

    for wall in walls:
        wall.render()

    dx, dy = 0, 0

    clock.tick(60)
    displayText( str(clock.get_fps()), 200, 100 )
    pygame.display.flip()
    screen.fill((230,230,230))