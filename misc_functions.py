import time
import os
import json
import random
from Classes.player import Debug_Create 
from Adventure.loot import Loot
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
    
def Generate_map(zone):
    with open("Data\Zone_Length.json", "r") as f:
        details = json.load(f)
    
    if zone not in details.keys():
        print(f"No zone such as - {zone}")
        time.sleep(1)
        return None

    return generate_map_string(details[zone])

def Choose_Zone(player):
    clear()
    with open("Data\Zone_Order.json", "r") as f:
        zones = json.load(f)[str(player.depth)]

    if player.zone != None:
        a = random.randint(0,2)
        if a == 1:
            del zones[random.randint(0, len(zones) - 1)]
        elif a == 2:
            zones.remove(player.zone)
            del zones[random.randint(0, len(zones) - 1)]
    else:
        zones = [zones[random.randint(0, len(zones) - 1)]]

    options = [
            "Loot" if random.random() < 0.3 * player.multipliers["luck"] and player.timer != 0 else "",
            *zones,
            "Jump down a deeper hole (progress)" if random.random() < 0.5 and player.timer != 0 and player.depth != 3 else ""
                ]
    options = [i for i in options if i != ""]

    descriptions = {}
    with open("Data\Zone_Descriptions.json", "r") as f:
        a = json.load(f)
        for i in zones:
            descriptions[i] = a[i]

    t = ''

    while True:

        print('Leaving Current Zone..\n\n')

        print("{:^10} {:<5}".format("Index", "Path"))
        print('-'*22)
        for x, i in enumerate(options, start=1):
            print("{:^10} {}".format(x, i))
        print()
        for x, i in enumerate(zones):
            print(f'{i} - "{descriptions[i]["path_description"]}"')


        print("\n"+t+"\n")
        t = ""

        a = input(f"\nSelect: ")
        if not a.isdigit() or not 0 < int(a) <= len(options):
            t = "Please Insert a Correct Index."
            continue
        t = ''
        a = options[int(a)-1]
        
        if a == "Loot":
            options.remove("Loot")
            t = "You looted the Chest"
            player = Loot(player, "Zone")
        elif a == "Jump down a deeper hole (progress)":
            player.depth += 1
            player.timer = 0
            player.zone = None
            return Choose_Zone(player)
        elif a in descriptions:
            player.zone = a
            t = descriptions[a]["chosen_description"]
            break

    return player, t