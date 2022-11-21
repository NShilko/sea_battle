import numpy as np  # for create field matrix and work with it
import random
import os  # for remove all info from console

DEBUG = False  # to detect pc ships on the field

os.system("")  # enable colors

nl = '\n'
SHIP_MARK = '□'
SHIP_DEATH = '■'
SHIP_AURA = '-'
SHIP_DEATH_AURA = 'X'
MISS_MARK = 'X'
dic_ships_spawn = {  # spawn the ships using this chain
    1: 'AAA',
    2: 'AAA',
    3: 'BB',
    4: 'BB',
    5: 'BB',
    6: 'C',
    7: 'C',
    8: 'C',
    9: 'C'
}
dic_ships_name = {
    1: '3-х палубный',
    2: '3-х палубный',
    3: '3-х палубный',
    4: '2-х палубный',
    5: '2-х палубный',
    6: '1 палубный',
    7: '1 палубный',
    8: '1 палубный',
    9: '1 палубный'
}
dic_color = {
    'reset': '\033[0m',
    'green': '\033[92m',
    'yellow': '\033[33m',
    'red': '\033[31m',
    'purple': '\033[35m',
    'white': '\033[37m',
}
INSTRUCTION = '''
                        Перед вами поле 9x9, где вы должны будете разместить свои корабли
                            либо вручную, либо автоматически. Всего у вас 9 кораблей:
                                             3-х палубный - 2 штуки
                                             2-х палубный - 3 штуки
                                              1 палубный - 4 штуки

        Расставляя корабли вы должны знать, что нельзя, чтобы корабли соприкасались ни боками, ни, даже, уголками. 
                        Как минимум одна клетка между ними должна быть обязательно.

            Цель игры: потопить флот противника из пяти кораблей, прежде чем противник потопит ваш флот.
                
'''

# ------ MAIN OPTION PROP ---------


class Game:
    x = 0  # need to send coordination to spawn the ships
    y = 0
    is_player_turn = True
    winner = ''

    def game_launched(self):
        pc_field.create_new_field()
        player_field.create_new_field()
        is_player_turn = True
        options.winner = ''
        player.reset_data()
        pc.reset_data()

    def clear_window(self):
        os.system('cls')  # Delete everything from window
        #pass

    def colored(self, text, color):  # make color for text
        return f'{dic_color[color]}{text}{dic_color["reset"]}'

    def main_menu(self):
        self.clear_window()  # remove all info from console
        print(nl * 7)
        align_help_small = " " * 17
        title = f'''{dic_color['yellow']}
        {align_help_small} ____  ____   __     ____   __  ____  ____  __    ____ 
        {align_help_small}/ ___)(  __) / _\   (  _ \ / _\(_  _)(_  _)(  )  (  __)
        {align_help_small}\___ \ ) _) /    \   ) _ (/    \ )(    )(  / (_/\ ) _) 
        {align_help_small}(____/(____)\_/\_/  (____/\_/\_/(__)  (__) \____/(____)
                                          {dic_color['reset']}'''
        print(title)
        print(nl * 3)
        self.game_launched()
        self.center_input('main_menu')

    def show_instruction(self):
        self.clear_window()
        print(nl * 5)
        print(f'{self.colored("----- ПРАВИЛА ИГРЫ -----", "yellow")}'.center(121))
        print(INSTRUCTION)
        print(nl*3)
        self.center_input('instruction')

    # -------- INPUT ----------

    def center_input(self, kind, ship=0):
        dic_input_txt = {
            'spawn_cell': f'''
            -- {self.colored('Выберите клетку, куда вы хотите разместить ваш ','yellow')}{self.colored(dic_ships_name[ship+1], 'green')}{self.colored(' корабль','yellow')} --
            -- Вначале запишите столбик [A-F], а затем строчку [0-6] --
            - [ Q ] Вернуться в меню
            - [ R ] Перезапустить игру
            - [ L ] Расставить отсальные корабли случайно (осталось: {9-ship})
            - [ H ] Отключить подсказки во время строительства кораблей
            -----------------------------------: ''',
            'spawn_position': f'''
            -- Выберите как именно вы хотите расположить корабль --
            - [ {self.colored('V','purple')} ] Вертикально
            - [ {self.colored('H','yellow')} ] Горизонтально
            - [ N ] Отмена
            -----------------------------------: ''',
            'spawn_position_x': '''
            -- Выберите как именно вы хотите расположить корабль --
            - [ H ] Горизонтально
            - [ N ] Отмена
            -----------------------------------: ''',
            'spawn_position_y': '''
            -- Выберите как именно вы хотите расположить корабль --
            - [ V ] Вертикально
            - [ N ] Отмена
            -----------------------------------: ''',
            'fight': '''
            -- Выберите ячеку, куда вы хотите совершить выстрел --
            -- Вначале запишите столбик [A-F], а затем строчку [0-6] --
            - [ Q ] Вернуться в меню
            - [ R ] Перезапустить игру
            -----------------------------------: ''',
            'end_game': f'''
            ------------- ИГРА ЗВЕРШЕНА --------------
            --- Победитель --- [ {self.colored(options.winner, 'yellow')} ] ---
            --- Нажмите Enter, чтобы продолжить! ---
            -----------------------------------: ''',
            'main_menu': '''
            ------------- ГЛАВНОЕ МЕНЮ --------------
            
            -- Добро пожаловать. Что будем делать? --
            - [ N ] Новая игра
            - [ E ] Выход из игры
            -----------------------------------: ''',
            'instruction': f'''
            --- Нажмите Enter, чтобы продолжить! ---
            -----------------------------------:
            ''',

        }
        result = input(dic_input_txt[kind]).upper()
        if kind == 'spawn_cell':
            if result:
                if len(result) > 2:
                    raise ErrSpawn('Вы ввели слишком длинную команду', ship=ship)
                elif len(result) > 1:
                    answer = list(result)
                    if answer[1].isnumeric():
                        if answer[0] in Field.LETTERS and int(answer[1]) in list(range(1, 10)):
                            self.x = Field.LETTERS.index(answer[0])
                            self.y = int(answer[1]) - 1
                            return player_field.check_field_spawn(x=self.x, y=self.y, ship=ship+1)
                        else:
                            raise ErrSpawn(f'Поля [ {"".join(answer)} ] не существует', ship=ship)
                    else:
                        raise ErrSpawn('Вторым символом необходимо указать номер строки', ship=ship)
                else:
                    if result == 'Q':
                        self.main_menu()
                    if result == 'R':
                        self.game_launched()
                        self.print_field('spawn_cell')
                    if result == 'L':
                        return player_field.ship_random_place(ship+1)
                    if result == 'H':
                        player.hep_vis_spawn = not player.hep_vis_spawn  # show or hide closed cells for building
                        options.print_field('spawn_cell')
                    else:
                        raise ErrSpawn('Такой команды не существует', ship=ship)
            else:
                raise ErrSpawn('Вы забыли ввести команду', ship=ship)

        elif kind == 'spawn_position':
            if result:
                if result == 'V':
                    return player_field.check_field_spawn(x=self.x, y=self.y, is_spawn=True, is_x=False, ship=ship)
                if result == 'H':
                    return player_field.check_field_spawn(x=self.x, y=self.y, is_spawn=True, is_x=True, ship=ship)
                if result == 'N':
                    player_field.remove_help_char('')
                    options.print_field('spawn_cell', ship=ship-1)
                else:
                    raise ErrPosition('Такой команды не существует', ship=ship - 1)
            else:
                raise ErrPosition('Вы забыли указать команду', ship=ship)
        elif kind == 'spawn_position_y':
            if result:
                if result == 'V':
                    return player_field.check_field_spawn(x=self.x, y=self.y, is_spawn=True, is_x=False, ship=ship)
                if result == 'N':
                    player_field.remove_help_char('')
                    options.print_field('spawn_cell', ship=ship-1)
                else:
                    raise ErrPosition('Такой команды не существует', ship=ship - 1)
            else:
                raise ErrPosition('Вы забыли указать команду', ship=ship)
        elif kind == 'spawn_position_x':
            if result:
                if result == 'H':
                    return player_field.check_field_spawn(x=self.x, y=self.y, is_spawn=True, is_x=True, ship=ship)
                if result == 'N':
                    player_field.remove_help_char('')
                    options.print_field('spawn_cell', ship=ship-1)
                else:
                    raise ErrPosition('Такой команды не существует', ship=ship - 1)
            else:
                raise ErrPosition('Вы забыли указать команду', ship=ship)

        elif kind == 'fight':
            if result:
                if result == 'Q':
                    self.main_menu()  # Go to Main Menu
                elif result == 'R':
                    self.game_launched()
                    self.print_field('spawn_cell')
                elif len(result) > 2:
                    raise LockedFire('Вы ввели неверную команду')
                elif len(result) > 1:
                    answer = list(result)
                    if answer[1].isnumeric():
                        if answer[0] in Field.LETTERS and int(answer[1]) in list(range(1, 10)):
                            self.x = Field.LETTERS.index(answer[0])
                            self.y = int(answer[1]) - 1
                            self.make_fire(pc_field.my_range, self.x, self.y)
                        else:
                            raise LockedFire(f'Поля [ {"".join(answer)} ] не существует')
                    else:
                        raise LockedFire('Вторым символом необходимо указать номер строки')
                else:
                    raise LockedFire('Вы ввели неверную команду')
            else:
                raise LockedFire('Вы забыли ввести команду')

        elif kind == 'main_menu':
            def new_game_start():
                player.score = 0
                pc.score = 0
                self.show_instruction()
            if result:
                if result == 'N':
                    new_game_start()
                elif result == 'E':
                    quit()
                else:
                    self.main_menu()
            else:
                new_game_start()
        elif kind == 'end_game':
            self.game_launched()
            self.print_field('spawn_cell')
        elif kind == 'instruction':
            if result:
                self.print_field('spawn_cell')
            else:
                self.print_field('spawn_cell')
        else:
            options.print_field(kind, 'Вы забыли ввести команду')

    # ----- PRINT FIELD --------

    def print_field(self, input_kind='', err='', ship=0):
        self.clear_window()

        def make_str(arr, kind, is_player=True, num=0):

            if kind == 'abc':
                return ' │ '.join(arr)
            elif kind == 'cell':
                if player.hep_vis_spawn:
                    out = ' │ '.join(arr)
                else:
                    out = ' │ '.join(arr).replace('-', ' ')
                if is_player:
                    # make live ships - green, dead ships - red
                    colored_out = out.replace(SHIP_MARK, self.colored(SHIP_MARK, 'green')).replace(SHIP_DEATH, self.colored(SHIP_DEATH, 'red'))
                    colored_out = colored_out.replace('V', self.colored('V', 'purple')).replace('H', self.colored('H', 'yellow'))
                else:
                    if DEBUG:  # you can edit it in line 5
                        colored_out = out.replace(SHIP_MARK, self.colored(SHIP_MARK, 'green')).replace(SHIP_DEATH, self.colored(SHIP_DEATH, 'red'))
                    else:  # make hide live ships and dead ships - red
                        colored_out = out.replace(SHIP_MARK, ' ').replace(SHIP_DEATH, self.colored(SHIP_DEATH, 'red'))
                return colored_out

        def make_cell(num):
            return f"{small_space}{num + 1} │ {make_str(player_field.my_range[num], 'cell', num=num)} {big_space}{num + 1} | {make_str(pc_field.my_range[num], 'cell', False, num)}"

        small_space = ' ' * 5
        big_space = (' ' * 10) + '┊' + (' ' * 10)
        small_line = '─' * 38
        long_line = small_space + small_line + big_space + small_line
        head = ' ' * 27 + f'ИГРОК [ {player.score} ]' + ' ' * 47 + f'КОМПЬЮТЕР [ {pc.score} ]'
        print(head)
        field_to_show = f'''
        {small_space}  │ {make_str(Field.LETTERS, 'abc')} {big_space}  │ {make_str(Field.LETTERS, 'abc')}
        {long_line}
        {make_cell(0)}
        {long_line}
        {make_cell(1)}
        {long_line}
        {make_cell(2)}
        {long_line}
        {make_cell(3)}
        {long_line}
        {make_cell(4)}
        {long_line}
        {make_cell(5)}
        {long_line}
        {make_cell(6)}
        {long_line}
        {make_cell(7)}
        {long_line}
        {make_cell(8)}
        '''
        print(field_to_show)
        if err:
            print(f'[ОШИБКА] {err}!'.center(120))

        options.center_input(kind=input_kind, ship=ship)

    # ----------- FIRE AND TURN --------

    def end_turn(self, end=False):
        if end:  # game is over
            if self.is_player_turn:
                options.winner = 'ИГРОК'
                player.score += 1
            else:
                pc.score += 1
                options.winner = 'КОМПЬЮТЕР'
            options.print_field('end_game')
        else:  # change the turn
            self.is_player_turn = not self.is_player_turn
            if self.is_player_turn:
                self.print_field('fight')
            else:
                self.ai_make_turn()

    def detect_ship_on_fire(self, player_dic, x, y):
        coordination = str(y) + str(x)
        coordination_index = None
        for idx, i in enumerate(list(player_dic.values())):
            if coordination in i:
                coordination_index = idx + 1  # detect in dic witch ship is on fire
        ship = list(player_dic[coordination_index])  # get all coordination about this ship
        ship.remove(coordination)  # remove one coordination of ship (one cell is destroyed)
        if self.is_player_turn:
            pc_field.my_range[y][x] = SHIP_DEATH  # print death cell on pc field
        else:
            player_field.my_range[y][x] = SHIP_DEATH  # print death on player field
        if ship:  # if ship have some other coordination (living cells)
            player_dic[coordination_index] = ship  # update dir with remaining living cells
            return True  # Game is not end -> next turn
        else:
            if self.is_player_turn:  # if ship is full destroyed -> make death aura around him. For PC
                first_cell = list(pc.dic_ships_position[coordination_index])[0]
                first_x = int(list(first_cell)[1])
                first_y = int(list(first_cell)[0])
                ship_len = len(list(pc.dic_ships_position[coordination_index]))
                pc.ships_count -= 1  # and let change ships count in the pc collection
                pc_field.make_ship_aura(first_x, first_y, ship_len, pc.dic_ship_is_horizontal[coordination_index], True)
                pc.ship_on_fire = False
                pc.ship_on_fire_location = []
                return pc.ships_count  # have some living ships? Let change the turn
            else:  # same for player
                first_cell = list(player.dic_ships_position[coordination_index])[0]
                first_x = int(list(first_cell)[1])
                first_y = int(list(first_cell)[0])
                ship_len = len(list(player.dic_ships_position[coordination_index]))
                player.ships_count -= 1  # and let change ships count in the player collection
                player_field.make_ship_aura(first_x, first_y, ship_len, player.dic_ship_is_horizontal[coordination_index], True)
                player.ship_on_fire = False
                player.ship_on_fire_location = []
                return player.ships_count  # have some living ships? Let change the turn

    def make_fire(self, field, x, y, is_ai=False):
        if field[y][x] == SHIP_DEATH_AURA:  # try to attack neutralized cell
            if is_ai:
                return False
            else:
                raise LockedFire('По этому полю нет смысла вести огонь')
        elif field[y][x] == SHIP_MARK:  # try to attack ship cell
            if self.is_player_turn:
                pc.ship_on_fire = True
                pc.ship_on_fire_location.append(str(y) + str(x))
                is_end = self.detect_ship_on_fire(pc.dic_ships_to_fire, x, y)
            else:
                player.ship_on_fire_location.append(str(y) + str(x))
                player.ship_on_fire = True
                is_end = self.detect_ship_on_fire(player.dic_ships_to_fire, x, y)
            self.end_turn(not bool(is_end))  # if you have some living ships -> next turn
        elif field[y][x] == ' ':  # try to attack free cell
            field[y][x] = MISS_MARK
            self.end_turn()
        else:
            if is_ai:
                return False
            else:
                raise LockedFire('По этому полю нет смысла вести огонь')

    # ----------- AI ------------

    def ai_smart_attack(self):
        def prepare_fire(x, y):
            pc.not_to_use_in_shot.append(y + x)  # collect pc shots to cache
            if not self.make_fire(player_field.my_range, int(x), int(y), True):
                self.ai_make_turn()

        def cell_to_shot_validation(var, is_more=False, is_x=False):  # where can pc shoot?
            if var >= 0:
                coordination = str(var).zfill(2)  # x -> xx
                if is_more:
                    if int(list(coordination)[int(is_x)]) >= 0 and coordination not in pc.not_to_use_in_shot:
                        choose.append(coordination)
                else:
                    if int(list(coordination)[int(is_x)]) < 9 and coordination not in pc.not_to_use_in_shot:
                        choose.append(coordination)

        choose = []  # collect possible cells to attack
        if len(player.ship_on_fire_location) == 2:  # two cells of player's ship are damage
            minimum = int(min(player.ship_on_fire_location))
            maximum = int(max(player.ship_on_fire_location))
            different = maximum - minimum
            if different >= 10:  # is player's ship on vertical position
                cell_to_shot_validation(minimum - 10, True, False)  # UP >= 0
                cell_to_shot_validation(maximum + 10, False, False)  # DOWN < 9
            elif different < 10:  # is player's ship on horizontal position
                cell_to_shot_validation(minimum - 1, True, True)   # Left >= 0
                cell_to_shot_validation(maximum + 1, False, True)  # Right < 9
        else:  # one cell of player's ship are damage
            cell_to_shot_validation(int(player.ship_on_fire_location[0]) - 1, True, True)  # left >= 0
            cell_to_shot_validation(int(player.ship_on_fire_location[0]) + 1, False, True)  # right < 9
            cell_to_shot_validation(int(player.ship_on_fire_location[0]) - 10, True, False)  # up >= 0
            cell_to_shot_validation(int(player.ship_on_fire_location[0]) + 10, False, False)  # down < 9

        pick = random.choice(choose)  # get one of possible cells
        pick_list = list(str(pick))
        prepare_fire(pick_list[1], pick_list[0])
                    
    def ai_make_turn(self):
        if player.ship_on_fire:
            self.ai_smart_attack()
        else:
            self.ai_random_cell_attack()

    def ai_random_cell_attack(self):
        x = random.randrange(0, 9)
        y = random.randrange(0, 9)
        coordination = str(y) + str(x)
        if coordination in pc.not_to_use_in_shot:  # cell is in cache? Try again
            self.ai_random_cell_attack()
        else:
            pc.not_to_use_in_shot.append(coordination)  # collect pc shots to cache
            if not self.make_fire(player_field.my_range, x, y, True):
                self.ai_make_turn()

# ------------ PLAYER PROP --------------


class Player:
    def __init__(self, score=0, is_ai=False, help_vision=False):
        self.score = score
        self.is_ai = is_ai
        self.hep_vis_spawn = help_vision
        self.dic_ships_position = {}  # collect all cells of ships
        self.dic_ships_to_fire = {}  # content only living cells of ships
        self.dic_ship_is_horizontal = {}  # horizontal or vertical position of spawned ships
        self.not_to_use_in_shot = []  # collect all cells with last fires
        self.ready_for_battle = False
        self.ships_count = 9
        self.ship_on_fire = False
        self.ship_on_fire_location = []

    def reset_data(self):
        self.dic_ships_position = {}  # collect all cells of ships
        self.dic_ships_to_fire = {}  # content only living cells of ships
        self.dic_ship_is_horizontal = {}  # horizontal or vertical position of spawned ships
        self.not_to_use_in_shot = []  # collect all cells with last fires
        self.ready_for_battle = False
        self.ships_count = 9
        self.ship_on_fire = False

# ---------------- FIELD PROP -----------


class Field:
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    def __init__(self):
        self.not_to_use_in_random = []  # need to create cache occupied cells for spawn
        self.my_range = []

    def create_new_field(self):
        self.my_range = np.full((len(self.LETTERS), len(self.LETTERS)), ' ', dtype=str)

    def remove_help_char(self, char='-'):
        if char:
            new_matrix = np.char.replace(self.my_range, char, ' ')
        else:
            new_matrix = np.char.replace(self.my_range, 'V', ' ')
            self.my_range = new_matrix
            new_matrix = np.char.replace(self.my_range, 'H', ' ')
        self.my_range = new_matrix

    def ship_random_place(self, ship):
        def append_to_not_use_cache(x, y):
            self.not_to_use_in_random.append(str(y) + str(x))

        x = random.randrange(0, 9)
        y = random.randrange(0, 9)
        if str(y) + str(x) not in self.not_to_use_in_random:
            is_horizontal = bool(random.randrange(0, 2))
            if self.my_range[y][x] == ' ':  # if cell is empty -> try to spawn the ship
                # is it possible to send the ship in this direction?
                if self.check_field_spawn(x=x, y=y, is_x=is_horizontal, ship=ship, is_random=True):
                    self.check_field_spawn(x=x, y=y, is_spawn=True, is_x=is_horizontal, ship=ship, is_random=True)
                # no? is it possible to send the ship in another direction?
                else:
                    if self.check_field_spawn(x=x, y=y, is_x=not is_horizontal, ship=ship, is_random=True):
                        self.check_field_spawn(x=x, y=y, is_spawn=True, is_x=not is_horizontal, ship=ship, is_random=True)
                    # same no? Ok, lets random it again
                    else:
                        append_to_not_use_cache(x, y)
                        self.ship_random_place(ship=ship)
            else:  # it's not free cell -> let cache it and try again
                append_to_not_use_cache(x, y)
                self.ship_random_place(ship=ship)
        else:
            # it's in cache? Try again
            self.ship_random_place(ship=ship)

    def make_ship_aura(self, x, y, ship_len, is_horizontal, is_attack=False):
        mark = SHIP_AURA
        if is_attack:
            mark = SHIP_DEATH_AURA
        else:
            self.remove_help_char('')
        if is_horizontal:
            for j in range(0, ship_len + 2):  # all cell ship that is closed (1 before ship and 1 to after ship)
                if 0 <= x - 1 + j < 9:
                    if x - 1 + j >= 0 and self.my_range[y][x - 1 + j] == ' ':  # up and down
                        self.my_range[y][x - 1 + j] = mark
                    if y - 1 >= 0:
                        if y - 1 + j >= 0 and self.my_range[y - 1][x - 1 + j] == ' ':  # left
                            self.my_range[y - 1][x - 1 + j] = mark
                    if y + 1 < 9:
                        if y - 1 + j >= 0 and self.my_range[y + 1][x - 1 + j] == ' ':  # right
                            self.my_range[y + 1][x - 1 + j] = mark
        else:
            for j in range(0, ship_len + 2):  # my cells about ship is close
                if 0 <= y - 1 + j < 9:
                    if y - 1 + j >= 0 and self.my_range[y - 1 + j][x] == ' ':  # up and down
                        self.my_range[y - 1 + j][x] = mark
                    if x - 1 >= 0:
                        if x - 1 + j >= 0 and self.my_range[y - 1 + j][x - 1] == ' ':  # left
                            self.my_range[y - 1 + j][x - 1] = mark
                    if x + 1 < 9:
                        if x - 1 + j >= 0 and self.my_range[y - 1 + j][x + 1] == ' ':  # right
                            self.my_range[y - 1 + j][x + 1] = mark

    def check_field_spawn(self, x, y, ship, is_spawn=False, is_x=None, is_random=False):
        def launch_pc_or_battle(is_battle):
            if is_battle:  # is player is ready?
                pc.ready_for_battle = True
                options.print_field(input_kind='fight')
            else:
                player.ready_for_battle = True
                pc_field.ship_random_place(ship=1)  # randomly spawn for pc

        close_cell_horizontal = []  # need to check all cells are empty or not (horizontal)
        close_cell_vertical = []  # need to check all cells are empty or not (vertical)
        ship_coordination = []  # need to collect all cell with new ship
        last_x_cell = x + len(dic_ships_spawn[ship])
        last_y_cell = y + len(dic_ships_spawn[ship])
        free_cells_tip = [' ', 'H', 'V']
        # Vertical check
        if len(self.my_range) >= last_y_cell:
            for i in range(len(dic_ships_spawn[ship])):  # check that all cells are free to use
                if is_spawn and not is_x:
                    self.my_range[y + i][x] = SHIP_MARK
                    ship_coordination.append(str(y + i)+str(x))
                else:
                    if self.my_range[y + i][x] not in free_cells_tip:
                        close_cell_vertical.append(i)
                    else:
                        self.my_range[y + i][x] = 'V'
        else:
            close_cell_vertical.append('skip')  # ship will not fit on the field by vertical
        # Horizontal check
        if len(self.my_range[0]) >= last_x_cell:
            for i in range(len(dic_ships_spawn[ship])):  # check that all cells are free to use
                if is_spawn and is_x:
                    self.my_range[y][x + i] = SHIP_MARK
                    ship_coordination.append(str(y) + str(x + i))
                else:
                    if self.my_range[y][x + i] not in free_cells_tip:
                        close_cell_horizontal.append(i)  # ship will not fit on the field by horizontal
                    else:
                        self.my_range[y][x + i] = 'H'
        else:
            close_cell_horizontal.append('skip')
        if is_spawn:
            if player.ready_for_battle:  # save position of created ship
                pc.dic_ships_position[ship] = pc.dic_ships_to_fire[ship] = ship_coordination
                pc.dic_ship_is_horizontal[ship] = is_x
            else:
                player.dic_ships_position[ship] = player.dic_ships_to_fire[ship] = ship_coordination
                player.dic_ship_is_horizontal[ship] = is_x
            self.make_ship_aura(x=x, y=y, ship_len=len(dic_ships_spawn[ship]), is_horizontal=is_x)
        if not is_random:
            # For manual by the player
            if not is_spawn:
                if ship < 6:
                    if not close_cell_vertical and not close_cell_horizontal:
                        options.print_field('spawn_position', ship=ship)
                    elif not close_cell_vertical:  # it can be placed only vertical
                        self.remove_help_char('H')
                        options.print_field('spawn_position_y', ship=ship)
                    elif not close_cell_horizontal:  # it can be placed only horizontal
                        self.remove_help_char('V')
                        options.print_field('spawn_position_x', ship=ship)
                    else:
                        raise ErrSpawn('Выбранное поле занято', ship=ship-1)
                else:
                    if not close_cell_vertical or not close_cell_horizontal:
                        self.check_field_spawn(x, y, ship, True, True)
                    else:
                        raise ErrSpawn('Выбранное поле занято', ship=ship - 1)
            else:
                if ship != 9:
                    options.print_field('spawn_cell', ship=ship)  # let build another ship
                else:  # player or pc have all ships
                    self.remove_help_char()
                    if player.ready_for_battle:
                        launch_pc_or_battle(True)
                    else:
                        launch_pc_or_battle(False)
        # Random
        else:
            if not is_spawn:
                if is_x:
                    return not bool(close_cell_horizontal)  # can I spawn ships by horizontal?
                else:
                    return not bool(close_cell_vertical)  # can I spawn ships by vertical&
            else:
                if ship != 9:
                    self.ship_random_place(ship=ship + 1)
                else:  # player or pc have all ships
                    self.remove_help_char()
                    if player.ready_for_battle:
                        launch_pc_or_battle(True)
                    else:
                        launch_pc_or_battle(False)

# ------------ ERRORS --------------


class LockedFire(Exception):  # Catch error when player try to fire on locked cell
    def __init__(self, msg):
        options.print_field('fight', msg)


class ErrPosition(Exception):
    def __init__(self, msg, ship):
        player_field.remove_help_char('')
        options.print_field('spawn_cell', msg, ship)


class ErrSpawn(Exception):
    def __init__(self, msg, ship):
        options.print_field('spawn_cell', msg, ship)

# ------------ LAUNCH ---------------


options = Game()
player = Player(help_vision=True)
pc = Player(is_ai=True)
player_field = Field()
pc_field = Field()
options.main_menu()
