# Load dependencies
import pygame
from pygame.locals import *
from sys import exit
import random
import csv
from pathlib import Path
from itertools import repeat

# Constants
PLAYER_COLOR = (199, 208, 215)
ENEMY_COLOR = (101, 120, 137)
TEXT_COLOR = (255, 240, 230)
SHIELD_POWERUP_COLOR = (80, 200, 237)
SHIELD_COLOR = (85, 134, 150)
BUTTON_COLOR = (101, 120, 137)
BUTTON_COLOR_SELECTED = (66, 78, 88)
AMMO_COLOR = (255, 249, 139)
AMMO_POWERUP_COLOR = (255, 219, 105)

BACKGROUND_COLOR = (79, 91, 103)
FONT_COLOR = (242, 242, 242)
WINDOW_SIZE = (320, 540)

# Initiate Pygame
pygame.init()

# Pygame Base Stuff
clock = pygame.time.Clock()
pygame.mixer.init()

pygame.display.set_caption("Meteora")
pygame.mouse.set_visible(False)

vec = pygame.math.Vector2 # player

# Initialize Surfaces
main_screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
screen = main_screen.copy() 

sfx_data = []
music_data = []

# Load resources
if Path("resources/Pixelar_Regular.ttf").exists():
    font = pygame.font.Font("resources/Pixelar_Regular.ttf", 26)
    print("Pixelar Font found")
else:
    print("ERROR: Pixelar Font not found. Switching to alternative")
    font = pygame.font.SysFont(None, 26)

if Path("resources/icon.png").exists():
    icon = pygame.image.load("resources/icon.png")
    pygame.display.set_icon(icon)
else:
    print("ERROR: Resources missing: icon.png")
    exit()

# Load Music
music_theme = "resources/music_theme.wav"
music_game = "resources/music_game.wav"
music_gameover = "resources/music_sad.wav"
sfx_explosion = "resources/e1.wav"
sfx_shield = "resources/e3.wav"
sfx_shoot = "resources/d6.wav"

# //// Fade Screen ////////////////////////////////////////////////////////////////////////////////////////////////////////
def fade(size, surface, fade_color=(0,0,0), delay=5):
    fade_surface = pygame.Surface(size)
    fade_surface.fill(fade_color)
    for alpha in range(300):
        fade_surface.set_alpha(alpha)
        redrawWindow(surface)
        surface.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(delay)
    
def library(target_list, *args):
    for i in args:
        target_list.append(pygame.mixer.Sound(i))

def set_all_vol(sounds, mult=100-1):
    for sound in sounds:
        vol = sound.get_volume()
        sound.set_volume(min(vol*mult, 1.0))

# Generate library
library(sfx_data, sfx_explosion, sfx_shield, sfx_shoot)
library(music_data, music_theme, music_game, music_gameover)

# From StackOverflow 
def screenshake():
    shk = -1
    for i in range(0, random.randint(3, 5)):
        for x in range(0, 20, random.randint(6, 10)):
            yield (x * shk, 0)
        for x in range(20, 0, random.randint(6, 10)):
            yield (x * shk, 0)
    while True:
        yield (0, 0)

def redrawWindow(surface, fill=BACKGROUND_COLOR):
    surface.fill(fill)
    # for flickering update here :)

# //// Button //////////////////////////////////////////////////////////////////////////////////////////////////////////
class Button:
    def __init__(self, width, height, x_pos, y_pos, text="", _color=(0, 0, 0), text_color=(40, 40, 40)):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = _color
        self.text = text
        self.text_color = text_color

        self.rect = pygame.rect.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.tx, self.ty = font.size(self.text)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(font.render(self.text, 0, self.text_color),
                    (self.x_pos + int(self.width / 2) - int(self.tx / 2), self.y_pos + int(self.height / 2) - int(self.ty / 2) ))
    def set_color(self, _color):
        self.color = _color

# //// Slider //////////////////////////////////////////////////////////////////////////////////////////////////////////
# Note: Some pieces of this code is from AustL's Pygame Widgets module
class Slider:
        def __init__(self, x_pos, y_pos, width, value=0, min_value=0, max_value=99, step=1, height=5, slider_width=10, slider_height=10, bar_color=(200, 200, 200), slider_color=(100, 23, 44)):
            
            # Position of slider and bar on screen
            self.x_pos = x_pos
            self.y_pos = y_pos

            # Bar Dimensions
            self.bar_width = width
            self.bar_height = height

            # Slider Dimensions
            self.slider_width = slider_width
            self.slider_height = slider_height

            # Colors
            self.bar_color = bar_color
            self.slider_color = slider_color

            # Values
            self.min_value = min_value
            self.max_value = max_value
            self.value = value # Start value, also controls slider position in relation of the bar that "holds" it
            self.step = step
            self.hit = False # Checks if is pressed
            
            # Rects
            self.bar_rect = pygame.rect.Rect(self.x_pos, self.y_pos, self.bar_width, self.bar_height)
            self.slider_rect = pygame.rect.Rect(self.x_pos+value, self.y_pos - int(self.bar_height / 2), self.slider_width, self.slider_height)


        def draw(self, surface):
            self.slider_rect.x = self.x_pos + self.value
            pygame.draw.rect(surface, self.bar_color, self.bar_rect)
            pygame.draw.rect(surface, self.slider_color, self.slider_rect)
            

        def get_input(self, event):
            is_pressed = pygame.mouse.get_pressed()[0] # Mousedown
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[0]:

                if self.bar_rect.collidepoint(mouse_x, mouse_y):
                    self.hit = True

                if self.hit:
                    self.value = self.round_value( (mouse_x - self.x_pos) / self.bar_width * self.max_value + self.min_value )
                    self.value = max(min(self.value, self.max_value), self.min_value)
            else:
                self.hit = False

        def cotains(self, x, y):
            x_range = 0

        def round_value(self, value):
            return self.step * round(value/self.step)

        def set_bar_color(self, _color):
            self.bar.fill(color)

        def set_slider_color(self, _color):
            self.slider.fill(color)
        
        def get_value(self):
            return self.value

# ///// Bullet //////////////////////////////////////////////////////////////////////////////////////////
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.width = 10
        self.height = 20

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(AMMO_COLOR)
        self.rect = self.image.get_rect()

        # Start Position     
        self.rect.center = (int(x), int(y))

        self.pos = vec(int(x), int(y))
        self.acc = vec(0, 0)
        self.vel_ = vec(0, 0)
        self.fric = 0.1
        self.vel = 0
        
    def draw(self, surface):
        pygame.draw.rect(surface, AMMO_COLOR, self.rect)

    def update(self):
        self.acc.y = -10

        self.acc += self.vel_ * self.fric
        self.vel_ += self.acc
        self.pos += self.vel_ + 1.2 * self.acc

        self.rect.center = self.pos
        if abs(self.pos[1])  > WINDOW_SIZE[1]:
            self.kill()

# ///// Player (Single Object) //////////////////////////////////////////////////////////////////////////////////////////
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.width = 30
        self.height = 30

        self.color = PLAYER_COLOR

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.max_vel = 5.0
        self.fric = -0.1

        # Shield 
        self.has_shield = False

        # bullets, you start with none
        self.ammo = 0
        self.max_ammo = 3

        # bullet delay
        self.shot_counter = 300

        # last shot
        self.last_shot = pygame.time.get_ticks()        

        # self.rect = pygame.rect.Rect((WINDOW_SIZE[0], WINDOW_SIZE[1], self.width, self.height))
        self.rect.center = (int(WINDOW_SIZE[0]/2), int(WINDOW_SIZE[1]-20))
        self.pos = vec(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]-20)
        self.acc = vec(0, 0)
        self.vel_ = vec(0, 0)

        self.vel = 0

        self.is_hit = False # Is the player being hit?

    def draw(self, state, surface):
        pygame.draw.rect(surface, self.color, self.rect) if state is True else None

    def key_manager(self):

        key = pygame.key.get_pressed()

        self.acc = vec(0, 0)
        if key[pygame.K_LEFT]:
            self.acc.x = -0.5
        if key[pygame.K_RIGHT]:
            self.acc.x = 0.5

        self.acc += self.vel_ * self.fric
        self.vel_ += self.acc
        self.pos += self.vel_ + 0.5 * self.acc

        self.rect.center = int(self.pos[0]), int(self.pos[1])

    def shoot(self, group):
        print(self.ammo)
        if self.ammo > 0 and not self.is_hit:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            group.add(bullet)
            self.set_ammo(-1)
        
    def update(self):
        if self.pos[0] - self.width/3 > WINDOW_SIZE[0]:
            self.pos[0] = 0
        if self.pos[0] + self.width/3 < 0:
            self.pos[0] = WINDOW_SIZE[0]

        if self.ammo > self.max_ammo: 
            self.ammo = self.max_ammo
    
    def set_color(self, _color):
        self.color = _color
    
    def set_ammo(self, amount):
        self.ammo += amount
    
    def get_ammo(self):
        return self.ammo
    
    def get_shield(self):
        return self.has_shield
    
    def set_shield(self, boolean_state):
        self.has_shield = boolean_state

# ///// Enemy (Single Object) //////////////////////////////////////////////////////////////////////////////////////////
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.width = 30
        self.height = 30

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(WINDOW_SIZE[0] - self.rect.width)
        self.rect.y = random.randrange(-220, -40)
        self.vy = random.randrange(2, 8)

        self.is_hit = False # Is the enemy hit (for bullet)

        # self.has_collided_with_screen = False
        self.has_counted = False

    def move(self):
        self.rect.move_ip(0, self.vy)

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect)

    def update(self, score_object, player_object):
        self.rect.y += self.vy
        
        if self.rect.top > WINDOW_SIZE[1] + 12:
            self.rect.x = random.randrange(WINDOW_SIZE[0] - self.rect.width)
            self.rect.y = random.randrange(-240, -40)
            self.vy = random.randrange(2, 12)
            self.has_counted = False

        if self.rect.top > WINDOW_SIZE[1]:
            if not self.has_counted:
                if player_object.is_hit == False:
                    score_object.set_score(1)
                    self.has_counted = True
    
        if player_object.is_hit: 
            if self.rect.bottom <= 0:
                self.has_counted = False


    def spawn(self, quantity, group):
        for i in range(quantity):
            grunt = Enemy()
            group.add(grunt)

# ///// Special Effects ////////////////////////////////////////////////////////////////////////////////////////////////
class Special_Effects:
    def __init__(self):
        self.particle_list = []
        
    def particle(self, x, y, x_velocity, y_velocity, timeout, cycle, particle_color=PLAYER_COLOR, trigger=False):
        timeout = abs(timeout)
        x_velocity = abs(x_velocity)
        y_velocity = abs(y_velocity)

        if trigger == True:
            for i in range(cycle):
                self.particle_list.append([[x, y], [random.randint(0, 40) / 10 -2, random.randint(0, 40) / 10 -2], random.randint(4, 7)])

        for i in self.particle_list:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= timeout
            i[1][0] +=  random.uniform(-x_velocity, x_velocity)
            i[1][1] +=  random.uniform(-y_velocity, y_velocity)
            pygame.draw.circle(screen, particle_color, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                self.particle_list.remove(i)

# ///// Powerup ////////////////////////////////////////////////////////////////////////////////////////////////////////
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Powerup class can acts as three different powerups:
        # Shield and Ammo

        self.width = 30
        self.height = 30

        self.image = pygame.Surface((self.width, self.height))
        
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(WINDOW_SIZE[0] - self.rect.width)
        self.rect.y = random.randrange(-220, -40)

        self.vy = random.randrange(3, 6)

        self.type = random.choice(['shield', 'ammo'])
        if self.type == "ammo":
            self.type_ammo()
        elif self.type == "shield":
            self.type_shield()

    def type_shield(self):
        self.width = 20
        self.height = 20
        self.image.fill(SHIELD_COLOR)
        
    def type_ammo(self):
        self.width = 15
        self.height = 20
        self.image.fill(AMMO_COLOR)
    
    # Yes, I took this from the enemy class, shut up
    def update(self, score_object, player_object):
        self.rect.y += self.vy
        if self.rect.top > WINDOW_SIZE[1] + 12:
            self.rect.x = random.randrange(WINDOW_SIZE[0] - self.rect.width)
            # self.rect.y = random.randrange(-240, -40)
            self.vy = random.randrange(2, 12)
        
        if self.rect.colliderect(player_object.rect):
            if self.type == "shield":
                player_object.has_shield = True
            if self.type == "ammo":
                player_object.set_ammo(1)
            self.kill()

        if self.rect.top > WINDOW_SIZE[1]:
            self.kill()

    def spawn(self, quantity, group):
        probability = 54 # percentage of a powerup to appear in current moment

        for i in range(quantity):
            powerup = Powerup()
            group.add(powerup)

# Score ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class Score:
    def __init__(self):
        self.score = 0

        self.highscore = ""

        if Path("resources/.highscore.csv").exists():
            print("File exist, reading file")
            with open('resources/.highscore.csv', 'r') as score_file:
                self.highscore = list(csv.reader(score_file))                
                score_file.close()

        else:
            print("ERROR, file does not exist, generating one")
            with open('resources/.highscore.csv', "w+") as score_file:
                writer = csv.writer(score_file)
                writer.writerow("0")
                self.highscore = ["0"] 
                score_file.close()

    def get_highscore(self):
        return  int("".join(self.highscore[0])) # Make whatever the fuck this is, thing?

    def get_score(self):
        return self.score

    def set_score(self, amount):
        self.score += amount

    def set_highscore(self, new_score):
        with open('resources/.highscore.csv', "w+") as score_file:
            writer = csv.writer(score_file)
            writer.writerow([new_score])
            score_file.close()

# Options Loop /////////////////////////////////////////////////////////////////////////////////////////////////////////
def options():
    is_clicking = False
    running = True

    pointer_particle = Special_Effects()

    main_menu = Button(140, 40, 90, 450, "Back to Menu", ENEMY_COLOR, FONT_COLOR)
    music_slider = Slider(190, 75, 100, 10)
    sfx_slider = Slider(190, 115, 100, pygame.mixer.music.get_volume()*100-1)

    particle_effects = []

    while running:
        pygame.mixer.music.set_volume(sfx_slider.get_value()/100)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if main_menu.rect.collidepoint(mouse_x, mouse_y):
            if is_clicking:
                running = False

        is_clicking = False
        screen.fill(BACKGROUND_COLOR)
        
        get_events = pygame.event.get()
        for event in get_events:
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_clicking = True
        
        # Particle Blast
        pointer_particle.particle(mouse_x, mouse_y, 0.2, 0, 0.03, 100, trigger=is_clicking)

        # Particle emiting
        particle_effects.append([ [mouse_x, mouse_y], [random.randint(10, 20) / 10 -2, random.randint(10, 20) / 10 -2], random.randint(2, 5)])

        screen.blit(font.render("Options", 0, (255, 240, 230)), (120, 20))
        screen.blit(font.render("Music", 0, (255, 240, 230)), (40, 70))
        screen.blit(font.render("Sound Effects", 0, (255, 240, 230)), (40, 110))

        main_menu.draw(screen)

        music_slider.draw(screen)
        sfx_slider.draw(screen)

        music_slider.get_input(get_events)
        sfx_slider.get_input(get_events)

        for i in particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.04
            i[1][0] +=  random.uniform(-0.4, 0.4)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                particle_effects.remove(i)

        main_screen.blit(screen, (0,0))
        pygame.display.update()
        clock.tick(30)

# Menu Loop ////////////////////////////////////////////////////////////////////////////////////////////////////////////
def menu():
    is_clicking = False

    start_game = Button(80, 40, 120, 150, "Start", BUTTON_COLOR, FONT_COLOR)
    options_game = Button(80, 40, 120, 200, "Options", BUTTON_COLOR, FONT_COLOR)
    exit_game = Button(80, 40, 120, 250, "Exit", BUTTON_COLOR, FONT_COLOR)

    particle_effects = []
    pointer_particle = Special_Effects()

    # Load music
    pygame.mixer.music.load(music_theme)
    pygame.mixer.music.play(-1)

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if start_game.rect.collidepoint(mouse_x, mouse_y):
            start_game.set_color(BUTTON_COLOR_SELECTED)
            if is_clicking:
                pygame.mixer.music.fadeout(1300)
                fade(WINDOW_SIZE, main_screen)
                main()
        else:
            start_game.set_color(BUTTON_COLOR)

        if options_game.rect.collidepoint(mouse_x, mouse_y):
            options_game.set_color(BUTTON_COLOR_SELECTED)
            if is_clicking:
                options()
        else:
            options_game.set_color(BUTTON_COLOR)

        if exit_game.rect.collidepoint(mouse_x, mouse_y):
            exit_game.set_color(BUTTON_COLOR_SELECTED)
            if is_clicking:
                exit()
        else:
            exit_game.set_color(BUTTON_COLOR)

        is_clicking = False
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_clicking = True
 
        # Particle Blast
        pointer_particle.particle(mouse_x, mouse_y, 0.2, 0, 0.03, 100, trigger=is_clicking)

        # Particle emiting
        particle_effects.append([ [mouse_x, mouse_y], [random.randint(10, 20) / 10 -2, random.randint(10, 20) / 10 -2], random.randint(2, 5)])

        screen.blit(font.render("Meteora", 0, (255, 240, 230)), (120, 10))
        screen.blit(font.render("a simple game by Frenzy", 0, (255, 240, 230)), (40, 60))

        start_game.draw(screen)
        options_game.draw(screen)
        exit_game.draw(screen)

        for i in particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.04
            i[1][0] +=  random.uniform(-0.4, 0.4)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                particle_effects.remove(i)

        main_screen.blit(screen, (0,0))
        pygame.display.update()
        clock.tick(30)

# Game Over Loop ////////////////////////////////////////////////////////////////////////////////////////////////////////////
def game_over(Score_obj):

    if Score_obj.get_score() > Score_obj.get_highscore():
        message = "Highscore!!!"
        Score_obj.set_highscore(Score_obj.get_score())
    else:
        message = "Score"

    is_clicking = False

    return_to_menu = Button(130, 40, 95, 150, "Back to Menu", ENEMY_COLOR, FONT_COLOR)
    play_again =     Button(130, 40, 95, 250, "One more try!", ENEMY_COLOR, FONT_COLOR)

    particle_effects = []
    pointer_particle = Special_Effects()

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if return_to_menu.rect.collidepoint(mouse_x, mouse_y):
            return_to_menu.set_color(BUTTON_COLOR_SELECTED)
            if is_clicking:
                menu()
        else:
            return_to_menu.set_color(BUTTON_COLOR)

        if play_again.rect.collidepoint(mouse_x, mouse_y):
            play_again.set_color(BUTTON_COLOR_SELECTED)
            if is_clicking:
                main()
        else:
            play_again.set_color(BUTTON_COLOR)

        is_clicking = False
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_clicking = True

        return_to_menu.draw(screen)
        play_again.draw(screen)

        screen.blit(font.render(message, 0, TEXT_COLOR), ( int(WINDOW_SIZE[0]/2)-int(font.size(message)[0]/2), WINDOW_SIZE[1] - 100))
        screen.blit(font.render(str(Score_obj.get_score()), 0, TEXT_COLOR), ( int(WINDOW_SIZE[0]/2) - int(font.size(str(Score_obj.get_score()))[0]) + 10, WINDOW_SIZE[1] - 60))

        # Particle Blast
        pointer_particle.particle(mouse_x, mouse_y, 0.2, 0, 0.03, 100, trigger=is_clicking)

        # Particle emiting
        particle_effects.append([ [mouse_x, mouse_y], [random.randint(10, 20) / 10 -2, random.randint(10, 20) / 10 -2], random.randint(2, 5)])

        for i in particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.04
            i[1][0] +=  random.uniform(-0.4, 0.4)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                particle_effects.remove(i)

        main_screen.blit(screen, (0,0))
        pygame.display.update()
        clock.tick(30)

# ////// Pause Loop ////////////////////////////////////////////////////////////////////////////////////////////////////
def pause():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    running = False
                    break

        screen.blit(font.render("Pause ", 0, TEXT_COLOR), (132, 230))
        main_screen.blit(screen, (0,0))
        pygame.display.update()
        clock.tick(30)

# ////// Game Loop ////////////////////////////////////////////////////////////////////////////////////////////////////
def main():
    running = True 

    # Initiate Objects
    mobs = pygame.sprite.Group()
    friends = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    P = Player()
    enemy = Enemy()
    score = Score()
    powerup = Powerup()
    
    # Had to put it here or else I'll end up with a method checking for the highscore every single damn time, and I'm not Yandere enough to do that
    highscore = str(score.get_highscore())

    counter = 0

    # Base offset, for screenshake
    offset = repeat((0,0))

    # Load music
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music_game)
    pygame.mixer.music.play(-1)
    # music_data[1].play(-1)
    
    # Explosion Counter, this is how I can control how many particle burst the game will create when the player looses
    gm_counter = 2
    game_over_counter = 60
    trigger = True
    explosion_particle = []

    while running:

        # Check all events
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_j: # Debug
                    # powerup.spawn(1, friends)
                    enemy.spawn(1, mobs)
                    for i in friends:
                        print(i.type)
                if event.key == K_SPACE:
                    pause()
                
                if event.key == K_z:
                    # TODO Figure out a way to fix sound issue
                    # sfx_data[1].play(1)
                    # pygame.mixer.Sound(sfx_shoot).play(1)
                    # pygame.mixer.music.play(1)
                    # pygame.mixer.music
                    P.shoot(bullets)


        if len(mobs.sprites()) != 20:
            if counter % 15 == 0:
                enemy.spawn(1, mobs)

        if (0.02 >= round(random.random(), 3)):
            powerup.spawn(1, friends)
        if counter >= 1000:
            counter = 0
        counter += 1

        screen.fill(BACKGROUND_COLOR)

        for i in pygame.sprite.spritecollide(P, mobs, True, pygame.sprite.collide_rect):
            if not P.get_shield():
                P.is_hit = True

                P.kill()
            P.set_shield(False)
        
        pygame.sprite.groupcollide(bullets, mobs, True, True)

        if P.is_hit:
            game_over_counter -= 1
            P.set_color(BACKGROUND_COLOR)
            if trigger == True:
                pygame.mixer.music.load(sfx_explosion)
                pygame.mixer.music.play(0)
                trigger = False
            while gm_counter != 0:
                offset = screenshake()
                for i in range(100):
                    explosion_particle.append([[P.rect.x, P.rect.y], [random.randint(0, 40) / 10 -2, random.randint(0, 40) / 10 -2], random.randint(4, 7)])
                gm_counter -= 1
            if game_over_counter == 0:
                game_over(score)
            
        P.draw(True, screen)
        mobs.update(score, P)
        mobs.draw(screen)

        friends.draw(screen)
        friends.update(score, P)

        bullets.draw(screen)
        bullets.update()

        P.key_manager()
        P.update()

        for i in explosion_particle:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.07
            i[1][0] +=  random.uniform(-0.3, 0.3)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                explosion_particle.remove(i)

        screen.blit(font.render("HIGHSCORE ", 0, TEXT_COLOR), ( int(WINDOW_SIZE[0]/2)-46, 10))
        screen.blit(font.render(highscore, 0, TEXT_COLOR), ( int(WINDOW_SIZE[0]/2-20), 30))
        screen.blit(font.render("SCORE " + str(score.get_score()), 0, TEXT_COLOR), (10, 40))
        screen.blit(font.render("AMMO " + str(P.get_ammo()), 0, TEXT_COLOR), (230, 40))

        main_screen.blit(screen, next(offset))
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    menu()


"""
To implement:

screenshake DONE!
shooting DONE!
shield - DONE!
sound effects (fix sound issue)

remove unused variables

add door sound (for fun)

bullet sound: D6

Shield: E3
"""
