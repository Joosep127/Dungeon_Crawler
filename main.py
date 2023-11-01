import os
from math import floor
from Classes.player import Create, Debug_Create 
from misc_functions import Hud
from shop import Shop
import time
clear = lambda: os.system('cls')



def Main():
    global player
    player = Create()

    Hud(player)
    if player.clss == 'The Physically Ill':
        print("Being not only Physically handicapped it appears you are also mentally retarded, deciding to go on an adventure to the local hole in the ground.\n")
    else:
        print("You one day decide to go to work, but you fell in to a hole.\n")
    input("[Press enter to continue]")
    Hud(player)

    

    while True: # Game Loop
        break


while False:
    clear()
    print(f'name: {user.name} hp: {user.health}/{user.max_health} || xp: {floor(20 * (user.multipliers["lvl_up"] ** (user.level - 1)) - user.xp)}p left) level: {user.level}')
    a = int(input('''Select what you want to do:
                    1: lose hp
                    2: gain hp
                    3: kill an enemy'''))
    if a == 1:
        user.lose_hp(int(input('amount to remove: ')))
    elif a == 2:
        user.add_hp(int(input('amount to add: ')))
    elif a == 3:
        print(user.add_xp(int(input('amount to add: ')))[-1])
        time.sleep(1)
    else:
        break

if __name__ == "__main__":
    #Main()
    while True:
        player = Debug_Create("Mr. Moneybags", 100, 100, 100, 100, "The Monopoly man")
        Shop(player)
        input("[Press ENTER to continue]")