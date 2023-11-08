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

def Map_Hud(player, map, player_pos, player_seen):
    clear()
    print(f"{player.name}, {player.clss}")
    print(f"Zone : {player.zone}")
    temp = map[:player_seen]
    print(temp[:player_pos-1] + "*" + temp[player_pos:])
    

def generate_map_string(zone_data):
    w, s, t = random.randint(*zone_data["length"]), random.randint(*zone_data["shops"]), random.randint(*zone_data["things"])
    if t < 0:
        t = 0

    m = ["_" for i in range(w)]

    repeats = 0
    while s > 0:
        i = random.randint(3,len(m)-1)
        repeats += 1
        if repeats > 100:
            break
        try:
            if m[i] != "_" or m[i+1] == 's' or m[i-1] == 's':
                continue
        except:
            continue

        m[i] = 's'

        s-= 1

    repeats = 0
    while t > 0:

        repeats += 1
        if repeats > 100:
            break

        i = random.randint(3,len(m)-1)

        try:
            if m[i] != "_" or m[i+1] != '_':
                continue
        except:
            continue

        t -= 1

        m[t] = 's'
    
    return '___'+''.join(m)
    

def Generate_map():
    with open("Data\Zone_Order.txt", "r") as f:
        order = [i.replace("\n", "") for i in f]
    with open("Data\Zone_Length.json", "r") as f:
        details = json.load(f)

    map = {i: generate_map_string(details[i]) for i in order}
    return map


