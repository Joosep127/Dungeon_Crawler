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

if __name__ == "__main__":
    #Main()
    while True:
        player = Debug_Create("Mr. Moneybags", 100, 100, 100, 100, "The Monopoly man")
        Shop(player)
        input("[Press ENTER to continue]")