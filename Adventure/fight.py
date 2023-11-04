import time
import json
import random
from misc_functions import Combat_Hud
from Adventure.enemy import Select_Enemy, Decide_Action
from Adventure.misc_zones import Loot



def Magic(player):
    spells = player.spells
    if spells == {}:
        return player, 'No spells'
    print("\n{:^10} {:<5} {:<15} {:<5}".format("Index", "Level", "Spell", "Mana cost"))
    for x, i in enumerate(spells.keys()):
        print("\n{:^10} {:<5} {:<15} {:<5}".format(x, spells[i], i, "Mana cost"))
    a = input('Select: ')
    return player, a

def Inventory(player):
    return

def Run(player):
    return

def Fight(player):
    player.reset_afflictions()
    enemy = Select_Enemy(str(player.depth), player.zone)
    happening = random.choice([
    f"You walk upon the {enemy['name']}.",
    f"The {enemy['name']} jumps in front of you.",
    f"The {enemy['name']} roars loudly.",
    f"You prepare to battle the {enemy['name']}.",
    f"You spot a {enemy['name']} in the distance.",
    f"The menacing presence of the {enemy['name']} grows stronger.",
    f"Your heart races as you approach the {enemy['name']}.",
    f"The {enemy['name']} eyes you cautiously.",
    f"You sense a forthcoming battle with the {enemy['name']}.",
    f"The air is charged with tension as you near the {enemy['name']}.",
    f"The {enemy['name']} readies itself for an encounter with you.",
    f"A battle with the {enemy['name']} seems inevitable."
    ])
    t = "\n"
    options = ['Attack', 'Magic', 'Inventory', 'Run']
    while True:
        if happening[0] == 'ran':
            if player.health/player.max_health < 0.3:
                print('You despretly fled from the ' + enemy['name'] + ' while he was ' + happening[1])
            if player.health/player.max_health < 0.6:
                print('You fled from the ' + enemy['name'] + ' while he was ' + happening[1])
            if player.health/player.max_health < 0.9:
                print('Deciding to pack your shit up you up and left while the ' + enemy['name'] + ' was ' + happening[1])
            else:
                print('You wandred off.')
            print('\n')
            input('[ENTER] To continue')
            break
        Combat_Hud(player, enemy)
        print(happening)
        print("{}\n{:^10} {:<5}".format(t, "Index", "Action"))
        print('-'*22)
        for x,i in enumerate(options, start=1):
            print(f'{x:^10} {i:<5}')
        
        a = input("Select: ")
        if a.isdigit():
            if 0 <= int(a)-1 < len(options):
                a = options(a)
                if a == 'Attack':
                    pass
                elif a == 'Magic':
                    player, a = Magic(player)
                    if a == "No spells":
                        t = "*You have no spells to Cast\n"
                        continue
                    if a == "No magic":
                        t = "*You cancel the magic\n"
                        continue
                elif a == 'Inventory':
                    player, a = Inventory(player)
                    if a == 'exit':
                        t = '*You closed your inventory\n'
                        continue
                elif a == 'Run':
                    pass
            else:
                print("Please choose a valid index")
                time.sleep(0.4)
                continue
        else:
            print("Please enter a number you fucking idiot.")
            time.sleep(0.4)
            continue

        player, enemy, happening = enemy_player_interaction(player, enemy, a)
    if random.random() < 0.1:
        player = Loot(player)
    return(player)