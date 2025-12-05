import pygame
import sys
import os

# general settings
W, H = 640, 360
FPS = 60

# game states
MENU = 0
START = 1
GAME = 2
WIN = 3
LOSE = 4

def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W,H))
        pygame.display.set_caption("Dungeons and Starvation")
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.camera = 0

def main(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)

            if self.state == MENU:
                self.draw_menu()
            elif self.state == START:
                self.update_start(keys, dt)
                self.draw_start()
            elif self.state == GAME:
                self.update_game(keys, dt)
                self.update_hunger(dt)
                self.draw_game()
            elif self.state == WIN:
                self.screen.blit(self.bg_win, (0,0))
                self.btn_restart_win.draw(self.screen)
            elif self.state == LOSE:
                self.screen.blit(self.bg_lose, (0,0))
                self.btn_restart_lose.draw(self.screen)

            pygame.display.update()

# helps to load images
BASE = os.path.dirname(os.path.abspath(__file__))
def load_image(path):
    return pygame.image.load(os.path.join(BASE, path)).convert_alpha()

# the button functions
class Button:
    def __init__(self, image, pos):
        self.image = image
        self.rect = image.get_rect(center=pos)

    # draw button onto the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # checks if the button was clicked
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# drawing the platform onto the screen
class Platform:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera, self.rect.y))

# drawing the food onto the screen
class Food:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.collected = False

    def draw(self, screen, camera):
        if not self.collected:
            screen.blit(self.image, (self.rect.x - camera, self.rect.y))

