import pygame,sys,random
pygame.init()
pygame.key.set_repeat(1, 100)

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Space Invaders')
font = pygame.font.SysFont("Comic Sans",50)

black = [0, 0, 0]
white = [255, 255, 255]
green = [0, 255, 0]
red = [255,0,0]
orange = [255,69,0]
Player = pygame.image.load("ship.png")
Playerrect = Player.get_rect()
Playerrect.left = (width * 0.48)
Playerrect.top = (height * 0.9)

alien1 = pygame.image.load("aliens.png")
aliens = []
score = 0
lives = 3

gameover = False
renderedText2 = font.render("Game Over!",1,orange)
renderedText3 = font.render("Press Q to Quit, or R to Restart",1,orange)
def addAliens():
    for row in range(0,5):
        for col in range(0,11):
            alien = pygame.Rect(10+col*40,10+row*40,25,25)
            aliens.append(alien)
addAliens()
##alien = pygame.Rect(10,10,25,25)
alienSpeed = 1
bullets = []
bombs = []
shelters = []

def addShelters():
    siz = 10
    sep = 150
    lft = (width-3*sep-6*siz)/2   # center the shelters on the screen
    for row in range(0,4):
        for col in range(0,6):
            for num in range(0,4):
                bit=pygame.Rect(lft+sep*num+col*siz,height-100-row*siz,siz,siz)
                if row==3 and (col==0 or col==5):
                    bit.top = bit.top+40
                shelters.append(bit)
addShelters()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if event.key == pygame.K_SPACE:
                bullets.append([Playerrect.centerx,Playerrect.top])
            if keys[pygame.K_LEFT]:
                Playerrect.right = Playerrect.right - 5
            if keys[pygame.K_RIGHT]:
                Playerrect.right = Playerrect.right + 5
                            ## r to restart and q to quit

            if gameover:
                if keys[pygame.K_r]:
                    gameover=False
                    lives = 3
                    score = 0
                    aliens = []
                    addAliens()
                    shelters = []
                    addShelters()
                    bombs = []
                    bullets = []
                    

                if keys[pygame.K_q]:
                    pygame.quit()
                    sys.exit()


    # find the smallest left and the largest right in the set
    minleft=width
    maxright=0
    for alien in aliens:
        if alien.left<minleft:
            minleft=alien.left
        if alien.right>maxright:
            maxright=alien.right

# If the leftmost or rightmost alien hits the border:
    if maxright>width-5 or minleft<5:
            # Reverse direction:
        alienSpeed=-alienSpeed
            # Move every alien down:
        for alien in aliens:
            alien.top = alien.top + 20
            if alien.bottom>Playerrect.top:
                lives = 0
                gameover = True
                
                    
        # move them left or right
    for alien in aliens:
        alien.left = alien.left + alienSpeed
        # drop bombs
        if random.randint(0,600)==0:
            bombs.append([alien.centerx,alien.bottom])

    for bullet in bullets:
        bullet[1] = bullet[1] - 3
        if bullet[1]<0:
            bullets.remove(bullet)
##
    for bomb in bombs:
        bomb[1] = bomb[1] + 3
        if bomb[1]<0:
            bombs.remove(bomb)

            #### Check if bullets hit aliens ####
    

    for bullet in bullets:
        for alien in aliens:
            if alien.collidepoint(bullet):
                aliens.remove(alien)
                bullets.remove(bullet)
                score = score + 20
                break
        for shelter in shelters:
            if shelter.collidepoint(bullet):
                shelters.remove(shelter)
                bullets.remove(bullet)
                #### Check if bombs hit player ####
    for bomb in bombs:
        if Playerrect.collidepoint(bomb):
            bombs.remove(bomb)
            lives = lives - 1
            break
        for shelter in shelters:
            if shelter.collidepoint(bomb):
                shelters.remove(shelter)
                bombs.remove(bomb)

    if lives == 0:
        gameover = True
        
                
    if len(aliens)==0:
        addAliens()
        alienSpeed=alienSpeed + 2
        if random.randint(0,400)==0:
            bombs.append([alien.centerx,alien.bottom])

    
    screen.fill(black)
    # draw your game elements here:
    screen.blit(Player,Playerrect)
    if gameover:
        screen.blit(renderedText2,(300,height/2-150))
        screen.blit(renderedText3, (100,height/2))
##    pygame.draw.rect(screen,white,Player,0)
    for shelter in shelters:
        pygame.draw.rect(screen,green,shelter,0)
    for alien in aliens:
        screen.blit(alien1,alien)
    for bullet in bullets:
        pygame.draw.circle(screen,green,bullet,5,0)
    for bomb in bombs:
        pygame.draw.circle(screen,red,bomb,5,0)
    
    renderedText = font.render("Score: "+str(score),1,orange)
   
    renderedText4 = font.render("Lives:"+str(lives),1,orange)
    screen.blit(renderedText, (width/2-175,10))
    screen.blit(renderedText4,(width/2+100,10))

    pygame.display.flip()
    pygame.time.wait(10)
