import time
import json
import random
from misc_functions import Combat_Hud

def Select_Enemy(depth, zone):
    with open("Data/Enemies.json", 'r') as f:
        a = json.load(f)[depth][zone]
    key = random.choice(list(a.keys()))
    return {**a[key], 'name': key, 'max_health': a[key]["health"]}

def Fight(player):
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
    while True:
        Combat_Hud(player, enemy)
        print(happening)
        print("\n\n{:^10} {:<5}".format("Index", "Action"))
        print('-'*22)
        options = ['Attack', 'Magic', 'Inventory', 'Run']
        for x,i in enumerate(options, start=1):
            print(f'{x:^10} {i:<5}')
        a = input("Select: ")
        
    return(player)