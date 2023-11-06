import os
from math import floor
from Classes.player import Create, Debug_Create 
from misc_functions import Hud, Generate_map
from Adventure.fight import Fight
from Adventure.shop import Shop
import random
import time
clear = lambda: os.system('cls')

a = Generate_map()

print(a)

exit()

def Main():
    global player
    player = Create()

    Hud(player)
    if player.clss == 'The Physically Ill':
        print("Being not only Physically handicapped it appears you are also mentally retarded, deciding to go on an adventure to the local hole in the ground.\n")
    else:
        print("You one day decide to go to work, but you fell in to a hole.\n")
    input("[Press enter to continue]")
    
    Map = Generate_map()

    while True: # Game Loop

        break

if __name__ == "__main__":
    Main()
    while False:
        player = Debug_Create("Mr. Moneybags", 100, 100, 100, 100, "The Monopoly man")
        player.zone = 'Underground Forest' 
        for i in range(5):
            player.add_inventory({'name' : "Health Potion", 'effect' : random.randint(5,7)})
            player.add_inventory({'name' : "Mana Potion", 'effect' : random.randint(5,7)})
            player.add_spell("Invisibility")
        Fight(player)
        input("[Press ENTER to continue]")