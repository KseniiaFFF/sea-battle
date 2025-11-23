import random

size_i, size_j = 10, 10

symbols = {
    'ship' : '[#]', 'damage' : '[*]', 'empty' : '[_]', 'kill' : '[X]', 'miss' : '[-]'
}

can_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def create_field():
    return [[symbols['empty'] for _ in range(size_j)] for _ in range(size_i)]

def show_pole(field):
    cell_width = 5
    print(' ' * (cell_width - 1), end='')
    for j in range(1, size_j + 1):
        print(f'{j:^{cell_width}}', end='')
    print()
    for i in range(size_i):
        print(f'{i+1:^{cell_width}}', end='')
        for j in range(size_j):
            print(f'{field[i][j]:^{cell_width}}', end='')
        print()

def save_game(pole_user_ships, pole_bot_ships, users_ships, bot_ships):
    with open('save_user_pole.txt', 'w') as file:
        for row in pole_user_ships:
            file.write(''.join(row) + '\n')
        file.write('users_ships\n')
        file.write(','.join(map(str, users_ships)) + '\n')
    with open('save_bot_pole.txt', 'w') as file:
        for row in pole_bot_ships:
            file.write(''.join(row) + '\n')
        file.write('bots_ships\n')
        file.write(','.join(map(str, bot_ships)) + '\n')

def load_game(pole_user, pole_bot, users_ships, bot_ships):
    pole_user.clear()
    pole_bot.clear()
    users_ships.clear()
    bot_ships.clear()

    with open('save_user_pole.txt', 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            if line == 'users_ships':
                section = 'users_ships'
                continue
            if section == 'users_ships':
                for x in line.split(','):
                    x = x.strip()
                    if x:
                        users_ships.append(int(x))
            else:
                cells = [cell + ']' for cell in line.split(']') if cell.strip() != '']
                pole_user.append(cells)

    with open('save_bot_pole.txt', 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            if line == 'bots_ships':
                section = 'bots_ships'
                continue
            if section == 'bots_ships':
                for x in line.split(','):
                    x = x.strip()
                    if x:
                        bot_ships.append(int(x))
            else:
                cells = [cell + ']' for cell in line.split(']') if cell.strip() != '']
                pole_bot.append(cells)

    return pole_user, pole_bot, users_ships, bot_ships

def permit_ship(user_ship, users_ships, pole):
    if users_ships.count(user_ship) < can_ships.count(user_ship):
        save_game(pole, pole_bot_ships, users_ships, bot_ships)
        return True
    print('Слишком много кораблей', user_ship)
    return False

def place_ship(pole, ship_size, angle, i, j):
    if angle == 1: 
        if j + ship_size > size_j:
            return False
        for x in range(ship_size):
            if pole[i][j+x] != symbols['empty']:
                return False
        for x in range(ship_size):
            pole[i][j+x] = symbols['ship']
    else: 
        if i + ship_size > size_i:
            return False
        for x in range(ship_size):
            if pole[i+x][j] != symbols['empty']:
                return False
        for x in range(ship_size):
            pole[i+x][j] = symbols['ship']
    return True

def can_place_ship(pole, ship, angle, i, j):

    cells = []

    if angle == 1:  
        if j + ship > size_j:
            return False
        cells = [(i, j + k) for k in range(ship)]
    else:  
        if i + ship > size_i:
            return False
        cells = [(i + k, j) for k in range(ship)]

    for ci, cj in cells:
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = ci + di, cj + dj
                if 0 <= ni < size_i and 0 <= nj < size_j:
                    if pole[ni][nj] != symbols['empty']:
                        return False
    return True

def place_ship(pole, ship, angle, i, j):

    if not can_place_ship(pole, ship, angle, i, j):
        return False

    if angle == 1:
        for k in range(ship):
            pole[i][j+k] = symbols['ship']
    else:
        for k in range(ship):
            pole[i+k][j] = symbols['ship']
    return True

def auto_ships(pole, ships_list):
    while len(ships_list) < len(can_ships):
        ship = random.choice(can_ships)
        if ships_list.count(ship) >= can_ships.count(ship):
            continue
        angle = random.randint(1,2)
        i, j = random.randint(0, size_i-1), random.randint(0, size_j-1)
        if place_ship(pole, ship, angle, i, j):
            ships_list.append(ship)

def user_put_ships(pole, users_ships):
    while len(users_ships) < len(can_ships):
        print('#-1; ##-2; ###-3; ####-4')
        user_ship = int(input('Enter number of ship or 0 for exit/save, 777 for load: '))
        if user_ship == 0:
            save_game(pole, pole_bot_ships, users_ships, bot_ships)
            print('Game saved.')
            exit()
        elif user_ship == 777:
            load_game(pole, pole_bot_ships, users_ships, bot_ships)
            show_pole(pole)
            continue
        if user_ship < 1 or user_ship > 4 or not permit_ship(user_ship, users_ships, pole):
            continue
        angle = int(input('Enter angle 1-horizontal, 2-vertical: '))
        i = int(input('Enter I (1-10): ')) - 1
        j = int(input('Enter J (1-10): ')) - 1
                
        if place_ship(pole, user_ship, angle, i, j):
            users_ships.append(user_ship)
            show_pole(pole)

def is_ship_dead(pole, i, j):
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for di, dj in directions:
        x, y = i + di, j + dj
        while 0 <= x < size_i and 0 <= y < size_j:
            if pole[x][y] == symbols['ship']:
                return False
            if pole[x][y] in (symbols['empty'], symbols['miss']):
                break
            x += di
            y += dj
    return True

def mark_dead_ship(pole, i, j):
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    pole[i][j] = symbols['kill']
    for di, dj in directions:
        x, y = i + di, j + dj
        while 0 <= x < size_i and 0 <= y < size_j:
            if pole[x][y] == symbols['damage']:
                pole[x][y] = symbols['kill']
            else:
                break
            x += di
            y += dj

def user_shoot(pole_bot_ships, pole_user_hits):
    while True:
        i = int(input('Enter I (1-10): ')) - 1
        j = int(input('Enter J (1-10): ')) - 1
        cell = pole_user_hits[i][j]
        if cell in (symbols['damage'], symbols['kill'], symbols['miss']):
            print('Already shot here')
            continue
        if pole_bot_ships[i][j] == symbols['ship']:
            pole_user_hits[i][j] = symbols['damage']
            pole_bot_ships[i][j] = symbols['damage']
            if is_ship_dead(pole_bot_ships, i, j):
                mark_dead_ship(pole_user_hits, i, j)
                print('Ship destroyed!')
            else:
                print('Hit!')
        else:
            pole_user_hits[i][j] = symbols['miss']
            print('Miss')
        break

def bot_shoot(pole_user_ships, pole_bot_hits):
    while True:
        i = random.randint(0, size_i-1)
        j = random.randint(0, size_j-1)
        cell = pole_bot_hits[i][j]
        if cell in (symbols['damage'], symbols['kill'], symbols['miss']):
            continue
        if pole_user_ships[i][j] == symbols['ship']:
            pole_bot_hits[i][j] = symbols['damage']
            pole_user_ships[i][j] = symbols['damage']
            if is_ship_dead(pole_user_ships, i, j):
                mark_dead_ship(pole_bot_hits, i, j)
                print('Bot destroyed your ship!')
            else:
                print('Bot hit your ship!')
        else:
            pole_bot_hits[i][j] = symbols['miss']
            print('Bot missed')
        break

def check_victory(pole):
    for row in pole:
        if symbols['ship'] in row:
            return False
    return True       

pole_user_ships = create_field()
pole_bot_ships = create_field()
pole_user_hits = create_field()
pole_bot_hits = create_field()

users_ships = []
bot_ships = []
auto_ships(pole_bot_ships, bot_ships)
user_put_ships(pole_user_ships, users_ships)

user_moves = 0
bot_moves = 0

while True:
    print('--- User ---')
    show_pole(pole_user_hits)
    user_shoot(pole_bot_ships, pole_user_hits)
    user_moves += 1
    if check_victory(pole_bot_ships):
        print('You won')
        with open('stats.txt', 'a') as file:  
            file.write('User won: ')
            file.write(str(user_moves))
        break

    print('--- Bot ---')
    show_pole(pole_bot_hits)
    bot_shoot(pole_user_ships, pole_bot_hits)  
    bot_moves += 1
    if check_victory(pole_user_ships):
        print('Bot won')
        with open('stats.txt', 'a') as file:  
            file.write('Bot won: ')
            file.write(str(bot_moves)+'\n')
        break