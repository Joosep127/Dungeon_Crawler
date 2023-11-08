import os
from math import floor
from Classes.player import Create, Debug_Create 
from misc_functions import Hud, Generate_map, Map_Hud
from Adventure.fight import Fight
from Adventure.shop import Shop,Generate_Shop_Inv
import random
import time 
clear = lambda: os.system('cls')



def Main():
    #player = Debug_Create("Mr. Moneybags", 100, 100, 100, 100, "The Monopoly man")
    
    player = Create()
    player.zone = 'Underground Forest' 

    Hud(player)
    if player.clss == 'The Physically Ill':
        print("Being not only Physically handicapped it appears you are also mentally retarded, deciding to go on an adventure to the local hole in the ground.\n")
    else:
        print("You one day decide to go to work, but you fell in to a hole.\n")
    input("[Press enter to continue]")
    
    Map = Generate_map()

    #Map = {'Underground Forest': "__s_"}

    player_pos = 1
    player_seen = 0
    shops = {}
    for x, i in enumerate(Map[player.zone]):
        if i == "s":
            shops[str(x)] = Generate_Shop_Inv(player.depth, player.multipliers['equipment'])
    

    while True: # Game Loop
        
        t = ""
        while True:
            if player_seen < player_pos-1:
                 player_seen = player_pos

            options = ["Enter Shop" if Map[player.zone][player_pos] == "s" else "", "Move Forward" if player_pos < len(Map[player.zone]) else "Go to next Zone", "Go Backwards" if player_pos != 0 else "", "Set up camp"]
            options = [i for i in options if i != ""]
            Map_Hud(player, Map[player.zone], player_pos, player_seen)

            print("Index  Command")
            for x, i in enumerate(options, start=1):
                print(f"{x:5} {i}")
            print("\n"+t)
            a = input(f"Select: ")
            if not a.isdigit() or not 0 < int(a) <= len(options):
                t = "Please Insert a Correct Index."
                continue
            t = ''
            a = options[int(a)-1]
            
            if a == 'Move Forward':
                player_pos += 1
            elif a == 'Go Backwards':
                player_pos -= 1
            elif a == "Set up camp":
                print('Setting up camp.')
            elif a == "Enter Shop":
                Shop(player, shops[str(player_pos)])

            if random.random() < 0.3:
                Fight(player)



if __name__ == "__main__":
    Main()
    
    while False:
        
        player = Debug_Create("Mr. Moneybags", 100, 100, 100, 100, "The Monopoly man")
        player.zone = 'Underground Forest' 
        for i in range(5):
            player.add_inventory({'name' : "Health Potion", 'effect' : random.randint(5,7)})
            player.add_inventory({'name' : "Mana Potion", 'effect' : random.randint(5,7)})
            player.add_spell("Invisibility")