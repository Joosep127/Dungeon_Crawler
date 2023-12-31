import os
from math import floor
from Classes.player import Create, Debug_Create 
from misc_functions import Hud, Generate_map, Map_Hud, Choose_Zone
from Adventure.camp import Set_Camp
from Adventure.fight import Fight
from Adventure.shop import Shop,Generate_Shop_Inv
import random
import time 
clear = lambda: os.system('cls')
clear()

def gen_shops(player, Map):
    shops = {}
    for x, i in enumerate(Map):
        if i == "s":
            shops[str(x)] = Generate_Shop_Inv(player.depth, player.multipliers['equipment'])
    return(shops)

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
    
    Map = Generate_map(player.zone)

    player_pos = 1
    player_seen = 0
    shops = gen_shops(player, Map)
    

    while True: # Game Loop
        
        t = ""
        while True:

            if player_seen < player_pos-1:
                 player_seen = player_pos

            options = ["Move Forward" if player_pos < len(Map) else "Leave Current Zone", "Go Backwards" if player_pos != 0 else "-", "Set up camp", "Enter Shop" if Map[player_pos-1] == "s" else ""]
            options = [i for i in options if i != ""]

            Map_Hud(player, Map, player_pos, player_seen)

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
                t = "You wandered around for a good while"
                player.timer += 1
            elif a == 'Go Backwards':
                player_pos -= 1
                t = "You walked backwards for an indeterminate amount of time"
                player.timer += 1
            elif a == "Set up camp":
                player = Set_Camp(player)
                t = "You're back on your journey"
                continue
            elif a == "Enter Shop":
                Shop(player, shops[str(player_pos-1)])
                t = "You left the shop"
                continue
            elif a == "Leave Current Zone":
                player_pos = 1
                player_seen = 0
                player, t = Choose_Zone(player)
                if t == "end":
                    break
                Map = Generate_map(player.zone)
                shops = gen_shops(player, Map)
                continue

            if random.random() < 0.3:
                Fight(player)
        break
    
    print("Here are your stats for this play through.")
    print(player)
    input("[ENTER] TO END THE GAME")



if __name__ == "__main__":
    Main()