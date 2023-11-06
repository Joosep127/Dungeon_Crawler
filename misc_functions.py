import time
import os
import json
import random
from Classes.player import Debug_Create 
clear = lambda: os.system('cls')

def Hud(player):
    clear()
    print(f"{player.name}, {player.clss}")
    print(f"Hp: {player.health}/{player.max_health} | Magic: {player.mana}/{player.max_mana} | {player.coin}$ | Lvl: {player.level}")
    #xp_needed = floor(20 * (player.multipliers["lvl_up"] ** (player.level - 1)) - player.xp)
    #print(f"xp: {player.xp}\n")
    print("\n")

def Combat_Hud(player, enemy, can_see_stats):
    clear()
    if can_see_stats:
        print("{:<41}|	{}".format(f'{player.name}, {player.clss}', enemy['name']))
        print("Hp: {:<14}| Magic: {:<14}|	Hp: {:<14}".format(f'{player.health}/{player.max_health}', f'{player.mana}/{player.mana}', f'{enemy["health"]}/{enemy["max_health"]}'))
        print("DMG: {:<13}| DEF: {:<16}|	DMG: {:<13} \n".format(f'{player.damage}(+{player.cal_damage()-player.damage})', player.cal_defence(), enemy["attack"]))
    elif not can_see_stats:
        print("{:<41}|	{}".format(f'{player.name}, {player.clss}', "*"*len(enemy['name'])))
        print("Hp: {:<14}| Magic: {:<14}|	Hp: {:<14}".format(f' {player.health}/{player.max_health}' , f'{player.mana}/{player.mana}', f'{"*"*len(enemy["max_health"])}/{"*"*len(enemy["max_health"])}'))
        print("DMG: {:<13}| DEF: {:<16}|	DMG: {:<13} \n".format(f'{player.damage}(+{player.cal_damage()-player.damage})', player.cal_defence(), enemy["attack"]))
    else:
        print("The object can_see_stats is broken")
        time.sleep(1)


def generate_map_string(zone_data):
    w, n, t = random.randint(*zone_data["length"]), random.randint(*zone_data["shops"]), random.randint(*zone_data["things"])
    if t < 0:
        t = 0

    total_positions = w
    empty_positions = total_positions - n - t

    m = ['s' if i < n else 't' if i < n + t else ' ' for i in range(total_positions)]

    # Shuffle the positions
    random.shuffle(m)

    # Convert to a string
    map_string = '___'.join(m).replace(" ", "_")

    return map_string
    

def Generate_map():
    with open("Data\Zone_Order.txt", "r") as f:
        order = [i.replace("\n", "") for i in f]
    with open("Data\Zone_Length.json", "r") as f:
        details = json.load(f)

    map = {i: generate_map_string(details[i]) for i in order}
    return map

print(Generate_map())