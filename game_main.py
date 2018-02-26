import pygame
import random
# Import tile draw functions
# noinspection PyUnresolvedReferences
import game_tiles as gt


# GUI classes from previous lessons
class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)


class Label:
    def __init__(self, rect, text, text_color, background_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        if background_color == -1:
            self.bgcolor = 0
        else:
            self.bgcolor = pygame.Color(background_color)
        if str(text_color)[0].isalpha():
            self.font_color = pygame.Color(text_color)
        else:
            self.font_color = text_color
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.SysFont('courier', self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        if self.bgcolor:
            surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)


class Button(Label):
    def __init__(self, rect, text, action):
        super().__init__(rect, text, (66, 66, 66), -1)
        self.action = action
        self.bgcolor = (205, 203, 189)
        # при создании кнопка не нажата
        self.pressed = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = (255, 233, 189)
            color2 = (255, 233, 189)
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = (255, 233, 189)
            color2 = (255, 233, 189)
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom),
                         2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos[0], event.pos[1])
            if self.pressed:
                if callable(self.action):
                    self.action()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False


# Game board class
class Board:
    def __init__(self, size, tl_pos, slot=0, score=0):
        self.surface = None
        self.slot = slot
        self.score = score
        self.tl_pos = tl_pos
        self.size = size
        self.tiles = [list('0' * size)[:] for _ in range(size)]

    # Start the game if called in a button
    def __call__(self, *args, **kwargs):
        global brd
        global gamestate
        brd = self
        gamestate = 3
        change_screen_size(self.size)

    # Clear this board's save file
    def clear(self):
        clear_save(self.slot)

    # Save this board
    def save(self):
        save('saves/savegame_' + str(self.slot) + '.save', self)

    # Rendering every tile
    def render(self, srf):
        y = self.tl_pos[1]
        for i in range(len(self.tiles)):
            x = self.tl_pos[0]
            for j in range(len(self.tiles[i])):
                gt.render(srf, self.tiles[i][j], (x, y))
                x += 100
            y += 100

    # Adding a new tile
    def add_random(self):
        empty_spot = False
        # Search if there is an empty spot
        for line in self.tiles:
            if '0' in line:
                empty_spot = True
        if empty_spot:
            empty_spot = False
            while not empty_spot:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                if self.tiles[y][x] == '0':
                    # noinspection PyUnusedLocal
                    emptsy_spot = True
                    # Determine the value of added tile
                    a = random.randrange(0, 100)
                    if a > 80:
                        self.tiles[y][x] = '2'
                    else:
                        self.tiles[y][x] = '1'
                    return None
        else:
            # If no empty spot return something
            return -1

    # Move every tile
    def move(self, direction):
        if direction == 'left':
            for c in range(self.size - 1):
                for i in range(self.size):
                    for j in range(1, self.size):
                        if self.tiles[i][j - 1] == '0':
                            self.tiles[i][j - 1] = str(self.tiles[i][j])
                            self.tiles[i][j] = '0'
                        if self.tiles[i][j] != '0' and self.tiles[i][j - 1] == self.tiles[i][j]:
                            self.combine(j - 1, i)
                            self.tiles[i][j] = '0'
        elif direction == 'right':
            for c in range(self.size - 1):
                for i in range(self.size):
                    for j in range(self.size - 2, -1, -1):
                        if self.tiles[i][j + 1] == '0':
                            self.tiles[i][j + 1] = str(self.tiles[i][j])
                            self.tiles[i][j] = '0'
                        elif self.tiles[i][j] != '0' and self.tiles[i][j + 1] == self.tiles[i][j]:
                            self.combine(j + 1, i)
                            self.tiles[i][j] = '0'
        elif direction == 'up':
            for c in range(self.size - 1):
                for i in range(1, self.size):
                    for j in range(self.size):
                        if self.tiles[i - 1][j] == '0':
                            self.tiles[i - 1][j] = str(self.tiles[i][j])
                            self.tiles[i][j] = '0'
                        elif self.tiles[i][j] != '0' and self.tiles[i - 1][j] == self.tiles[i][j]:
                            self.combine(j, i - 1)
                            self.tiles[i][j] = '0'
        elif direction == 'down':
            for c in range(self.size - 1):
                for i in range(self.size - 2, -1, -1):
                    for j in range(self.size):
                        if self.tiles[i + 1][j] == '0':
                            self.tiles[i + 1][j] = str(self.tiles[i][j])
                            self.tiles[i][j] = '0'
                        elif self.tiles[i][j] != '0' and self.tiles[i + 1][j] == self.tiles[i][j]:
                            self.combine(j, i + 1)
                            self.tiles[i][j] = '0'
        if self.add_random() is not None:
            return -1
        else:
            return None

    # Upgrade tile and increase score
    def combine(self, x, y):
        self.tiles[y][x] = str(gt.tile_ladder[gt.tile_ladder.index(self.tiles[y][x]) + 1])
        self.score += int(2 ** gt.tile_ladder.index(self.tiles[y][x]))


# Function to load a board from a save file
def load(name):
    f = open(name, mode='r', encoding='utf8')
    data = f.readlines()
    f.close()
    # If save is empty return None
    if not data:
        return None
    size = int(data[0].strip().split()[0])
    if size:
        # If save is not empty return saved board
        tiles = list(map(lambda x: list(x.strip()), data[1:size + 1]))
        b = Board(size, (40, 120))
        b.tiles = tiles[:]
        b.slot = int(name[:][-6])
        b.score = int(data[0].strip().split()[1])
        return b
    else:
        # If save is empty return None
        return None


# Function to save a board to a save file
def save(name, b):
    f = open(name, mode='w', encoding='utf8')
    f.write(str(b.size) + ' ' + str(b.score) + '\n')
    for line in b.tiles:
        f.write(''.join(line) + '\n')
    f.close()
    global gamestate
    gamestate = 1
    # Reload save selection GUI
    global gui_ss
    gui_ss.elements = []
    gui_ss.add_element(Label(((width / 2) - 225, 20, 370, 50), "Select save slot", 'black', -1))
    check_save(1)
    check_save(2)
    check_save(3)
    gui_ss.add_element(Button((15, height - 45, 110, 40), 'Back', change_state_0))


# Functions to change gamestate
# Used only in buttons
def change_state_0():
    global gamestate
    gamestate = 0


def change_state_1():
    global gamestate
    global width
    gamestate = 1


def change_state_2():
    global gamestate
    gamestate = 2


def change_state_3():
    global gamestate
    gamestate = 3


def change_state_4():
    global gamestate
    gamestate = 4


# Function to change screen size to fit a board with size n
def change_screen_size(bw):
    global width, height
    global screen_size
    height = 240 + bw * 100
    width = 80 + bw * 100
    screen_size = width, height
    global surface
    surface = pygame.display.set_mode(screen_size)


# Functions to set new board size
# Used only in buttons
def ss4():
    global brd
    global gamestate
    brd.size = 4
    brd.tiles = [list('0' * 4)[:] for _ in range(4)]
    gamestate = 3
    change_screen_size(4)


def ss5():
    global brd
    global gamestate
    brd.size = 5
    brd.tiles = [list('0' * 5)[:] for _ in range(5)]
    gamestate = 3
    change_screen_size(5)


def ss6():
    global brd
    global gamestate
    brd.size = 6
    brd.tiles = [list('0' * 6)[:] for _ in range(6)]
    gamestate = 3
    change_screen_size(6)


# Function to check state of save files
def check_save(save):
    global width
    b = load('saves/savegame_' + str(save) + '.save')
    if b is None:
        # If save is empty, add an otion to create one
        b = Board(4, (40, 120), save)
        global brd
        brd = b
        gui_ss.add_element(Button(((width / 2) - 175, 25 + save * 100, 370, 40), "Empty slot", change_state_4))
    else:
        # If save is not empty, add an option to load it
        b.slot = save
        gui_ss.add_element(Button(((width / 2) - 175, 25 + save * 100, 370, 40), "Save slot " + str(save), b))
        # Board size display
        gui_ss.add_element(
            Label(((width / 2) - 175, 75 + save * 100, 370, 30), str(b.size) + 'X' + str(b.size), (50, 50, 50), -1))
        # Add an option to clear it
        gui_ss.add_element(Button(((width / 2) - 105, 75 + save * 100, 90, 30), 'Clear', b.clear))
        # Show save score
        gui_ss.add_element(Label(((width / 2) + 15, 75 + save * 100, 370, 30), str(b.score), (50, 50, 50), -1))


# Save reset function
def clear_save(save):
    f = open('saves/savegame_' + str(save) + '.save', mode='w', encoding='utf8')
    f.write('0')
    # Reload save selection GUI
    gui_ss.elements = []
    gui_ss.add_element(Label(((width / 2) - 225, 20, 370, 50), "Select save slot", 'black', -1))
    check_save(1)
    check_save(2)
    check_save(3)
    gui_ss.add_element(Button((15, height - 45, 110, 40), 'Back', change_state_0))


gamestate = 0

# Standard board
brd = Board(4, (40, 120))

# Window settings
width, height = 480, 640
screen_size = width, height
pygame.init()
surface = pygame.display.set_mode(screen_size)
pygame.display.flip()

# Title screen gui elements
gui_ts = GUI()
gui_ts.add_element(Label(((width / 2) - 155, 70, 80, 50), "py", 'grey', -1))
gui_ts.add_element(Label(((width / 2) - 95, 50, 190, 80), "2048", 'black', -1))
gui_ts.add_element(Button(((width / 2) - 85, 225, 170, 70), "Play", change_state_1))
gui_ts.add_element(Button(((width / 2) - 85, 325, 170, 70), "Help", change_state_2))
# gui_ts.add_element(Button(((width / 2) - 225, 425, 450, 70), "Leaderboard", change_state_4))

# Save slot selection gui elements
gui_ss = GUI()
gui_ss.add_element(Label(((width / 2) - 225, 20, 370, 50), "Select save slot", 'black', -1))
check_save(1)
check_save(2)
check_save(3)
gui_ss.add_element(Button((15, height - 45, 110, 40), 'Back', change_state_0))

# Size selection gui elements
gui_szs = GUI()
gui_szs.add_element(Label(((width / 2) - 225, 20, 370, 45), "Select board size", 'black', -1))
gui_szs.add_element(Button(((width / 2) - 40, 175, 80, 40), '4X4', ss4))
gui_szs.add_element(Button(((width / 2) - 40, 275, 80, 40), '5X5', ss5))
gui_szs.add_element(Button(((width / 2) - 40, 375, 80, 40), '6X6', ss6))

# In-game GUI
gui_ing = GUI()
gui_ing.add_element(Button((15, 15, 110, 40), 'Back', brd.save))
gui_ing.add_element(Label((90, 70, 80, 50), "Score: ", 'black', -1))

# Help GUI
gui_h = GUI()
gui_h.add_element(Label(((width / 2) - 225, 70, 370, 25), "To win you need to make a 2048 tile", 'black', -1))
gui_h.add_element(
    Label(((width / 2) - 225, 120, 370, 25), "You can move all tiles at once ", 'black', -1))
gui_h.add_element(
    Label(((width / 2) - 225, 145, 370, 25), "using arrow keys", 'black', -1))
gui_h.add_element(
    Label(((width / 2) - 225, 170, 370, 25), "When to tiles with the same number ", 'black', -1))
gui_h.add_element(
    Label(((width / 2) - 225, 195, 370, 25), "collide they combine", 'black', -1))
gui_h.add_element(
    Label(((width / 2) - 225, 220, 370, 25), "Score is increased by the number ", 'black', -1))
gui_h.add_element(
    Label(((width / 2) - 225, 245, 370, 25), "on the new tile after combining", 'black', -1))
gui_h.add_element(Button((15, height - 45, 110, 40), 'Back', change_state_0))

# Clock setup
fps = 60
clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Saving the game if window is closed
            if gamestate == 3:
                save('saves/savegame_' + str(brd.slot) + '.save', brd)
            pygame.quit()
            exit(0)
        elif event.type == pygame.KEYDOWN:
            # Tile movement events
            if gamestate == 3:
                if event.key == pygame.K_LEFT:
                    brd.move('left')
                elif event.key == pygame.K_RIGHT:
                    brd.move('right')
                elif event.key == pygame.K_UP:
                    brd.move('up')
                elif event.key == pygame.K_DOWN:
                    brd.move('down')
                # elif event.key == pygame.K_INSERT:
                #     brd.add_random()
                # elif event.key == pygame.K_DELETE:
                #     brd.tiles = [list('0' * 4)[:] for _ in range(4)]
        # GUI events
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            if gamestate == 0:
                gui_ts.get_event(event)
            elif gamestate == 1:
                gui_ss.get_event(event)
            elif gamestate == 2:
                gui_h.get_event(event)
            elif gamestate == 3:
                gui_ing.get_event(event)
            elif gamestate == 4:
                gui_szs.get_event(event)

    # Background color fill
    surface.fill((255, 233, 189))

    # GUI rendering
    if gamestate == 0:
        gui_ts.render(surface)
    elif gamestate == 1:
        gui_ss.render(surface)
    elif gamestate == 2:
        gui_h.render(surface)
    elif gamestate == 3:
        gui_ing = GUI()
        gui_ing.add_element(Button((15, 15, 110, 40), 'Back', brd.save))
        gui_ing.add_element(Label((90, 70, 80, 50), "Score: " + str(brd.score), 'black', -1))

        gui_ing.render(surface)
        brd.render(surface)
    elif gamestate == 4:
        gui_szs.render(surface)

    clock.tick(fps)
    pygame.display.flip()
