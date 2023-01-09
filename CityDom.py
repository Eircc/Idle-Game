from re import S, X
from tkinter.tix import Tree
import pygame
import json
import sys
import math

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
        self.RED = (255, 0, 0)

        # ------------------------- IMAGES -------------------------
        # loading screen image
        self.loading_screen = pygame.image.load(r"pictures\loading screen.png")
        self.loading_screen = pygame.transform.scale(self.loading_screen, (self.WIDTH, self.HEIGHT))

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
        
        # LOADING ALL GAME RESOURCES
        # backgroud image
        self.background_early = pygame.image.load(r"pictures\background [ancient].png")
        self.background_middle = pygame.image.load(r"pictures\background [middle renaissance].png")
        self.background_late = pygame.image.load(r"pictures\background [industrial, modern].png")
        self.background = pygame.transform.scale(self.background_middle, (2.5 * self.WIDTH, 2.5 * self.HEIGHT))

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
        self.shop_red_button = pygame.image.load(r"pictures\shop red button.png")
        self.shop_red_button = pygame.transform.scale(self.shop_red_button, (self.WIDTH * 0.1, self.HEIGHT * 0.07))
        self.shop_red_button_clicked = pygame.image.load(r"pictures\shop red button clicked.png")
        self.shop_red_button_clicked = pygame.transform.scale(self.shop_red_button_clicked, (self.WIDTH * 0.1, self.HEIGHT * 0.07))
        self.shop_green_button_clicked = pygame.image.load(r"pictures\shop green button clicked.png")
        self.shop_green_button_clicked = pygame.transform.scale(self.shop_green_button_clicked, (self.WIDTH * 0.1, self.HEIGHT * 0.07))

        # shop images
        self.shop_top = pygame.image.load(r"pictures\shop menu top tab.png")
        self.shop_top = pygame.transform.scale(self.shop_top, (self.WIDTH, self.HEIGHT))
        self.shop_bottom = pygame.image.load(r"pictures\shop menu bottom tab.png")
        self.shop_bottom = pygame.transform.scale(self.shop_bottom, (self.WIDTH, self.HEIGHT))
        self.shop_bar = pygame.image.load(r"pictures\shop menu buttons.png")
        self.shop_bar = pygame.transform.scale(self.shop_bar, (self.WIDTH / 2, self.HEIGHT / 9)) # 960x120

        self.shop_build_item_names = ["House", "Animal Farm", "Crop Farm", "Mine"]
        self.shop_upgrade_item_names = ["Upgrade 1", "Upgrade 2", "Upgrade 3", "Upgrade 4"]
        self.shop_item_y = [self.HEIGHT / 36 * 11, self.HEIGHT / 9 * 4, self.HEIGHT / 12 * 7, self.HEIGHT / 18 * 13] # 330, 480, 630, 780
        
        self.house_shop = pygame.image.load(r"pictures\house [ancient].png")
        self.house_shop = pygame.transform.scale(self.house_shop, (self.WIDTH / 19.2, self.HEIGHT / 10.8)) # 150x150
        self.barn_shop = pygame.image.load(r"pictures\barn.png")
        self.barn_shop = pygame.transform.scale(self.barn_shop, (self.WIDTH / 19.2, self.HEIGHT / 10.8)) # 150x150)
        self.pasture_shop = pygame.image.load(r"pictures\pasture.png")
        self.pasture_shop = pygame.transform.scale(self.pasture_shop, (self.WIDTH / 19.2, self.HEIGHT / 10.8)) # 150x150)

        # coin bar image
        self.coin_bar = pygame.image.load(r"pictures\coin bar.png")

        # town hall image
        self.town_hall = pygame.image.load(r"pictures\town hall [ancient].png")
        self.town_hall = pygame.transform.scale(self.town_hall, (self.HEIGHT / 2, self.HEIGHT / 2))
        self.town_hall_rect = self.town_hall.get_rect(center=self.screen.get_rect().center)

        self.town_hall_x = self.WIDTH * 0.59
        self.town_hall_y = self.HEIGHT * 0.40

        # building images
        self.house = pygame.image.load(r"pictures\house [ancient].png")
        self.house = pygame.transform.scale(self.house, (self.HEIGHT * 0.231, self.WIDTH * 0.130))
        self.barn = pygame.image.load(r"pictures\barn.png")
        self.barn = pygame.transform.scale(self.barn, (self.HEIGHT * 0.231, self.WIDTH * 0.13))
        self.pasture = pygame.image.load(r"pictures\pasture.png")
        self.pasture = pygame.transform.scale(self.pasture, (self.HEIGHT * 0.231, self.WIDTH * 0.13))

        self.upgrade = pygame.image.load(r"pictures\upgrade.png")
        self.upgrade = pygame.transform.scale(self.upgrade, (self.HEIGHT * 0.0694, self.WIDTH * 0.039))

        # TESTING
        # self.test_x = self.WIDTH * 1.04
        # self.test_y = self.HEIGHT * 1.56
        # self.test_x2 = self.WIDTH * 0.57
        # self.test_y2 = self.HEIGHT * 1.25
        # self.test_x3 = self.WIDTH * 0.46
        # self.test_y3 = self.HEIGHT * 1.35

        # fonts
        self.title_font = r"fonts\LuckiestGuy.ttf"
        self.subtitle_font = r"fonts\Staatliches-Regular.ttf"
        self.text_font = r"fonts\Aleo Regular 400.ttf"

        # ------------------ GAME STATE VARIABLES ------------------
        self.running = True # if the game is running
        self.dragging = False # if the player is dragging the map around
        self.drag = True # if the player is able to drag the map
        self.exiting = False # if the player is in the exit menu
        self.shop_open = False # if the player has opened the shop
        self.shop_tab_open = 0 # which shop tab is open, 0 for top tab, 1 for bottom tab

        self.update = pygame.USEREVENT + 1 # create event to update income
        pygame.time.set_timer(self.update, 1000) # updates every 1000 miliseconds or 1 second

        # --------------------- GAME VARIABLES ---------------------
        with open("data.json", "r") as read_file:
            self.data = json.load(read_file)

        # income
        self.money = self.data["balance"]
        self.income = self.data["income"]

        # cps and cost
        self.house_cost = self.data["costs"]["house"] # original $100
        self.house_cps = self.data["cps"]["house"] # original $5
        self.barn_cost = self.data["costs"]["barn"] # original $1000
        self.barn_cps = self.data["cps"]["barn"] # original $40
        self.pasture_cost = self.data["costs"]["pasture"] # original $5000
        self.pasture_cps = self.data["cps"]["pasture"] # original $150

        self.house_upgrade_cost = self.data["upgrade costs"]["house"] # original $250
        self.barn_upgrade_cost = self.data["upgrade costs"]["barn"] # original $1500
        self.pasture_upgrade_cost = self.data["upgrade costs"]["pasture"] # original $7500
        self.all_upgrade_cost = self.data["upgrade costs"]["all"] # original $15000

        self.default_positions = [ # 1, 3, 4, 17, 15, 16, 13, 11, 2, 10, 8, 9, 7, 5, 6, 18, 25, 24, 21, 20, 14, 22, 23, 12, 19, 26, 27, 28
            [0.255, 0.3], # 1
            [0.345, 0.49], # 3
            [0.43, 0.65], # 4
            [0.55, 0.88], # 17
            [0.72, 0.7], # 15
            [0.88, 0.53], # 16
            [0.76, 0.28], # 13
            [0.585, 0.11], # 11
            [0.43, 0.245], # 2
            [0.3, 0.02], # 10
            [0.155, 0.132], # 8
            [0.01, 0.26], # 9
            [0.115, 0.45], # 7
            [0.2, 0.63], # 5
            [0.289, 0.775], # 6             
            [0.43, 0.99], # 18
            [0.57, 1.25], # 25
            [0.68, 1.15], # 24
            [0.86, 0.98], # 21
            [1.05, 0.84], # 20
            [0.9, 0.132], # 14
            [0.75, -0.09], # 22
            [0.62, -0.3], # 23
            [0.455, -0.13], # 12
            [0.31, 1.1], # 19
            [0.46, 1.35], # 26
            [0.91, 1.31], # 27
            [1.04, 1.56], # 28
        ]
        self.positions = []
        self.buildings = self.data["buildings"]

        self.total_shift = [0, 0]

        self.fade_out() # fade out the loading screen

    def blit_background(self):
        self.background_rect.center = (self.background_center_x, self.background_center_y)
        self.screen.blit(self.background, self.background_rect)

    def blit_buildings(self):
        self.town_hall_rect.center = (self.town_hall_x, self.town_hall_y)
        self.screen.blit(self.town_hall, self.town_hall_rect)

        for i in range(len(self.buildings)):
            if self.buildings[i] == "house":
                house_rect = self.house.get_rect()
                house_rect.centerx = self.WIDTH * self.default_positions[i][0] + self.total_shift[0]
                house_rect.centery = self.HEIGHT * self.default_positions[i][1] + self.total_shift[1]
                self.screen.blit(self.house, house_rect)
            if self.buildings[i] == "barn":
                barn_rect = self.barn.get_rect()
                barn_rect.centerx = self.WIDTH * self.default_positions[i][0] + self.total_shift[0]
                barn_rect.centery = self.HEIGHT * self.default_positions[i][1] + self.total_shift[1]
                self.screen.blit(self.barn, barn_rect)
            if self.buildings[i] == "pasture":
                pasture_rect = self.pasture.get_rect()
                pasture_rect.centerx = self.WIDTH * self.default_positions[i][0] + self.total_shift[0]
                pasture_rect.centery = self.HEIGHT * self.default_positions[i][1] + self.total_shift[1]
                self.screen.blit(self.pasture, pasture_rect)

        # TESTING
        # house_rect = self.pasture.get_rect()
        # house_rect.centerx = self.test_x
        # house_rect.centery = self.test_y
        # self.screen.blit(self.pasture, house_rect)
        # house_rect = self.pasture.get_rect()
        # house_rect.centerx = self.test_x2
        # house_rect.centery = self.test_y2
        # self.screen.blit(self.pasture, house_rect)
        # house_rect = self.pasture.get_rect()
        # house_rect.centerx = self.test_x3
        # house_rect.centery = self.test_y3
        # self.screen.blit(self.pasture, house_rect)

    def blit_money_balance(self):
        # bar
        self.coin_bar_rect = self.coin_bar.get_rect()
        self.coin_bar_rect.right = self.WIDTH - 25
        self.coin_bar_rect.top = 25
        self.screen.blit(self.coin_bar, self.coin_bar_rect)
        # text
        font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.027))
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
            self.save()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_x_initial, self.mouse_y_initial = event.pos
            # EXIT MENU
            if self.exiting: # if user clicks while the exit menu is open
                if self.mouse_x_initial >= self.WIDTH / 2 + 15 and self.mouse_x_initial <= self.WIDTH / 2 + 165: # check x is within yes button
                    if self.mouse_y_initial >= self.HEIGHT / 2 and self.mouse_y_initial <= self.HEIGHT / 2 + 40: # check y is within yes button
                        # display click
                        self.exit_menu_yes_rect = self.exit_menu_yes.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
                        self.screen.blit(self.exit_menu_yes, self.exit_menu_yes_rect)
                        self.exit_text() # display text
                        pygame.display.update() 
                        self.save()
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
                        if self.shop_open:
                            self.shop()
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
            # SHOP MENU
            elif self.shop_open:
                # check if player is exiting the shop
                dist = math.sqrt((self.mouse_x_initial - self.WIDTH * 0.7671875) ** 2 + (self.mouse_y_initial - self.HEIGHT * 0.1814) ** 2) # center of the exit button is (1473, 196), radius 45
                if dist <= 45:
                    self.shop_open = False
                    self.drag = True
                    self.display()
                # check if player is switching tabs inside the shop
                if self.mouse_x_initial <= self.WIDTH / 2 - self.WIDTH * 0.28125 and self.mouse_x_initial >= self.WIDTH / 2 - self.WIDTH * 0.3125:
                    # if player is clicking on the top button
                    if self.mouse_y_initial <= self.HEIGHT / 2 and self.mouse_y_initial >= self.HEIGHT / 2 - self.HEIGHT * 0.2222:
                        self.shop_tab_open = 0
                        self.shop()
                    # if player is clicking on the bottom button
                    if self.mouse_y_initial <= self.HEIGHT / 2 + self.HEIGHT * 0.2222 and self.mouse_y_initial >= self.HEIGHT / 2:
                        self.shop_tab_open = 1
                        self.shop()
                # check if player is buying something
                if self.shop_tab_open == 0:
                    # if player x is within one of the green buttons
                    if self.mouse_x_initial >= self.WIDTH * 0.625 and self.mouse_x_initial <= self.WIDTH * 0.719:
                        # if player is buying first item
                        if self.mouse_y_initial >= self.shop_item_y[0] - self.HEIGHT / 36 and self.mouse_y_initial <= self.shop_item_y[0] + self.HEIGHT / 36:
                            if self.money >= self.house_cost:
                                # clicking animation
                                green_clicked_rect = self.shop_green_button_clicked.get_rect()
                                green_clicked_rect.centerx = self.WIDTH * 0.673
                                green_clicked_rect.centery = self.shop_item_y[0]
                                self.screen.blit(self.shop_green_button_clicked, green_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                house_cost = font.render(f"${self.house_cost}", True, self.WHITE)
                                house_cost_rect = house_cost.get_rect()
                                house_cost_rect.centerx = self.WIDTH * 0.673
                                house_cost_rect.centery = self.shop_item_y[0]
                                self.screen.blit(house_cost, house_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)

                                self.money -= self.house_cost
                                self.income += self.house_cps
                                self.buildings.append('house')
                                self.house_cost *= 2
                                self.shop()
                            else:
                                # clicking animation
                                red_clicked_rect = self.shop_red_button_clicked.get_rect()
                                red_clicked_rect.centerx = self.WIDTH * 0.673
                                red_clicked_rect.centery = self.shop_item_y[0]
                                self.screen.blit(self.shop_red_button_clicked, red_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                house_cost = font.render(f"${self.house_cost}", True, self.WHITE)
                                house_cost_rect = house_cost.get_rect()
                                house_cost_rect.centerx = self.WIDTH * 0.673
                                house_cost_rect.centery = self.shop_item_y[0]
                                self.screen.blit(house_cost, house_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)
                                self.shop()
                        # if player is buying second item
                        elif self.mouse_y_initial >= self.shop_item_y[1] - self.HEIGHT / 36 and self.mouse_y_initial <= self.shop_item_y[1] + self.HEIGHT / 36:
                            if self.money >= self.barn_cost:
                                # clicking animation
                                green_clicked_rect = self.shop_green_button_clicked.get_rect()
                                green_clicked_rect.centerx = self.WIDTH * 0.673
                                green_clicked_rect.centery = self.shop_item_y[1]
                                self.screen.blit(self.shop_green_button_clicked, green_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                barn_cost = font.render(f"${self.barn_cost}", True, self.WHITE)
                                barn_cost_rect = barn_cost.get_rect()
                                barn_cost_rect.centerx = self.WIDTH * 0.673
                                barn_cost_rect.centery = self.shop_item_y[1]
                                self.screen.blit(barn_cost, barn_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)

                                self.money -= self.barn_cost
                                self.income += self.barn_cps
                                self.buildings.append('barn')
                                self.barn_cost *= 3
                                self.shop()
                            else:
                                # clicking animation
                                red_clicked_rect = self.shop_red_button_clicked.get_rect()
                                red_clicked_rect.centerx = self.WIDTH * 0.673
                                red_clicked_rect.centery = self.shop_item_y[1]
                                self.screen.blit(self.shop_red_button_clicked, red_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                barn_cost = font.render(f"${self.barn_cost}", True, self.WHITE)
                                barn_cost_rect = barn_cost.get_rect()
                                barn_cost_rect.centerx = self.WIDTH * 0.673
                                barn_cost_rect.centery = self.shop_item_y[1]
                                self.screen.blit(barn_cost, barn_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)
                                self.shop()
                        # if player is buying third item
                        elif self.mouse_y_initial >= self.shop_item_y[2] - self.HEIGHT / 36 and self.mouse_y_initial <= self.shop_item_y[2] + self.HEIGHT / 36:
                            if self.money >= self.pasture_cost:
                                green_clicked_rect = self.shop_green_button_clicked.get_rect()
                                green_clicked_rect.centerx = self.WIDTH * 0.673
                                green_clicked_rect.centery = self.shop_item_y[2]
                                self.screen.blit(self.shop_green_button_clicked, green_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                pasture_cost = font.render(f"${self.pasture_cost}", True, self.WHITE)
                                pasture_cost_rect = pasture_cost.get_rect()
                                pasture_cost_rect.centerx = self.WIDTH * 0.673
                                pasture_cost_rect.centery = self.shop_item_y[2]
                                self.screen.blit(pasture_cost, pasture_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)

                                self.money -= self.pasture_cost
                                self.income += self.pasture_cps
                                self.buildings.append('pasture')
                                self.pasture_cost *= 4
                                self.shop()
                            else:
                                # clicking animation
                                red_clicked_rect = self.shop_red_button_clicked.get_rect()
                                red_clicked_rect.centerx = self.WIDTH * 0.673
                                red_clicked_rect.centery = self.shop_item_y[2]
                                self.screen.blit(self.shop_red_button_clicked, red_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                pasture_cost = font.render(f"${self.pasture_cost}", True, self.WHITE)
                                pasture_cost_rect = pasture_cost.get_rect()
                                pasture_cost_rect.centerx = self.WIDTH * 0.673
                                pasture_cost_rect.centery = self.shop_item_y[2]
                                self.screen.blit(pasture_cost, pasture_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)
                                self.shop()
                # check if player is upgrading something
                else:
                    # if player x is within one of the green buttons
                    if self.mouse_x_initial >= self.WIDTH * 0.625 and self.mouse_x_initial <= self.WIDTH * 0.719:
                        # if player is buying first item
                        if self.mouse_y_initial >= self.shop_item_y[0] - self.HEIGHT / 36 and self.mouse_y_initial <= self.shop_item_y[0] + self.HEIGHT / 36:
                            if self.money >= self.house_upgrade_cost:
                                # clicking animation
                                green_clicked_rect = self.shop_green_button_clicked.get_rect()
                                green_clicked_rect.centerx = self.WIDTH * 0.673
                                green_clicked_rect.centery = self.shop_item_y[0]
                                self.screen.blit(self.shop_green_button_clicked, green_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                house_upgrade_cost = font.render(f"${self.house_upgrade_cost}", True, self.WHITE)
                                house_upgrade_cost_rect = house_upgrade_cost.get_rect()
                                house_upgrade_cost_rect.centerx = self.WIDTH * 0.673
                                house_upgrade_cost_rect.centery = self.shop_item_y[0]
                                self.screen.blit(house_upgrade_cost, house_upgrade_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)

                                self.money -= self.house_upgrade_cost
                                self.house_cps *= 2
                                self.house_upgrade_cost *= 5
                                self.shop()
                            else:
                                # clicking animation
                                red_clicked_rect = self.shop_red_button_clicked.get_rect()
                                red_clicked_rect.centerx = self.WIDTH * 0.673
                                red_clicked_rect.centery = self.shop_item_y[0]
                                self.screen.blit(self.shop_red_button_clicked, red_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                house_upgrade_cost = font.render(f"${self.house_upgrade_cost}", True, self.WHITE)
                                house_upgrade_cost_rect = house_upgrade_cost.get_rect()
                                house_upgrade_cost_rect.centerx = self.WIDTH * 0.673
                                house_upgrade_cost_rect.centery = self.shop_item_y[0]
                                self.screen.blit(house_upgrade_cost, house_upgrade_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)
                                self.shop()
                        # if player is buying second item
                        elif self.mouse_y_initial >= self.shop_item_y[1] - self.HEIGHT / 36 and self.mouse_y_initial <= self.shop_item_y[1] + self.HEIGHT / 36:
                            if self.money >= self.barn_upgrade_cost:
                                # clicking animation
                                green_clicked_rect = self.shop_green_button_clicked.get_rect()
                                green_clicked_rect.centerx = self.WIDTH * 0.673
                                green_clicked_rect.centery = self.shop_item_y[1]
                                self.screen.blit(self.shop_green_button_clicked, green_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                barn_upgrade_cost = font.render(f"${self.barn_upgrade_cost}", True, self.WHITE)
                                barn_upgrade_cost_rect = barn_upgrade_cost.get_rect()
                                barn_upgrade_cost_rect.centerx = self.WIDTH * 0.673
                                barn_upgrade_cost_rect.centery = self.shop_item_y[1]
                                self.screen.blit(barn_upgrade_cost, barn_upgrade_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)

                                self.money -= self.barn_upgrade_cost
                                self.barn_cps *= 2
                                self.barn_upgrade_cost *= 5
                                self.shop()
                            else:
                                # clicking animation
                                red_clicked_rect = self.shop_red_button_clicked.get_rect()
                                red_clicked_rect.centerx = self.WIDTH * 0.673
                                red_clicked_rect.centery = self.shop_item_y[1]
                                self.screen.blit(self.shop_red_button_clicked, red_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                barn_upgrade_cost = font.render(f"${self.barn_upgrade_cost}", True, self.WHITE)
                                barn_upgrade_cost_rect = barn_upgrade_cost.get_rect()
                                barn_upgrade_cost_rect.centerx = self.WIDTH * 0.673
                                barn_upgrade_cost_rect.centery = self.shop_item_y[1]
                                self.screen.blit(barn_upgrade_cost, barn_upgrade_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)
                                self.shop()
                        # if player is buying third item
                        elif self.mouse_y_initial >= self.shop_item_y[2] - self.HEIGHT / 36 and self.mouse_y_initial <= self.shop_item_y[2] + self.HEIGHT / 36:
                            if self.money >= self.pasture_upgrade_cost:
                                # clicking animation
                                green_clicked_rect = self.shop_green_button_clicked.get_rect()
                                green_clicked_rect.centerx = self.WIDTH * 0.673
                                green_clicked_rect.centery = self.shop_item_y[2]
                                self.screen.blit(self.shop_green_button_clicked, green_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                pasture_upgrade_cost = font.render(f"${self.pasture_upgrade_cost}", True, self.WHITE)
                                pasture_upgrade_cost_rect = pasture_upgrade_cost.get_rect()
                                pasture_upgrade_cost_rect.centerx = self.WIDTH * 0.673
                                pasture_upgrade_cost_rect.centery = self.shop_item_y[2]
                                self.screen.blit(pasture_upgrade_cost, pasture_upgrade_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)

                                self.money -= self.pasture_upgrade_cost
                                self.pasture_cps *= 2
                                self.pasture_upgrade_cost *= 5
                                self.shop()
                            else:
                                # clicking animation
                                red_clicked_rect = self.shop_red_button_clicked.get_rect()
                                red_clicked_rect.centerx = self.WIDTH * 0.673
                                red_clicked_rect.centery = self.shop_item_y[2]
                                self.screen.blit(self.shop_red_button_clicked, red_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                pasture_upgrade_cost = font.render(f"${self.pasture_upgrade_cost}", True, self.WHITE)
                                pasture_upgrade_cost_rect = pasture_upgrade_cost.get_rect()
                                pasture_upgrade_cost_rect.centerx = self.WIDTH * 0.673
                                pasture_upgrade_cost_rect.centery = self.shop_item_y[2]
                                self.screen.blit(pasture_upgrade_cost, pasture_upgrade_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)
                                self.shop()
                        # if player is buying last item
                        elif self.mouse_y_initial >= self.shop_item_y[3] - self.HEIGHT / 36 and self.mouse_y_initial <= self.shop_item_y[3] + self.HEIGHT / 36:
                            if self.money >= self.all_upgrade_cost:
                                # clicking animation
                                green_clicked_rect = self.shop_green_button_clicked.get_rect()
                                green_clicked_rect.centerx = self.WIDTH * 0.673
                                green_clicked_rect.centery = self.shop_item_y[3]
                                self.screen.blit(self.shop_green_button_clicked, green_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                all_upgrade_cost = font.render(f"${self.all_upgrade_cost}", True, self.WHITE)
                                all_upgrade_cost_rect = all_upgrade_cost.get_rect()
                                all_upgrade_cost_rect.centerx = self.WIDTH * 0.673
                                all_upgrade_cost_rect.centery = self.shop_item_y[3]
                                self.screen.blit(all_upgrade_cost, all_upgrade_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)

                                self.money -= self.all_upgrade_cost
                                self.house_cps *= 2
                                self.barn_cps *= 2
                                self.pasture_cps *= 2
                                self.all_upgrade_cost *= 5
                                self.shop()
                            else:
                                # clicking animation
                                red_clicked_rect = self.shop_red_button_clicked.get_rect()
                                red_clicked_rect.centerx = self.WIDTH * 0.673
                                red_clicked_rect.centery = self.shop_item_y[3]
                                self.screen.blit(self.shop_red_button_clicked, red_clicked_rect)
                                font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
                                all_upgrade_cost = font.render(f"${self.all_upgrade_cost}", True, self.WHITE)
                                all_upgrade_cost_rect = all_upgrade_cost.get_rect()
                                all_upgrade_cost_rect.centerx = self.WIDTH * 0.673
                                all_upgrade_cost_rect.centery = self.shop_item_y[3]
                                self.screen.blit(all_upgrade_cost, all_upgrade_cost_rect)
                                pygame.display.update()
                                pygame.time.delay(150)
                                self.shop()
            # MAIN SCREEN
            # check if player clicks on the shop button
            if self.mouse_x_initial >= self.WIDTH - 200 - self.WIDTH * 0.013 and self.mouse_x_initial <= self.WIDTH  * 0.987: # if x is inside shop button
                if self.mouse_y_initial >= self.HEIGHT - 200 - self.HEIGHT * 0.023 and self.mouse_y_initial <= self.HEIGHT * 0.977: # if y is inside shop button
                    self.drag = False
                    self.shop_open = True
                    self.shop()
            # start dragging/moving
            elif event.button == 1 and self.drag: # check if user is able to drag 
                self.dragging = True
            # check if player is clicking inside the shop

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
                self.total_shift[0] += movement_x
                self.total_shift[1] += movement_y

                # TESTING
                # self.test_x += movement_x
                # self.test_y += movement_y
                # self.test_x2 += movement_x
                # self.test_y2 += movement_y
                # self.test_x3 += movement_x
                # self.test_y3 += movement_y

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
        font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.027))
        exit_text = font.render("Exit Game?", True, self.BLACK)
        exit_text_rect = exit_text.get_rect()
        exit_text_rect.centerx = self.WIDTH / 2
        exit_text_rect.centery = self.HEIGHT / 2 - 25
        self.screen.blit(exit_text, exit_text_rect)
        # display "NO" text on the left
        font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.024))
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

    def shop(self):
        if self.shop_tab_open == 0: # if the upper tab (buildings) is open
            self.shop_top_rect = self.shop_top.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
            self.screen.blit(self.shop_top, self.shop_top_rect)
            title = "Buildings"
        else: # if the lower tab (upgrades) is open
            self.shop_bottom_rect = self.shop_bottom.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
            self.screen.blit(self.shop_bottom, self.shop_bottom_rect)
            title = "Upgrades"
        # display title text
        font = pygame.font.Font(self.title_font, 50)
        title_text = font.render(title, True, self.WHITE)
        title_text_rect = title_text.get_rect()
        title_text_rect.centerx = self.WIDTH / 2
        title_text_rect.centery = self.HEIGHT / 6
        self.screen.blit(title_text, title_text_rect)
        for i in range(4):
            bar_rect = self.shop_bar.get_rect(center=(self.WIDTH / 2, self.shop_item_y[i]))
            self.screen.blit(self.shop_bar, bar_rect)

        if self.shop_tab_open == 0: # if the upper tab (buildings) is open
            self.buildings_window()
        else:
            self.upgrades_window()
        pygame.display.update()

    def buildings_window(self):
        font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.04))
        font2 = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))

        # house
        house_rect = self.house_shop.get_rect()
        house_rect.centerx = self.WIDTH * 0.286
        house_rect.centery = self.shop_item_y[0]
        self.screen.blit(self.house_shop, house_rect)
        # name
        house_text = font.render("House", True, self.WHITE)
        house_text_rect = house_text.get_rect()
        house_text_rect.centerx = self.WIDTH * 0.37
        house_text_rect.centery = self.shop_item_y[0]
        self.screen.blit(house_text, house_text_rect)
        # cps
        house_cps = font2.render(f"cps: {self.house_cps}", True, self.WHITE)
        house_cps_rect = house_cps.get_rect()
        house_cps_rect.centerx = self.WIDTH / 2
        house_cps_rect.centery = self.shop_item_y[0]
        self.screen.blit(house_cps, house_cps_rect)
        # cost
        if self.money < self.house_cost:
            red_rect = self.shop_red_button.get_rect()
            red_rect.centerx = self.WIDTH * 0.673
            red_rect.centery = self.shop_item_y[0]
            self.screen.blit(self.shop_red_button, red_rect)
        house_cost = font2.render(f"${self.house_cost}", True, self.BLACK)
        house_cost_rect = house_cost.get_rect()
        house_cost_rect.centerx = self.WIDTH * 0.673
        house_cost_rect.centery = self.shop_item_y[0]
        self.screen.blit(house_cost, house_cost_rect)

        # barn
        barn_rect = self.barn_shop.get_rect()
        barn_rect.centerx = self.WIDTH * 0.286
        barn_rect.centery = self.shop_item_y[1]
        self.screen.blit(self.barn_shop, barn_rect)
        # name
        barn_text = font.render("Barn", True, self.WHITE)
        barn_text_rect = barn_text.get_rect()
        barn_text_rect.centerx = self.WIDTH * 0.37
        barn_text_rect.centery = self.shop_item_y[1]
        self.screen.blit(barn_text, barn_text_rect)
        # cps
        barn_cps = font2.render(f"cps: {self.barn_cps}", True, self.WHITE)
        barn_cps_rect = barn_cps.get_rect()
        barn_cps_rect.centerx = self.WIDTH / 2
        barn_cps_rect.centery = self.shop_item_y[1]
        self.screen.blit(barn_cps, barn_cps_rect)
        # cost
        if self.money < self.barn_cost:
            red_rect = self.shop_red_button.get_rect()
            red_rect.centerx = self.WIDTH * 0.673
            red_rect.centery = self.shop_item_y[1]
            self.screen.blit(self.shop_red_button, red_rect)
        barn_cost = font2.render(f"${self.barn_cost}", True, self.BLACK)
        barn_cost_rect = barn_cost.get_rect()
        barn_cost_rect.centerx = self.WIDTH * 0.673
        barn_cost_rect.centery = self.shop_item_y[1]
        self.screen.blit(barn_cost, barn_cost_rect)

        # pasture
        pasture_rect = self.pasture_shop.get_rect()
        pasture_rect.centerx = self.WIDTH * 0.286
        pasture_rect.centery = self.shop_item_y[2]
        self.screen.blit(self.pasture_shop, pasture_rect)
        pasture_text = font.render("Pasture", True, self.WHITE)
        # name
        pasture_text_rect = pasture_text.get_rect()
        pasture_text_rect.centerx = self.WIDTH * 0.37
        pasture_text_rect.centery = self.shop_item_y[2]
        self.screen.blit(pasture_text, pasture_text_rect)
        # cps
        pasture_cps = font2.render(f"cps: {self.pasture_cps}", True, self.WHITE)
        pasture_cps_rect = pasture_cps.get_rect()
        pasture_cps_rect.centerx = self.WIDTH / 2
        pasture_cps_rect.centery = self.shop_item_y[2]
        self.screen.blit(pasture_cps, pasture_cps_rect)
        # cost
        if self.money < self.pasture_cost:
            red_rect = self.shop_red_button.get_rect()
            red_rect.centerx = self.WIDTH * 0.673
            red_rect.centery = self.shop_item_y[2]
            self.screen.blit(self.shop_red_button, red_rect)
        pasture_cost = font2.render(f"${self.pasture_cost}", True, self.BLACK)
        pasture_cost_rect = pasture_cost.get_rect()
        pasture_cost_rect.centerx = self.WIDTH * 0.673
        pasture_cost_rect.centery = self.shop_item_y[2]
        self.screen.blit(pasture_cost, pasture_cost_rect)

        # locked
        locked = font.render("LOCKED", True, self.RED)
        locked_rect = locked.get_rect()
        locked_rect.centerx = self.WIDTH * 0.43
        locked_rect.centery = self.shop_item_y[3]
        self.screen.blit(locked, locked_rect)
        red_rect = self.shop_red_button.get_rect()
        red_rect.centerx = self.WIDTH * 0.673
        red_rect.centery = self.shop_item_y[3]
        self.screen.blit(self.shop_red_button, red_rect)

    def upgrades_window(self):
        font = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.04))
        font2 = pygame.font.Font(self.subtitle_font, int(self.HEIGHT * 0.025))
        
        # house upgrades
        upgrade_rect = self.upgrade.get_rect()
        upgrade_rect.centerx = self.WIDTH * 0.28
        upgrade_rect.centery = self.shop_item_y[0]
        self.screen.blit(self.upgrade, upgrade_rect)
        # text
        house_upgrade = font.render(f"Upgrade Houses", True, self.WHITE)
        house_upgrade_rect = house_upgrade.get_rect()
        house_upgrade_rect.centerx = self.WIDTH * 0.39
        house_upgrade_rect.centery = self.shop_item_y[0]
        self.screen.blit(house_upgrade, house_upgrade_rect)
        # description
        house_description = font2.render("x2 house cps", True, self.WHITE)
        house_description_rect = house_description.get_rect()
        house_description_rect.centerx = self.WIDTH * 0.545
        house_description_rect.centery = self.shop_item_y[0]
        self.screen.blit(house_description, house_description_rect)
        # cost
        if self.money < self.house_upgrade_cost:
            red_rect = self.shop_red_button.get_rect()
            red_rect.centerx = self.WIDTH * 0.673
            red_rect.centery = self.shop_item_y[0]
            self.screen.blit(self.shop_red_button, red_rect)
        house_upgrade_cost = font2.render(f"${self.house_upgrade_cost}", True, self.BLACK)
        house_upgrade_cost_rect = house_upgrade_cost.get_rect()
        house_upgrade_cost_rect.centerx = self.WIDTH * 0.673
        house_upgrade_cost_rect.centery = self.shop_item_y[0]
        self.screen.blit(house_upgrade_cost, house_upgrade_cost_rect)

        # barn upgrades
        upgrade_rect = self.upgrade.get_rect()
        upgrade_rect.centerx = self.WIDTH * 0.28
        upgrade_rect.centery = self.shop_item_y[1]
        self.screen.blit(self.upgrade, upgrade_rect)
        # text
        barn_upgrade = font.render(f"Upgrade Barns", True, self.WHITE)
        barn_upgrade_rect = barn_upgrade.get_rect()
        barn_upgrade_rect.centerx = self.WIDTH * 0.39
        barn_upgrade_rect.centery = self.shop_item_y[1]
        self.screen.blit(barn_upgrade, barn_upgrade_rect)
        # description
        barn_description = font2.render("x2 barn cps", True, self.WHITE)
        barn_description_rect = barn_description.get_rect()
        barn_description_rect.centerx = self.WIDTH * 0.545
        barn_description_rect.centery = self.shop_item_y[1]
        self.screen.blit(barn_description, barn_description_rect)
        # cost
        if self.money < self.barn_upgrade_cost:
            red_rect = self.shop_red_button.get_rect()
            red_rect.centerx = self.WIDTH * 0.673
            red_rect.centery = self.shop_item_y[1]
            self.screen.blit(self.shop_red_button, red_rect)
        barn_upgrade_cost = font2.render(f"${self.barn_upgrade_cost}", True, self.BLACK)
        barn_upgrade_cost_rect = barn_upgrade_cost.get_rect()
        barn_upgrade_cost_rect.centerx = self.WIDTH * 0.673
        barn_upgrade_cost_rect.centery = self.shop_item_y[1]
        self.screen.blit(barn_upgrade_cost, barn_upgrade_cost_rect)

        # pasture upgrades
        upgrade_rect = self.upgrade.get_rect()
        upgrade_rect.centerx = self.WIDTH * 0.28
        upgrade_rect.centery = self.shop_item_y[2]
        self.screen.blit(self.upgrade, upgrade_rect)
        # text
        pasture_upgrade = font.render(f"Upgrade Pastures", True, self.WHITE)
        pasture_upgrade_rect = pasture_upgrade.get_rect()
        pasture_upgrade_rect.centerx = self.WIDTH * 0.39
        pasture_upgrade_rect.centery = self.shop_item_y[2]
        self.screen.blit(pasture_upgrade, pasture_upgrade_rect)
        # description
        pasture_description = font2.render("x2 pasture cps", True, self.WHITE)
        pasture_description_rect = pasture_description.get_rect()
        pasture_description_rect.centerx = self.WIDTH * 0.545
        pasture_description_rect.centery = self.shop_item_y[2]
        self.screen.blit(pasture_description, pasture_description_rect)
        # cost
        if self.money < self.pasture_upgrade_cost:
            red_rect = self.shop_red_button.get_rect()
            red_rect.centerx = self.WIDTH * 0.673
            red_rect.centery = self.shop_item_y[2]
            self.screen.blit(self.shop_red_button, red_rect)
        pasture_upgrade_cost = font2.render(f"${self.pasture_upgrade_cost}", True, self.BLACK)
        pasture_upgrade_cost_rect = pasture_upgrade_cost.get_rect()
        pasture_upgrade_cost_rect.centerx = self.WIDTH * 0.673
        pasture_upgrade_cost_rect.centery = self.shop_item_y[2]
        self.screen.blit(pasture_upgrade_cost, pasture_upgrade_cost_rect)

        # all upgrades
        upgrade_rect = self.upgrade.get_rect()
        upgrade_rect.centerx = self.WIDTH * 0.28
        upgrade_rect.centery = self.shop_item_y[3]
        self.screen.blit(self.upgrade, upgrade_rect)
        # text
        upgrade_all = font.render(f"Upgrade All", True, self.WHITE)
        upgrade_all_rect = upgrade_all.get_rect()
        upgrade_all_rect.centerx = self.WIDTH * 0.39
        upgrade_all_rect.centery = self.shop_item_y[3]
        self.screen.blit(upgrade_all, upgrade_all_rect)
        # description
        all_description = font2.render("x2 all cps", True, self.WHITE)
        all_description_rect = all_description.get_rect()
        all_description_rect.centerx = self.WIDTH * 0.545
        all_description_rect.centery = self.shop_item_y[3]
        self.screen.blit(all_description, all_description_rect)
        # cost
        if self.money < self.pasture_upgrade_cost:
            red_rect = self.shop_red_button.get_rect()
            red_rect.centerx = self.WIDTH * 0.673
            red_rect.centery = self.shop_item_y[3]
            self.screen.blit(self.shop_red_button, red_rect)
        all_upgrade_cost = font2.render(f"${self.all_upgrade_cost}", True, self.BLACK)
        all_upgrade_cost_rect = all_upgrade_cost.get_rect()
        all_upgrade_cost_rect.centerx = self.WIDTH * 0.673
        all_upgrade_cost_rect.centery = self.shop_item_y[3]
        self.screen.blit(all_upgrade_cost, all_upgrade_cost_rect)

    def save(self):
        with open("data.json", "w") as write_file:
            self.data["balance"] = self.money
            self.data["income"] = self.income
            self.data["buildings"] = self.buildings
            self.data["costs"]["house"] = self.house_cost
            self.data["costs"]["barn"] = self.barn_cost
            self.data["costs"]["pasture"] = self.pasture_cost
            self.data["cps"]["house"] = self.house_cps
            self.data["cps"]["barn"] = self.barn_cps
            self.data["cps"]["pasture"] = self.pasture_cps
            self.data["upgrade costs"]["house"] = self.house_upgrade_cost
            self.data["upgrade costs"]["barn"] = self.barn_upgrade_cost
            self.data["upgrade costs"]["pasture"] = self.pasture_upgrade_cost
            self.data["upgrade costs"]["all"] = self.all_upgrade_cost
            json.dump(self.data, write_file)
                
    def on_execute(self):
        self.loading()
        self.display()
        while self.running:
            self.blit_money_balance()
            if self.shop_open and self.exiting == False:
                self.shop()
            pygame.display.update()
            for event in pygame.event.get():
                self.check_event(event)
            self.clock.tick(self.FPS)

start = Game()
start.on_execute()
