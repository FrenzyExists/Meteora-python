# Load dependencies
import pygame
from pygame.locals import *
from sys import exit
import random
import csv
from pathlib import Path

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

# main_screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
# screen = main_screen.copy()
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

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
music_gameover = "resources/music_gameover.wav"
# music_highscore = "resources/music_highscore.ogg"
# sfx_select = "resources/sfx_select.ogg"
# sfx_explosion = "resources/sfx_explosion.ogg"
# sfx_selected = "resources/sfx_selected.ogg"


def offset(value):
    value = abs(value)
    temp = 0
    while temp < n:
        yield temp
        temp += 1

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

# Slider
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

# ///// Player (Single Object) //////////////////////////////////////////////////////////////////////////////////////////
class Player:
    def __init__(self):
        self.x_pos = 140
        self.y_pos = 500
        self.width = 30
        self.height = 30
        self.friction = 0.6
        self.acceleration = 0.4
        self.max_vel = 5.0
        self.fric = -0.1
        self.color = PLAYER_COLOR

        # bullets, you start with none
        self.ammo = 0
        self.max_ammo = 3

        # bullet delay
        self.shot_counter = 300

        # last shot
        self.last_shot = pygame.time.get_ticks()        

        self.rect = pygame.rect.Rect((WINDOW_SIZE[0], WINDOW_SIZE[1], self.width, self.height))
        self.rect.center = (int(WINDOW_SIZE[0]/2), int(WINDOW_SIZE[1]-20))
        self.pos = vec(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]-20)
        self.acc = vec(0, 0)
        self.vel_ = vec(0, 0)

        self.vel = 0

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

        self.rect.center = self.pos

    def update(self):
        if self.pos[0] - self.width/3 > WINDOW_SIZE[0]:
            self.pos[0] = 0
        if self.pos[0] + self.width/3 < 0:
            self.pos[0] = WINDOW_SIZE[0]

    def shoot(self):
        bullet = Bullet()
        self.ammo -=1
    
    def set_color(self, _color):
        self.color = _color

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

        self.is_drawn = True

        self.has_collided_with_screen = False
        self.has_counted = False

    def move(self):
        self.rect.move_ip(0, self.vy)

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect)

    def update(self, score_object):
        self.rect.y += self.vy
        if self.rect.top > WINDOW_SIZE[1] + 12:
            self.rect.x = random.randrange(WINDOW_SIZE[0] - self.rect.width)
            self.rect.y = random.randrange(-240, -40)
            self.vy = random.randrange(2, 12)

        if self.rect.top > WINDOW_SIZE[1]:
            if not self.has_counted:
                score_object.set_score(1)
                self.has_counted = True

        if self.rect.bottom <= 0:
            self.has_counted = False


    def spawn(self, quantity, group):
        for i in range(quantity):
            grunt = Enemy()
            group.add(grunt)


# Powerup //////////////////////////////////////////////////////////////////////////////////////////////////////////////
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Powerup class can acts as three different powerups:
        # Shield
        # Ammo

        self.width = 30
        self.height = 30

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(WINDOW_SIZE[0] - self.rect.width)
        self.rect.y = random.randrange(-220, -40)

        self.vy = random.randrange(3, 6)

        self.type = random.choice(['shield', 'ammo'])

    def type_shield(self):

        self.width = 30
        self.height = 30

    def type_ammo(self, player):

        self.width = 30
        self.height = 30
    
    # Yes, I took this from the enemy class, shut up
    def update(self, score_object):
        self.rect.y += self.vy
        if self.rect.top > WINDOW_SIZE[1] + 12:
            self.rect.x = random.randrange(WINDOW_SIZE[0] - self.rect.width)
            # self.rect.y = random.randrange(-240, -40)
            self.vy = random.randrange(2, 12)

        # if self.rect.top > WINDOW_SIZE[1]:
        #     if not self.has_counted:
        #         score_object.set_score(1)
        #         self.has_counted = True

        # if self.rect.bottom <= 0:
        #     self.has_counted = False


    def spawn(self, quantity, group):
        probability = 54 #percentage of a powerup to appear in current moment

        for i in range(quantity):
            powerup = Powerup()
            group.add(powerup)

    def collide(self, rect):
        pass


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
        return  int("".join(self.highscore[0])) # Make whatever the fuck this is drier

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


    main_menu = Button(140, 40, 90, 450, "Back to Menu", ENEMY_COLOR, FONT_COLOR)
    music_slider = Slider(190, 75, 100, 10)
    sfx_slider = Slider(190, 115, 100, 10)

    particle_effects = []
    mouse_particle_effects = []

    while running:
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

        if is_clicking:
            for i in range(100):
                mouse_particle_effects.append([ [mouse_x, mouse_y], [random.randint(0, 40) / 10 -2, random.randint(0, 40) / 10 -2], random.randint(4, 7)])
                # particle_list.append([ [mouse_x, mouse_y], [random.randint(0, 40) / 10 -2, -2], random.randint(2, 6)])

        particle_effects.append([ [mouse_x, mouse_y], [random.randint(10, 20) / 10 -2, random.randint(10, 20) / 10 -2], random.randint(2, 5)])

        screen.blit(font.render("Options", 0, (255, 240, 230)), (120, 20))
        screen.blit(font.render("Music", 0, (255, 240, 230)), (40, 70))
        screen.blit(font.render("Sound Effects", 0, (255, 240, 230)), (40, 110))

        main_menu.draw(screen)

        music_slider.draw(screen)
        sfx_slider.draw(screen)

        music_slider.get_input(get_events)
        sfx_slider.get_input(get_events)

        for i in mouse_particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.02
            i[1][0] +=  random.uniform(-0.3, 0.3)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                mouse_particle_effects.remove(i)


        for i in particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.04
            i[1][0] +=  random.uniform(-0.4, 0.4)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                particle_effects.remove(i)

        pygame.display.update()
        clock.tick(30)


# Menu Loop ////////////////////////////////////////////////////////////////////////////////////////////////////////////
def menu():
    is_clicking = False

    start_game = Button(80, 40, 120, 150, "Start", BUTTON_COLOR, FONT_COLOR)
    options_game = Button(80, 40, 120, 200, "Options", BUTTON_COLOR, FONT_COLOR)
    exit_game = Button(80, 40, 120, 250, "Exit", BUTTON_COLOR, FONT_COLOR)

    particle_effects = []
    mouse_particle_effects = []

    # Load music
    pygame.mixer.music.load(music_theme)
    pygame.mixer.music.play(-1)

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if start_game.rect.collidepoint(mouse_x, mouse_y):
            start_game.set_color(BUTTON_COLOR_SELECTED)
            if is_clicking:
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

        if is_clicking:
            for i in range(100):
                mouse_particle_effects.append([ [mouse_x, mouse_y], [random.randint(0, 40) / 10 -2, random.randint(0, 40) / 10 -2], random.randint(4, 7)])
                

        particle_effects.append([ [mouse_x, mouse_y], [random.randint(10, 20) / 10 -2, random.randint(10, 20) / 10 -2], random.randint(2, 5)])

        screen.blit(font.render("Meteora", 0, (255, 240, 230)), (120, 10))
        screen.blit(font.render("a simple game by Frenzy", 0, (255, 240, 230)), (40, 60))

        start_game.draw(screen)
        options_game.draw(screen)
        exit_game.draw(screen)

        for i in mouse_particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.02
            i[1][0] +=  random.uniform(-0.3, 0.3)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                mouse_particle_effects.remove(i)


        for i in particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.04
            i[1][0] +=  random.uniform(-0.4, 0.4)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                particle_effects.remove(i)


        pygame.display.update()
        clock.tick(30)


# Game Over Loop ////////////////////////////////////////////////////////////////////////////////////////////////////////////
def game_over(Score_obj):

    print(Score_obj.get_score())
    print(Score_obj.get_highscore())

    if Score_obj.get_score() > Score_obj.get_highscore():
        message = "Highscore!!!"
        Score_obj.set_highscore(Score_obj.get_score())
    else:
        message = "Score"


    is_clicking = False

    return_to_menu = Button(130, 40, 95, 150, "Back to Menu", ENEMY_COLOR, FONT_COLOR)
    play_again =     Button(130, 40, 95, 250, "One more try!", ENEMY_COLOR, FONT_COLOR)

    particle_effects = []
    mouse_particle_effects = []


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


        if is_clicking:
            for i in range(100):
                mouse_particle_effects.append([ [mouse_x, mouse_y], [random.randint(0, 40) / 10 -2, random.randint(0, 40) / 10 -2], random.randint(4, 7)])
                

        particle_effects.append([ [mouse_x, mouse_y], [random.randint(10, 20) / 10 -2, random.randint(10, 20) / 10 -2], random.randint(2, 5)])

        for i in mouse_particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.02
            i[1][0] +=  random.uniform(-0.3, 0.3)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                mouse_particle_effects.remove(i)


        for i in particle_effects:
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]
            i[2] -= 0.04
            i[1][0] +=  random.uniform(-0.4, 0.4)
            pygame.draw.circle(screen, PLAYER_COLOR, [int(i[0][0]), int(i[0][1])], int(i[2]))
            if i[2] <= 0:
                particle_effects.remove(i)


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

        screen.blit(font.render("Pause ", 0, TEXT_COLOR), ( 132, 230))
        pygame.display.update()
        clock.tick(30)

# ////// Game Loop ////////////////////////////////////////////////////////////////////////////////////////////////////
def main():

    running = True 

    # Initiate Objects
    player_group = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    P = Player()
    
    enemy = Enemy()
    score = Score()
    
    # Had to put it here or else I'll end up with a method checking for the highscore every single damn time, and I'm not Yandere enough to do that
    highscore = str(score.get_highscore())

    counter = 0

    # Load music
    pygame.mixer.music.load(music_game)
    pygame.mixer.music.play(-1)

    # Explosion Counter, this is how I can control how many particle burst the game will create when the player looses
    gm_counter = 2
    game_over_counter = 60
    is_hit = False
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
                    enemy.spawn(1, mobs)
                    print("Mob Generated")
                if event.key == K_SPACE:
                    pause()

        if len(mobs.sprites()) != 20:
            if counter % 15 == 0:
                enemy.spawn(1, mobs)
        if counter >= 1000:
            counter = 0
        counter += 1

        screen.fill(BACKGROUND_COLOR)
 
        for i in range(8):
            if pygame.sprite.spritecollideany(P, mobs):

                is_hit = True
                break
        
        if is_hit == True:
            
            game_over_counter -= 1
            P.set_color(BACKGROUND_COLOR)
            while gm_counter != 0:
                for i in range(100):
                    explosion_particle.append([[P.rect.x, P.rect.y], [random.randint(0, 40) / 10 -2, random.randint(0, 40) / 10 -2], random.randint(4, 7)])
                gm_counter -= 1
            if game_over_counter == 0:
                
                game_over(score)
            

        P.draw(True, screen)
        mobs.update(score)
        mobs.draw(screen)
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
        screen.blit(font.render(highscore, 0, TEXT_COLOR), (WINDOW_SIZE[0]/2-20, 30))
        screen.blit(font.render("SCORE " + str(score.get_score()), 0, TEXT_COLOR), (10, 40))
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    menu()
