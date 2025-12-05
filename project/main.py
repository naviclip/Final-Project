import pygame
import sys
import os

# general settings
W, H = 640, 360
FPS = 60
GRAVITY = 0.8
JUMP = -12
SPEED = 3.5
ANIM_SPEED = 0.1
HUNGER_DECREMENT_TIME = 2.0
HUNGER_DECREMENT = 1
HUNGER_INCREMENT = 1
MAX_HUNGER_ICONS = 4

# game states
MENU = 0
START = 1
GAME = 2
WIN = 3
LOSE = 4

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W,H))
        pygame.display.set_caption("Dungeons and Starvation")
        self.clock = pygame.time.Clock()
        self.state = MENU
        self.camera = 0
    
    # loading in all of the image assets
        self.bg_menu = load_image("assets/ui/title_bg.png")
        self.bg_start = load_image("assets/backgrounds/start/bg_start_0.png")
        self.bg_dungeon = load_image("assets/backgrounds/dungeon/bg_dungeon_0.png")
        self.bg_win = load_image("assets/ui/win_bg.png")
        self.bg_lose = load_image("assets/ui/lose_bg.png")

        self.btn_start = Button(load_image("assets/ui/buttons/button_start.png"), (470, 274))
        self.btn_quit = Button(load_image("assets/ui/buttons/button_quit.png"), (470, 334))
        self.btn_restart_win = Button(load_image("assets/ui/buttons/button_restart.png"), (549, 191))
        self.btn_restart_lose = Button(load_image("assets/ui/buttons/button_restart.png"), (141, 199))

        self.start_ground = load_image("assets/platforms/start_ground.png")
        self.dungeon_ground = load_image("assets/platforms/dungeon_ground.png")

        p0 = load_image("assets/platforms/platform_0.png")
        p1 = load_image("assets/platforms/platform_1.png")
        self.platforms = [Platform(300, 150, p0), Platform(500, 110, p1), Platform(700, 170, p0)]

        idle = load_image("assets/agnis/agnis/idle/agnis_idle_0.png")
        left_imgs = [load_image(f"assets/agnis/agnis/run_left/agnis_run_left00{i}.png") for i in range(4)]
        right_imgs = [load_image(f"assets/agnis/agnis/run_right/agnis_run_right00{i}.png") for i in range(4)]
        self.player = Player(idle, left_imgs, right_imgs)

        # food
        self.food_img = load_image("assets/agnis/food/food.png")
        self.foods = [
            Food(self.platforms[0].rect.x + 10, self.platforms[0].rect.y - 20, self.food_img),
            Food(self.platforms[1].rect.x + 10, self.platforms[1].rect.y - 20, self.food_img),
            Food(self.platforms[2].rect.x + 10, self.platforms[2].rect.y - 20, self.food_img)
        ]

        # hunger
        self.hunger = MAX_HUNGER_ICONS
        self.hunger_timer = 0

    # get ground y positions
    def start_ground_y(self):
        return H - self.start_ground.get_height()
    def dungeon_ground_y(self):
        return H - self.dungeon_ground.get_height()

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

class Player:
    def __init__(self, idle_img, left_imgs, right_imgs):
        self.idle_img = idle_img
        self.left_imgs = left_imgs
        self.right_imgs = right_imgs

        self.x = 200
        self.y = 200
        self.vy = 0
        self.sprite_index = 0
        self.anim_timer = 0
        self.sprite = idle_img
        self.width = idle_img.get_width()
        self.height = idle_img.get_height()

    # animates the player when moving
    def animate(self, left, right, dt):
        if not left and not right:
            self.sprite = self.idle_img
            self.sprite_index = 0
            self.anim_timer = 0
            return

        images = self.left_imgs if left else self.right_imgs
        self.anim_timer += dt
        if self.anim_timer >= ANIM_SPEED:
            self.sprite_index = (self.sprite_index + 1) % len(images)
            self.anim_timer = 0
        self.sprite = images[self.sprite_index]

    # draws the player
    def draw(self, screen, camera):
        screen.blit(self.sprite, (self.x - camera, self.y))

def main():
    Game().run()
    
if __name__ == "__main__":
    main()
