from re import S, X
from tkinter.tix import Tree
import pygame
import json
import sys
import math

# implement switching tabs in the shop menu
# make sure the shop button hitbox is corrent

class Game:
    def __init__(self):
        pygame.init()

        # -------------------- WINDOW VARIABLES --------------------
        self.WIDTH = pygame.display.Info().current_w
        self.HEIGHT = pygame.display.Info().current_h
        self.SIZE = (self.WIDTH, self.HEIGHT)

        self.screen = pygame.display.set_mode(self.SIZE)

        # set window name and icon
        pygame.display.set_caption("CityDom")
        self.icon = pygame.image.load(r"pictures\icon.png")
        pygame.display.set_icon(self.icon)


        self.clock = pygame.time.Clock()
        self.FPS = 30

        # -------------------------- TEXT --------------------------
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_YELLOW = (255, 235, 100)
        self.YELLOW = (255, 230, 80)

        # ------------------------- IMAGES -------------------------
        # loading screen image
        self.loading_screen = pygame.image.load(r"pictures\loading screen.png")
        self.loading_screen = pygame.transform.scale(self.loading_screen, (self.WIDTH, self.HEIGHT))

        # backgroud image
        self.background_dirt = pygame.image.load(r"pictures\background_dirt.png")
        self.background = pygame.transform.scale(self.background_dirt, (2.5 * self.WIDTH, 2.5 * self.HEIGHT))

        self.background_center_x = self.WIDTH / 2
        self.background_center_y = self.HEIGHT / 2
        self.background_rect = self.background.get_rect(center=(self.background_center_x, self.background_center_y))

        self.movement_speed = 4

        # exit menu images
        self.exit_menu = pygame.image.load(r"pictures\exit menu blank.png")
        self.exit_menu_yes = pygame.image.load(r"pictures\exit menu yes.png")
        self.exit_menu_no = pygame.image.load(r"pictures\exit menu no.png")

        # shop button image
        self.shop_button = pygame.image.load(r"pictures\shop button.png")
        self.shop_button = pygame.transform.scale(self.shop_button, (self.WIDTH * 0.1, self.HEIGHT * 0.19))

        # shop images
        self.shop_top = pygame.image.load(r"pictures\shop menu top tab.png")
        self.shop_top = pygame.transform.scale(self.shop_top, (self.WIDTH, self.HEIGHT))
        self.shop_bottom = pygame.image.load(r"pictures\shop menu bottom tab.png")
        self.shop_bottom = pygame.transform.scale(self.shop_bottom, (self.WIDTH, self.HEIGHT))
        
        # coin bar image
        self.coin_bar = pygame.image.load(r"pictures\coin bar.png")

        # town hall image
        self.town_hall = pygame.image.load(r"pictures\town hall [ancient].png")
        self.town_hall = pygame.transform.scale(self.town_hall, (self.HEIGHT / 2, self.HEIGHT / 2))
        self.town_hall_rect = self.town_hall.get_rect(center=self.screen.get_rect().center)

        self.town_hall_x = self.WIDTH * 0.51
        self.town_hall_y = self.HEIGHT * 0.25

        # ------------------ GAME STATE VARIABLES ------------------
        self.running = True # if the game is running
        self.dragging = False # if the player is dragging the map around
        self.drag = True # if the player is able to drag the map
        self.exiting = False # if the player is in the exit menu
        self.shop_open = False # if the player has opened the shop
        self.tab_open = 0 # which shop tab is open, 0 for top tab, 1 for bottom tab

        self.update = pygame.USEREVENT + 1 # create event to update income
        pygame.time.set_timer(self.update, 1000) # updates every 1000 miliseconds or 1 second

        # --------------------- GAME VARIABLES ---------------------
        with open("data.json", "r") as read_file:
            self.data = json.load(read_file)

        # income
        self.money = self.data["balance"]
        self.income = self.data["income"]

    def fade_out(self): # fade out the loading screen
        fade = pygame.Surface((self.WIDTH, self.HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(30):
            fade.set_alpha(alpha * 10)
            self.draw_loading_screen()
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
    
    def draw_loading_screen(self): # display the loading screen
        self.loading_screen_rect = self.loading_screen.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
        self.screen.blit(self.loading_screen, self.loading_screen_rect)

    def loading(self): # run the loading screen
        self.draw_loading_screen()
        pygame.display.update()
        pygame.time.delay(3000)
        self.fade_out()

    def blit_background(self):
        self.background_rect.center = (self.background_center_x, self.background_center_y)
        self.screen.blit(self.background, self.background_rect)

    def blit_buildings(self):
        self.town_hall_rect.center = (self.town_hall_x, self.town_hall_y)
        self.screen.blit(self.town_hall, self.town_hall_rect)

    def blit_money_balance(self):
        # bar
        self.coin_bar_rect = self.coin_bar.get_rect()
        self.coin_bar_rect.right = self.WIDTH - 25
        self.coin_bar_rect.top = 25
        self.screen.blit(self.coin_bar, self.coin_bar_rect)
        # text
        font = pygame.font.Font(None, int(self.HEIGHT * 0.027))
        balance_text = font.render(str(self.money), True, self.BLACK)
        balance_text_rect = balance_text.get_rect()
        balance_text_rect.right = self.WIDTH - 60
        balance_text_rect.centery = self.coin_bar_rect.centery
        self.screen.blit(balance_text, balance_text_rect)

    def blit_shop_icon(self):
        self.shop_button_rect = self.shop_button.get_rect()
        self.shop_button_rect.right = self.WIDTH * 0.987
        self.shop_button_rect.bottom = self.HEIGHT * 0.977
        self.screen.blit(self.shop_button, self.shop_button_rect)

    def update_balance(self):
        self.money += self.income

    def display(self):
        self.blit_background()
        self.blit_buildings()
        self.blit_money_balance()
        self.blit_shop_icon()
        pygame.display.update()

    def check_event(self, event):
        # if user decides to exit game
        if event.type == pygame.QUIT:
            with open("data.json", "w") as write_file:
                self.data["balance"] = self.money
                self.data["income"] = self.income
                json.dump(self.data, write_file)
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_x_initial, self.mouse_y_initial = event.pos
            # start dragging/moving
            if event.button == 1 and self.drag: # check if user is able to drag 
                self.dragging = True
            if self.exiting: # if user clicks while the exit menu is open
                if self.mouse_x_initial >= self.WIDTH / 2 + 15 and self.mouse_x_initial <= self.WIDTH / 2 + 165: # check x is within yes button
                    if self.mouse_y_initial >= self.HEIGHT / 2 and self.mouse_y_initial <= self.HEIGHT / 2 + 40: # check y is within yes button
                        # display click
                        self.exit_menu_yes_rect = self.exit_menu_yes.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
                        self.screen.blit(self.exit_menu_yes, self.exit_menu_yes_rect)
                        self.exit_text() # display text
                        pygame.display.update() 
                        sys.exit() # user decided to exit game
                elif self.mouse_x_initial >= self.WIDTH / 2 - 165 and self.mouse_x_initial <= self.WIDTH / 2 - 15: # check x is within no button
                    if self.mouse_y_initial >= self.HEIGHT / 2 and self.mouse_y_initial <= self.HEIGHT / 2 + 40: # check y is within no button
                        self.exiting = False
                        self.drag = True
                        # display click
                        self.exit_menu_no_rect = self.exit_menu_no.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
                        self.screen.blit(self.exit_menu_no, self.exit_menu_no_rect)
                        self.exit_text()
                        pygame.display.update()
                        self.display()
                # check if player clicks outside the exit menu
                if self.mouse_y_initial <= self.HEIGHT / 2 - 50 or self.mouse_y_initial >= self.HEIGHT / 2 + 50: # if y is outside the exit menu y
                    self.exiting = False
                    self.drag = True
                    self.display()
                if self.mouse_y_initial >= self.HEIGHT / 2 - 50 and self.mouse_y_initial <= self.HEIGHT / 2 + 50: # if y is inside the exit menu y
                    if self.mouse_x_initial <= self.WIDTH / 2 - 200 or self.mouse_x_initial >= self.WIDTH / 2 + 200: # if x is outside the exit menu x
                        self.exiting = False
                        self.drag = True
                        self.display()
            # check if player clicks on the shop button
            if self.mouse_x_initial >= self.WIDTH - 200 - self.WIDTH * 0.013 and self.mouse_x_initial <= self.WIDTH  * 0.987: # if x is inside shop button
                if self.mouse_y_initial >= self.HEIGHT - 200 - self.HEIGHT * 0.023 and self.mouse_y_initial <= self.HEIGHT * 0.977: # if y is inside shop button
                    self.drag = False
                    self.shop_open = True
                    self.shopA()
            # check if player is clicking inside the shop
            if self.shop_open:
                # check if player is exiting the shop
                dist = math.sqrt((self.mouse_x_initial - self.WIDTH * 0.7671875) ** 2 + (self.mouse_y_initial - self.HEIGHT * 0.1814) ** 2) # center of the exit button is (1473, 196), radius 45
                if dist <= 45:
                    self.shop_open = False
                    self.drag = True
                    self.display()

                # check if player is switching tabs inside the shop
                if self.mouse_x_initial <= self.WIDTH / 2 - 540 and self.mouse_x_initial >= self.WIDTH / 2 - 600:
                    # if player is clicking on the top button
                    if self.mouse_y_initial <= self.HEIGHT / 2 and self.mouse_y_initial >= self.HEIGHT / 2 - 240:
                        self.tab_open = 0
                        self.shopA()
                    # if player is clicking on the bottom button
                    if self.mouse_y_initial <= self.HEIGHT / 2 + 240 and self.mouse_y_initial >= self.HEIGHT / 2:
                        self.tab_open = 1
                        self.shopB()

        elif event.type == pygame.MOUSEBUTTONUP:
            # stop dragging/moving
            if event.button == 1:
                self.dragging  = False
        elif event.type == pygame.MOUSEMOTION:
            # dragging/moving the background
            if self.dragging:
                self.mouse_x, self.mouse_y = event.pos
                movement_x = (self.mouse_x - self.mouse_x_initial) / self.movement_speed
                movement_y = (self.mouse_y - self.mouse_y_initial) / self.movement_speed

                if self.background_rect.left + movement_x >= 0 or self.background_rect.right + movement_x <= self.WIDTH:
                    movement_x = 0
                if self.background_rect.top + movement_y >= 0 or self.background_rect.bottom + movement_y <= self.HEIGHT:
                    movement_y = 0

                self.background_center_x += movement_x
                self.background_center_y += movement_y
                self.town_hall_x += movement_x
                self.town_hall_y += movement_y
                self.display()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit()
                self.exit_text()
        elif event.type == self.update:
            # update balance every second
            self.update_balance()

    def exit(self):
        # exiting
        self.exiting = True
        self.drag = False
        # draw exit game window
        self.exit_menu_rect = self.exit_menu.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
        self.screen.blit(self.exit_menu, self.exit_menu_rect)

    def exit_text(self):
        # display text
        font = pygame.font.Font(None, int(self.HEIGHT * 0.027))
        exit_text = font.render("Exit Game?", True, self.BLACK)
        exit_text_rect = exit_text.get_rect()
        exit_text_rect.centerx = self.WIDTH / 2
        exit_text_rect.centery = self.HEIGHT / 2 - 25
        self.screen.blit(exit_text, exit_text_rect)
        # display "NO" text on the left
        font = pygame.font.Font(None, int(self.HEIGHT * 0.024))
        no_text = font.render("NO", True, self.BLACK)
        no_text_rect = no_text.get_rect()
        no_text_rect.centerx = self.WIDTH / 2 - 90
        no_text_rect.centery = self.HEIGHT / 2 + 20
        self.screen.blit(no_text, no_text_rect)
        # display "YES" text on the right
        yes_text = font.render("YES", True, self.BLACK)
        yes_text_rect = yes_text.get_rect()
        yes_text_rect.centerx = self.WIDTH / 2 + 90
        yes_text_rect.centery = self.HEIGHT / 2 + 20
        self.screen.blit(yes_text, yes_text_rect)

    def shopA(self):
        self.shop_top_rect = self.shop_top.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
        self.screen.blit(self.shop_top, self.shop_top_rect)
        pygame.display.update()

    def shopB(self):
        self.shop_bottom_rect = self.shop_bottom.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
        self.screen.blit(self.shop_bottom, self.shop_bottom_rect)
        pygame.display.update()
                
    def on_execute(self):
        self.loading()
        self.display()
        while self.running:
            self.blit_money_balance()
            pygame.display.update()
            for event in pygame.event.get():
                self.check_event(event)
            self.clock.tick(self.FPS)

start = Game()
start.on_execute()