import os
from math import floor
from Classes.player import Player
clear = lambda: os.system('cls')

def Change_name():
    while True:
        name = input("Enter your name: ")
        if len(name) > 20:
            print("Name is too long. It must be 20 characters or less.")
        else:
            try:
                name.encode('ascii')
            except UnicodeEncodeError:
                print("Name contains non-ASCII characters. Please enter a valid Player name.")
            else:
                break
        return(name)

def Create():
    name = Change_name()  
    game_classes = {
    'The Regular Guy': {
        'name': '*Has a ketchup stain on his shirt',
        'health': 100,
        'mana': 50,
        'damage': 20,
        'coin': 100
    },
    'The Thief': {
        'name': '*Is decked out with handbags and whatnot from having stolen soo much loot from old ladies',
        'health': 80,
        'mana': 100,
        'damage': 30,
        'coin': 50
    },
    'The Knight': {
        'name': "*Despite the sword's steel blade haven fallen off from countless battles, he still uses the wooden handle to beat monsters into submission",
        'health': 150,
        'mana': 30,
        'damage': 40,
        'coin': 200
    },
    'The Rogue': {
        'name': '*Fast and agile ',
        'health': 90,
        'mana': 70,
        'damage': 25,
        'coin': 75
    },
    'The Physically Ill': {
        'name': 'The Physically Ill',
        'health': 50,
        'mana': 10,
        'damage': 10,
        'coin': 10
    }
}
    while True:
        clear()
        print('''Hello {name}. Please choose your characters class: ''')
        for j,i in game_classes.items():
            print()
        a = input("")


Create()
#user = Player('Peeter', 100, 20, 1, 0)


while True:
    clear()
    print(f'name: {user.name} hp: {user.health}/{user.max_health} || xp: {floor(user.xp)}p({floor(20 * (user.multipliers["lvl_up"]**(user.level-1)) - user.xp)}p left) level: {user.level}')
    a = int(input('''Select what you want to do:
                    1: lose hp
                    2: gain hp
                    3: kill an enemy'''))
    if a == 1:
        user.lose_hp(int(input('amount to remove: ')))
    elif a == 2:
        user.add_hp(int(input('amount to add: ')))
    elif a == 3:
        user.add_xp(int(input('amount to add: ')))
    else:
        break