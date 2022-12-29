import pygame
import sys
import json


class Game:
    def __init__(self):
        pygame.init()

        # -------------------- SCREEN VARIABLES --------------------
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.SIZE = (self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode(self.SIZE)

        self.clock = pygame.time.Clock()
        self.FPS = 30

        # -------------------------- TEXT --------------------------

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_YELLOW = (255, 235, 100)
        self.YELLOW = (255, 230, 80)

        # ------------------------- IMAGES -------------------------
        # backgroud image
        self.background_dirt = pygame.image.load(r"pictures\background_dirt.png")
        self.background = pygame.transform.scale(self.background_dirt, (5760 * 0.8, 3240 * 0.8))
        self.background_rect = self.background.get_rect(center=self.screen.get_rect().center)
        
        self.background_center_x = self.WIDTH / 2
        self.background_center_y = self.HEIGHT / 2
        self.movement_speed = 4

        # town hall image
        self.town_hall = pygame.image.load(r"pictures\town hall [ancient].png")
        self.town_hall = pygame.transform.scale(self.town_hall, (500, 500))
        self.town_hall_rect = self.town_hall.get_rect(center=self.screen.get_rect().center)

        self.town_hall_x = self.WIDTH / 2 + 20
        self.town_hall_y = self.HEIGHT / 2 - 275

        # ------------------ GAME STATE VARIABLES ------------------
        self.running = True
        self.dragging = False

        self.update = pygame.USEREVENT + 1 # create event to update income
        pygame.time.set_timer(self.update, 1000) # updates every 1000 miliseconds or 1 second

        # --------------------- GAME VARIABLES ---------------------
        with open("data.json", "r") as read_file:
            self.data = json.load(read_file)

        # income
        self.money = self.data["balance"]
        self.income = 1

    def blit_background(self):
        self.background_rect.center = (self.background_center_x, self.background_center_y)
        self.screen.blit(self.background, self.background_rect)

    def blit_buildings(self):
        self.town_hall_rect.center = (self.town_hall_x, self.town_hall_y)
        self.screen.blit(self.town_hall, self.town_hall_rect)

    def blit_money_balance(self):
        # bar
        pygame.draw.rect(self.screen, self.LIGHT_YELLOW, pygame.Rect(self.WIDTH - 365, 35, 290, 40))
        pygame.draw.rect(self.screen, self.BLACK, pygame.Rect(self.WIDTH - 370, 30, 300, 50), 8, 8)
        # coin
        pygame.draw.circle(self.screen, self.LIGHT_YELLOW, (self.WIDTH - 50, 50), 35, 0)
        pygame.draw.circle(self.screen, self.BLACK, (self.WIDTH - 50, 50), 40, 7)
        # text
        font = pygame.font.Font(None, 30)
        balance_text = font.render(str(self.money), True, self.BLACK)
        balance_text_rect = balance_text.get_rect()
        balance_text_rect.right = self.WIDTH - 95
        balance_text_rect.top = 45
        self.screen.blit(balance_text, balance_text_rect)
    
    def update_balance(self):
        self.money += self.income

    def display(self):
        self.blit_background()
        self.blit_buildings()
        self.blit_money_balance()
        pygame.display.update()

    def check_event(self, event):
        # if user decides to exit game
        if event.type == pygame.QUIT:
            with open("data.json", "w") as write_file:
                self.data["balance"] = self.money
                json.dump(self.data, write_file)
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # start dragging/moving
            if event.button == 1:
                self.dragging = True
                self.mouse_x_initial, self.mouse_y_initial = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            # stop dragging/moving
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            # dragging/moving the background
            if self.dragging:
                self.mouse_x, self.mouse_y = event.pos
                movement_x = (self.mouse_x - self.mouse_x_initial)/self.movement_speed 
                movement_y = (self.mouse_y - self.mouse_y_initial)/self.movement_speed

                if self.background_rect.left + movement_x >= 0 or self.background_rect.right + movement_x <= self.WIDTH:
                    movement_x = 0
                if self.background_rect.top + movement_y >= 0 or self.background_rect.bottom + movement_y <= self.HEIGHT:
                    movement_y = 0

                self.background_center_x += movement_x
                self.background_center_y += movement_y
                self.town_hall_x += movement_x
                self.town_hall_y += movement_y
                self.display()
        
        elif event.type == self.update:
            # update balance every second
            self.update_balance()

    def intro(self):
        font = pygame.font.Font(None, 64)
        title_text = font.render('Penis', True, self.WHITE)
        fade_surface = title_text.copy()
        alpha_surface = pygame.Surface(fade_surface.get_size(), pygame.SRCALPHA)
        alpha = 0
        while alpha < 255:
            alpha += 1
            fade_surface = title_text.copy()
            alpha_surface.fill((255, 255, 255, alpha))
            fade_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.fill(self.BLACK)
            fade_surface_rect = fade_surface.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
            self.screen.blit(fade_surface, fade_surface_rect)
            pygame.display.update()
            pygame.time.delay(5)
        pygame.time.delay(2000)
        while alpha > 0:
            alpha -= 1
            fade_surface = title_text.copy()
            alpha_surface.fill((255, 255, 255, alpha))
            fade_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.fill(self.BLACK)
            fade_surface_rect = fade_surface.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
            self.screen.blit(fade_surface, fade_surface_rect)
            pygame.display.update()
            pygame.time.delay(5)

    def on_execute(self):
        # self.intro()
        self.display()
        while self.running:
            self.blit_money_balance()
            pygame.display.update()
            for event in pygame.event.get():
                self.check_event(event)
            self.clock.tick(self.FPS)

start = Game()
start.on_execute()
