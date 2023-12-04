import random
from Classes import Equipment_create
import json
import os
clear = lambda: os.system('cls')

def Enemy_Loot(player):
    a = random.random
    if a <= 0.1:
        with open("Data/Zone_Spells.json") as f:
            spell = random.choice(json.load(f)[player.zone])
        player.add_spell(spell)
        input(f"The Enemy dropped you forgotten knowladge. A new Spell called {spell}!!\n[Enter To Continue]")
    elif a <= 0.5:
        eq = Equipment_create()
        input(f'The enemy dropped a new {eq.type}! {eq.name} with the stat of {eq.stat}. It has been added to your inventory\n[Enter To Continue]')
        player.add_inventory(eq)

    return(player)

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
                    sword = Equipment_create("Sword")
                    input(f'You got a new Sword! {sword.name} with the damage stat of {sword.stat}. It has been added to your inventory\n[Enter To Continue]')
                    player.add_inventory(sword)
                elif a == "Magic Power":
                    if random.random <= 0.2:
                        with open("Data/Zone_Spells.json") as f:
                            spell = random.choice(json.load(f)[player.zone])
                        player.add_spell(spell)
                        input(f"Because you're so talented you gained a {spell} from your current zone.\n[Enter To Continue]")
                    else:
                        player.max_mana += 10
                        player.add_skills["magic"] += 30
                        input(f"You failed at being talented but you gained 10 max mana and experience in casting magic")
                elif a == "Strength":
                    if random.random <= 0.2:
                        player.affliction_multipliers["do_damage"] += 0.1
                        input(f"You now hit with more damage. Veeeri Stronk (:\n[Enter To Continue]")
                    else:
                        player.affliction_multipliers["do_damage_additive"] += 5
                        input(f"You now hit with more damage. Veeeri Stronk (:\n[Enter To Continue]")


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
        player = Enemy_Loot(player)
    elif condition == "Levelup":
        player = Level_Up(player)
    elif condition == "None":
        pass
    return(player)