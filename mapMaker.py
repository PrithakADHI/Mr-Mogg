import pygame, pandas, sys

pygame.init()
screen = pygame.display.set_mode((1280,1280), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

def displayText(txt, x, y):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(txt, True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (x // 2, y // 2)

    screen.blit(text, textRect)

def make_grid(x, y, mx, my, mb, no):
    for i in range(x):
        for j in range(y):

            pygame.draw.rect(screen, (50, 255, 100), (i * 32, j * 32, 32, 32), 1)

            if is_colliding(mx, my, i * 32, j * 32, 32, 32):
                displayText(str(i) + " " + str(j), 100, 100)
                displayText( str(i * 32) + " " + str(j * 32) + " 32 32" , 200, 300)
            
            if is_colliding(mx, my, i*32, j*32, 32, 32) and mb:
                global map, map2
                map.append( str(i*32) + " " + str(j*32) + " 32 32 " + str(no).strip() + "\n"  )
                map = pandas.Series(map).drop_duplicates().tolist()
                map2.append( [i*32, j*32, 32, 32, no] )
                map2 = pandas.Series(map2).drop_duplicates().tolist()

def is_colliding(x, y, x1, y1, w, h):
    if x >= x1 and y >= y1 and x <= x1 + w and y <= y1 + h:
        return True

def makeMap( map ):
    for i in map:
        img = pygame.image.load("assets/blocks/" + str(i[4]).strip() + ".png")
        screen.blit(img, ( i[0], i[1] ))

map = []
map2 = []
clicked = False
no = 1



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(map)
            if map != []:
                f = open("map.mp", "w")
                f.writelines(map)
                f.close()
            pygame.quit()
            sys.exit()

    mx, my = pygame.mouse.get_pos() 
    clicked = pygame.mouse.get_pressed()

    makeMap(map2)

    k = pygame.key.get_pressed()

    if k[pygame.K_q]:
        no = 1
    if k[pygame.K_w]:
        no = 2
    if k[pygame.K_e]:
        no = 3
    if k[pygame.K_r]:
        no = 4
    if k[pygame.K_t]:
        no = 5
    if k[pygame.K_y]:
        no = 6
    
    if k[pygame.K_ESCAPE]:
        if map != []:
            f = open("map.mp", "w")
            f.writelines(map)
            f.close()
        pygame.quit()
        sys.exit()

    make_grid(60,40, mx, my, clicked[0], no)
    clicked = False

    displayText( str(no), 100, 400 )

    clock.tick(60)
    pygame.display.flip()
    screen.fill((255,255,255))