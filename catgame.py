# 1 - Import library
import pygame
import random
import time
from pygame.locals import (RLEACCEL, K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,KEYDOWN,QUIT,K_c,K_q,K_s,K_SPACE, K_p)

# 2 - Initialize the game
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#name the game window 
pygame.display.set_caption("Catch the mouse and avoid the dogs!")

#define position
#center = (255, 174)

#Define Colors - RGB
black = (0,0,0,1)
white = (255,255,255)
green = (34,177,76)
red = (255,0,0)
blue = (38,110,193)

#define font name'
font_name = pygame.font.match_font('helvetica')

#defines how to draw text to use for score counter
def draw_text(surf, text, size, x, y):
    #sets font type and size
    font = pygame.font.Font(font_name, size)
    #sets text, anti-aliased and colour
    text_surface = font.render(text, True, (0, 0, 0))
    #creates text box
    text_rect = text_surface.get_rect()
    #sets position of text box
    text_rect.midtop = (x , y)
    #push to screen display
    surf.blit(text_surface, text_rect) 

# set clock for framerate
clock = pygame.time.Clock()

# Set positions of graphics
#background_position = [0, 0]

#background image
#background = pygame.image.load("background.png")

#define pause
def pause():
    paused = True
    while paused:
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        screen.fill(background, 1)
        draw_text(screen, "Paused", 50, 400, 300)
        draw_text(screen, "Press P to continue or Q to quit", 35, 400, 300)
        pygame.display.update()
        clock.tick(5)        

#define score
def score(message):
    draw_text(screen, "Score: ", 25, 600, 50)
    draw_text(screen, str(score), 40, 65, 525)

#define lives
def lives(message):
    draw_text(screen, "Lives: ", 25, 600, 25)
    draw_text(screen, str(lives), 40, 65, 525)

#set the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("cat2.png").convert()
        self.surf.set_colorkey((white), RLEACCEL)
        self.rect = self.surf.get_rect()

    #set movement control
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

    #keep player in screen on green field
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 125:
            self.rect.top = 125
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#define dog class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("dog.PNG").convert()
        self.surf.set_colorkey((white), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(170, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(3, 5)
    # move enemy based on speed, but remove it when it passes the left edge of the screen.
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        #if pygame.sprite.spritecollideany(player, enemy):
        if pygame.sprite.spritecollideany(player, enemies):
            global lives
            lives -= 1
            self.kill()

#define mouse class (power up)
class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super(Mouse, self).__init__()
        self.surf = pygame.image.load("mouse.png").convert()
        self.surf.set_colorkey((white), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(170, SCREEN_HEIGHT),
            )
        )
    # Move the mouse based on a constant speed, but remove it when it passes the left edge of the screen.
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        #if pygame.sprite.spritecollideany(player, mouse):
        if pygame.sprite.spritecollideany(player, mouse):
            global score
            score += 1
            self.kill()

# Create custom events for adding a new dog and mouse
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 420)
ADDMOUSE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDMOUSE, 450)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, mouse sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for collision detection - score up and position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
mouse = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
        #if player presses the x in the top right of the pygame window or quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                #quit
            if event.type == pygame.KEYDOWN:
                #if player press c stop intro and run game loop
                if event.key == K_SPACE:
                    intro = False
                    # gameLoop()
                #if player press Q quit pygame window
                if event.key == pygame.K_q:
                    game_over()
                    pygame.quit()
                    #quit
        #sets background
        #screen.fill(green)
        screen.blit(background, (0,0))

        #sets text
        draw_text(screen, "Let's catch the mouses!", 50, 400, 200)
        draw_text(screen, "Control the cat with your keyboard.", 30, 400, 300)
        draw_text(screen, "Collect as many mouses as possible while avoid dogs!", 30, 400, 400)
        draw_text(screen, "Press SPACE to start or Q to quit!", 25, 400, 500)
        #updates screen display
        pygame.display.update()
        #clock.tick(15)

def game_over():
    gameOver = True
    while gameOver:
        for event in pygame.event.get():
        #if player presses the x in the top right of the pygame window or quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                #quit
                #break

            if event.type == pygame.KEYDOWN:
                #if player press s to start game loop
                if event.key == pygame.K_SPACE:
                    gameOver = False
                    game_intro()
                #if player press Q quit pygame window
                if event.key == pygame.K_q:
                    pygame.quit()
                    #quit

        #sets background
        screen.blit(background, (0,0))
        #screen.fill(green)
        #sets text
        draw_text(screen, "Game Over!", 50, 400, 200)
        draw_text(screen, "Final Score: " + str(score), 50, 400, 300)
        draw_text(screen, "Press SPACE to restart or q to exit!", 35, 400, 400)
        #updates screen display
        pygame.display.update()
        #clock.tick(15)

background = pygame.image.load("background.png")

# Setup for sounds
pygame.mixer.init()
# Sound source: http://www.orangefreesounds.com/analog-dream-electronic-downtempo-music/
pygame.mixer.music.load("background_music.mp3")
#loops music
pygame.mixer.music.play(loops=-1)
#game end sound: http://soundbible.com/1687-TomCat.html
exit_sound = pygame.mixer.Sound("catEnd.ogg")
#purr: http://soundbible.com/1002-Purring.html
#happy_sound = pygame.mixer.Sound("purr.ogg")
# Set the base volume for all sounds
#happy_sound.set_volume(3)
exit_sound.set_volume(5)

#def redrawGameWindow():
    #screen.blit(background, (0,0))
    #font = pygame.font.SysFont("helvetica", 30, True)
    #text = font.render("Score: " + str(score), 1, (black))
    #screen.blit(text, (610, 10))
    
    #pygame.display.update()

#define gameloop
def gameLoop():
    score = 0
    lives = 3
     
    running = True
    while running:
        for event in pygame.event.get():
        # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    #print("Final Score: " + str(score))
                    game_over()
                    running = False
                if event.key == pygame.K_q:
                    #print("Final Score: " + str(score))
                    game_over()
                    running = False
                if event.key == pygame.K_p:
                    pause()
            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                game_over()
                #print("Final Score: " + str(score))
                running = False

            # Should we add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy, and add it to our sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            # Should we add a new mouse?
            elif event.type == ADDMOUSE:
                # Create the new MOUSE, and add it to our sprite groups
                new_mouse = Mouse()
                mouse.add(new_mouse)
                all_sprites.add(new_mouse)
            #elif lives == 0
                #game_over()
    
    
    # Refresh background and score:
    #redrawGameWindow()

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies and mouse
    enemies.update()
    mouse.update()

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # check remaining lives
        lives -= 1
        print("Lives remained: " + str(lives))
        running = True


    elif pygame.sprite.spritecollideany(player, mouse):
        # If so, play happy purr:
        #happy_sound.play()

        #Continue the loop
        running = True 

    # 60 frames per second rate
    clock.tick(60)

    # Flip everything to the display
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # 60 frames per second rate
    #clock.tick(60)

    #close pygame
    pygame.quit()


game_intro()
gameLoop()
