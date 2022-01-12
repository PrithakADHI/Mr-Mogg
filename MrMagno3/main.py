import pygame, time, sys, random, math, csv

pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN, vsync=True)
clock = pygame.time.Clock()

offset = [0, -482]

isGrounded = False
headBump = False

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
        self.speedy = 475
        
        self.oghealth = 200
        self.health = 200

        self.mana = 300
        self.ogmana = 300


        self.health_img = pygame.image.load("assets/player/healthbar_img.png")
        #self.img = pygame.image.load("assets/player/1.png")
        self.imgarr = [ pygame.image.load("assets/player/1.png").convert_alpha(), pygame.image.load("assets/player/2.png").convert_alpha(), pygame.image.load("assets/player/3.png").convert_alpha(), pygame.image.load("assets/player/4.png").convert_alpha(), pygame.image.load("assets/player/5.png").convert_alpha(), pygame.image.load("assets/player/6.png").convert_alpha(), pygame.image.load("assets/player/7.png").convert_alpha(), pygame.image.load("assets/player/8.png").convert_alpha() ]
        
        self.hitbox = pygame.Rect(self.x + 13, self.y, self.w - 27, self.h)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def render(self, ori, no):
        img = pygame.transform.scale(self.imgarr[no], (self.w, self.h))
        if ori == "Left":
            img = pygame.transform.flip(img, True, False)

        pygame.draw.rect(screen, (255,200,100), (offset[0] + self.hitbox.x, offset[1] + self.hitbox.y, self.hitbox.w, self.hitbox.h), 1)
        
        screen.blit(img, ( offset[0] +  self.hitbox.x - 13, offset[1] + self.hitbox.y, self.hitbox.w, self.hitbox.h))

    def render_health_bar(self):
        img = pygame.transform.scale(self.health_img, (100,100))
        screen.blit(img, (25,50))

        per = (self.health / self.oghealth) * 100

        pygame.draw.rect(screen, (255,255,255), (100, 87, 100, 15))
        pygame.draw.rect(screen, (255,100,140), (100, 87, per, 15))

        per2 = (self.mana / self.ogmana) * 100

        pygame.draw.rect(screen, (255,255,255), (100, 87+20, 100, 15))
        pygame.draw.rect(screen, (100,200,255), (100, 87+20, per2, 15))

        


    def move(self, dx, dy, colliders):
        self.move_single_axis(dx, 0, colliders)
        self.move_single_axis(0, dy, colliders)
    
    def move_single_axis(self, dx, dy, colliders):

        self.hitbox.x += dx
        self.hitbox.y += dy

        global isGrounded
        global headBump

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
                else:
                    isGrounded = False
                if dy < 0:
                    #self.rect.top = wall.rect.bottom
                    headBump = True
                    self.hitbox.top = wall.rect.bottom
                else:
                    headBump = False

class Object(object):
    def __init__(self, x, y, w, h, no):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.img = pygame.image.load("assets/blocks/" + str(no).strip() + ".png").convert_alpha()

    def render(self):
        #Just for testingt
        #pygame.draw.rect(screen, (100,200,255), self.rect, 0)
        img = pygame.transform.scale(self.img, (self.w, self.h))
        if is_colliding( offset[0] + self.rect.x - 100, offset[1] + self.rect.y + 25, -125, 0, 1280, 800 ):
            screen.blit(img, (offset[0] + self.rect.x, offset[1] + self.rect.y, self.rect.w, self.rect.h) )

class Enemy1(object):
    def __init__(self, x, y):
        self.hitbox = pygame.Rect(x, y, 22, 40)
        self.speedx = 300
        self.speedy = 400
        self.img_array = [ pygame.image.load("assets/enemies/e11.png").convert_alpha() ]
        self.dir = "Right"
    
    def render(self):
        #Just for testing
        pygame.draw.rect(screen, (255,100,100), (offset[0] + self.hitbox.x, offset[1] + self.hitbox.y, self.hitbox.w, self.hitbox.h), 3 )
        img = pygame.transform.scale(self.img_array[0], (50,50))
        if self.dir == "Left":
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, (offset[0] + self.hitbox.x - 18, offset[1] + self.hitbox.y - 10))

    def move(self, dx, dy, colliders, dt):
        self.move_single_axis(dx, 0, colliders, dt)
        self.move_single_axis(0, dy, colliders, dt)
    
    def move_single_axis(self, dx, dy, colliders, dt):

        self.hitbox.x += dx * dt
        self.hitbox.y += dy * dt

        if dx > 0:
            self.dir = "Right"
        if dx < 0:
            self.dir = "Left"

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
                if dy < 0:
                    #self.rect.top = wall.rect.bottom
                    self.hitbox.top = wall.rect.bottom
    
    def follow_player(self, player, dt):
        pygame.draw.rect( screen, (255,100,100), (offset[0] + self.hitbox.x - 300, offset[1] + self.hitbox.y - 300, 600, 600), 1 )
        if player.hitbox.colliderect( pygame.Rect( self.hitbox.x - 300, self.hitbox.y - 300, 600, 600 ) ):
            dx, dy = player.hitbox.x - self.hitbox.x, player.hitbox.y - self.hitbox.y
            dist = math.hypot(dx, dy)
            if dist != 0: 
                dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            #self.rect.x += dx * self.speed
            #self.rect.y += dy * self.speed

            self.move(dx * self.speedx * 1.05, 0, walls, dt)

            #self.speedx = dx*self.speedx
            #self.speedy = dy*self.speedy

class particles():
    def __init__(self, pos, vel, timer, col):
        self.pos = pos
        self.vel = vel
        self.timer = timer
        self.col = col

def displayText(txt, x, y, font_size=16):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(txt, True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (x,y)

    screen.blit(text, textRect)

def makeMap(fileName):
    global walls
    with open(fileName) as f:
        #w, h = [int(x) for x in next(f).split()]
        array = [[int(x) for x in line.split()] for line in f]

    for x in array:
        walls.append( Object( x[0], x[1], x[2], x[3], x[4] ) )

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def is_colliding(x, y, x1, y1, w, h):
    if x >= x1 and y >= y1 and x <= x1 + w and y <= y1 + h:
        return True

def game_over():
    screen.fill((255,255,255))
    displayText("GAME OVER!!!!", width//2, height//2, 32)
    
    pygame.display.update()
    time.sleep(1)
    sys.exit()

ori = "Left"
P = Player(offset[0] + 274,offset[1] + 1502)

E_List = [Enemy1(1200,718)]

walls = []

particle_array = []

mana_array = []

background_objects = [  [0.015, [1000,530,400,1000]], [0.015, [480, 430, 400, 1000]], [0.025, [120,100,400,900]], [0.05, [30,40,400, 800]]]

jump = False
jump_i = 0

fly = False

no = 0

dx = 0
dy = 0

acc = 0
y_change = 0

angle = 0
faceMouse = False
dJump = False

makeMap("map.mp")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(offset)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump = True
                isGrounded = False

    for background_object in background_objects:
        obj_rect = pygame.Rect( background_object[1][0] + offset[0] * background_object[0], background_object[1][1] + offset[1] * background_object[0], background_object[1][2], background_object[1][3] )
        if background_object[0] == 0.05:
            pygame.draw.rect(screen, (200,200,200), obj_rect)
        elif background_object[0] == 0.025:
            pygame.draw.rect(screen, (150,150,150), obj_rect)
        elif background_object[0] == 0.015:
            pygame.draw.rect(screen, (100,100,100), obj_rect)

    now = time.time()
    dt = now - prev_time
    prev_time = now

    dy = 600 * dt
    edy = 600 * dt

    for particle in particle_array:
        particle.pos[0] += particle.vel[0]
        particle.pos[1] += particle.vel[1] 
        particle.timer -= (1/20)

        draw_circle_alpha(screen, (particle.col[0], particle.col[1], particle.col[2], 100), ( offset[0] + particle.pos[0], offset[1] + particle.pos[1] ), particle.timer * 2)
        pygame.draw.circle(screen, (255,255,255), ( offset[0] + particle.pos[0], offset[1] + particle.pos[1] ), particle.timer)
    
        if particle.timer <= 0:
            particle_array.remove(particle)

    k = pygame.key.get_pressed()

    mx, my = pygame.mouse.get_pos()

    if k[pygame.K_a] == False and k[pygame.K_d] == False:
        no = 0

    if k[pygame.K_j]:
        P.mana = 300

    if k[pygame.K_w] and P.mana > 0:
        P.mana -= 50 * dt
        fly = True
        isGrounded = False
        dy = (P.speedy / 2 * -1) * dt
        particle_array.append( particles( [P.hitbox.x + 10, P.hitbox.y + 50], [random.randint(0,20) / 10 -1, 5], random.randint(7, 10) , [100,200,255] ))

    if k[pygame.K_ESCAPE]:
        print(offset)
        pygame.quit()
        sys.exit()
    
    if k[pygame.K_a]:
        ori = "Left"
        dx = (P.speedx * -1) * dt
        if fly == False:
            no += 13 * dt
        if isGrounded:
            particle_array.append( particles([ P.hitbox.x + 10, P.hitbox.y + 50], [random.randint(0,20) / 10 - 1, 0.25], random.randint(2,6), [128,128,128] ))

    if k[pygame.K_d]:
        ori = "Right"
        dx = P.speedx * dt
        if fly == False:
            no += 13 * dt
        if isGrounded:
            particle_array.append( particles([ P.hitbox.x + 10, P.hitbox.y + 50], [random.randint(0,20) / 10 - 1, 0.25], random.randint(2,6), [128,128,128] ))

    if isGrounded == False:
        no = 1

    if isGrounded == True:
        fly = False

    if jump:
        jump_i += 60 * dt

        if headBump:
            jump_i = 0
            jump = False

        if not fly:
            if jump_i <= 20:
                dy = (P.speedy * -1) * dt
            
            if jump_i >= 20:
                dy = (P.speedy) * dt

        if jump_i >= (20+20):
            jump_i = 0
            jump = False
            dJump = False


    if P.hitbox.x >= 1110:
        offset[0] -= 1000 * dt

    if P.hitbox.x < 1110:
        offset[0] += 1000 * dt

    if P.hitbox.y <= 500 and jump == False:
        offset[1] += 1000 * dt

    if P.hitbox.y >= 500:
        offset[1] -= 1000 * dt

    if offset[0] <= -100 * 10.67:
        offset[0] = -100 * 10.67

    if offset[0] >= 0:
        offset[0] = 0

    if offset[1] <= -40 *(450/40):
        offset[1] = -40 *(450/40)

    if offset[1] >= 0:
        offset[1] = 0

    if P.hitbox.y < 0:
        P.hitbox.y = 0
        headBump = True
    else:
        headBump = False

    if no > 6:
        no = 0

    m_no = round(no)

    if P.hitbox.x < 0:
        P.hitbox.x = 0

    if P.hitbox.x > 2320:
        P.hitbox.x = 2320
    
    P.render(ori, m_no)
    P.move(dx, dy, walls)
    for E in E_List:
        E.render()
        E.follow_player(P, dt)
        E.move(0, E.speedy, walls, dt)

        if E.hitbox.colliderect( P.hitbox ):
            game_over()

    faceMouse = False

    for wall in walls:
        wall.render()

    dx, dy = 0, 0

    P.render_health_bar()

    clock.tick(60)
    displayText( str(clock.get_fps()), 200, 100 )
    displayText( str(P.hitbox.x) + " " + str(P.hitbox.y), 200, 50)
    #displayText( str(offset[0]) + " " + str(offset[1]), 200, 100 )
    #displayText( str(isGrounded), 200, 150 )
    pygame.display.flip()
    screen.fill((127,127,127))


