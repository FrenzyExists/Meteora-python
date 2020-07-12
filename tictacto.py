import pygame
from pygame.locals import *
import sys
import random
from math import log2
import os

# Constants
PLAYER_COLOR = (199, 208, 215)
ENEMY_COLOR = (101, 120, 137)
BACKGROUND_COLOR = (79, 91, 103)
FONT_COLOR = (242, 242, 242)
WINDOW_SIZE = (320, 540)
# Adding speed = sqrt(score)/e**2

# TODO: Highscore list board

# Initiate Pygame
pygame.init()

# Pygame Base Stuff
clock = pygame.time.Clock()
pygame.display.set_caption("Meteora")

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
font = pygame.font.Font(os.path.join("resources", "Pixelar_Regular.ttf"), 26)
# All music from this game is made by Patric de Arteaga from patrickdearteaga.com under creative commons license
pygame.mixer.init()  # for sound


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
        surface.blit(font.render(self.text, 0, self.text_color), (self.x_pos + self.width/2 - self.tx/2, self.y_pos + self.height/2 - self.ty/2))


# ///// Special Effects ////////////////////////////////////////////////////////////////////////////////////////////////
class SpecialEffects:
    def __init__(self):
        particles = []
        pass
    def screenshake(self):
        pass

    def particle_blast(self, x, y, surface):
        particles = []

        particles.append([[x, y], [random.randint(0, 20) / 10 , -2], random.randint(2, 10)])

        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            pygame.draw.circle(surface, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            # pygame.draw.circle(surface, (255,255,255), (int(particle[0][1]+random.randint(-10,10)), int(particle[0][0])), int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)


class Player:
    def __init__(self):
        self.x_pos = 140
        self.y_pos = 500
        self.width = 30
        self.height = 30

        self.rect = pygame.rect.Rect((self.x_pos, self.y_pos, self.width, self.height))

    def draw(self, state, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect) if state is True else None

    def key_manager(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if key[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

    def update(self):
        if self.rect.left > WINDOW_SIZE[0]:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WINDOW_SIZE[0]

    def collision(self, Rect):
        # print(self.rect)
        if self.rect.colliderect(Rect):
            print("COLLISION!!!!")

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
        # self.vx = random.uniform(-log2(1.1), log2(1.1))

        self.is_drawn = True

    def move(self):
        self.rect.move_ip(0, self.vy)

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect)

    def update(self):
        self.rect.y += self.vy
        # self.rect.x += self.vx
        # if self.rect.top > WINDOW_SIZE[1] + 12 or self.rect.left < -30 or self.rect.right > WINDOW_SIZE[0] + 30:
        if self.rect.top > WINDOW_SIZE[1] + 12:
            self.rect.x = random.randrange(WINDOW_SIZE[0] - self.rect.width)
            self.rect.y = random.randrange(-240, -40)
            self.vy = random.randrange(2, 12)
            # self.vx = random.randrange(1, 4)

    def spawn(self, quantity, group):
        for i in range(quantity):
            grunt = Enemy()
            group.add(grunt)


# Score ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class Score:
    def __init__(self):
        self.score = 0

    def get_score(self):
        return self.score

    def set_score(self, amount):
        self.score += amount

# FPS //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def fps(frames):
    pygame.time.Clock().tick(frames)

# Options Loop /////////////////////////////////////////////////////////////////////////////////////////////////////////
def options():
    pass

# Menu Loop ////////////////////////////////////////////////////////////////////////////////////////////////////////////
def menu():
    is_clicking = False

    start_game = Button(80, 40, 120, 150, "Start", ENEMY_COLOR, FONT_COLOR)
    options_game = Button(80, 40, 120, 200, "Options", ENEMY_COLOR, FONT_COLOR)
    exit_game = Button(80, 40, 120, 250, "Exit", ENEMY_COLOR, FONT_COLOR)

    part = SpecialEffects()

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if start_game.rect.collidepoint(mouse_x, mouse_y):
            if is_clicking:
                main()

        if options_game.rect.collidepoint(mouse_x, mouse_y):
            if is_clicking:
                options()

        if exit_game.rect.collidepoint(mouse_x, mouse_y):
            if is_clicking:
                sys.exit()

        is_clicking = False
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_clicking = True

        part.particle_blast(mouse_x, mouse_y, screen)
        screen.blit(font.render("Meteora", 0, (255, 240, 230)), (120, 10))
        screen.blit(font.render("a simple game by Frenzy", 0, (255, 240, 230)), (40, 60))

        start_game.draw(screen)
        options_game.draw(screen)
        exit_game.draw(screen)
        pygame.display.update()
        clock.tick(30)


# ////// Game Loop ////////////////////////////////////////////////////////////////////////////////////////////////////
def main():

    # Initiate Objects
    P = Player()
    particle = SpecialEffects()
    mobs = pygame.sprite.Group()
    enemy = Enemy()
    score = Score()
    # enemy.spawn(8, mobs, score)
    score = Score()
    enemy.spawn(8, mobs)
    # print(mobs.sprites())

    while True:

        # Check all events
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_j:
                    print("Mob Generated")

        screen.fill(BACKGROUND_COLOR)
        # if P.rect.colliderect(enemy.rect):
        #     particle.particle_blast(P.x_pos, P.y_pos)
        for i in range(8):
            if pygame.sprite.spritecollideany(P, mobs):
                particle.particle_blast(random.randint(-P.x_pos, P.x_pos), random.randint(0, 100) + P.y_pos-60, screen)
            

        P.draw(True, screen)
        mobs.update()
        mobs.draw(screen)
        P.key_manager()
        P.collision(enemy.rect)
        P.update()

        screen.blit(font.render("SCORE " + str(score.get_score()), 0, (255, 240, 230)), (10, 10))

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    menu()
