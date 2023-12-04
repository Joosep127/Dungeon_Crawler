import random
from Classes import Equipment_create
import os
clear = lambda: os.system('cls')


def Level_Up(player):
    t = ''
    while True:
        option = ["New Sword", "Magic Power", "Strength"]
        print("Upon leveling up you see a window open before your eyes. \nWhat do you get?: ")
        print("{:^10} {:<5}".format("Index", "Action"))
        print('-'*22)
        for x,i in enumerate(options, start=1):
            print(f'{x:^10} {i:<5}')
        print(t)
        a = input("Select: ")
        if a.isdigit():
            a = int(a)
            if 0 <= int(a)-1 < len(options):
                a = options[a-1]
                
                if a == 'New Sword':
                    sword = Equipment_create()
                    input(f'You got a new Sword! {sword.name} with the damage stat of {sword.stat}. It has been added to your inventory\n[Enter To Continue]')
                    player.add_inventory(sword)
                elif a == "Magic Power":
                


            else:
                t = "Please choose a valid index"
                continue
        else:
            t = "Please enter a number you fucking idiot."
            continue
         
        
    return player

def Loot(player, condition="None"):
    if condition == "Zone":
        pass
    elif condition == "Enemy":
        pass
    elif condition == "Levelup":
        player = Level_Up(player)
    elif condition == "None":
        pass
    return(player)