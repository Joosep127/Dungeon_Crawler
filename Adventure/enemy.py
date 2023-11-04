import random
import json

def Select_Enemy(depth, zone):
    with open("Data/Enemies.json", 'r') as f:
        a = json.load(f)[depth][zone]
    key = random.choice(list(a.keys()))
    with open("Data/Enemy_Elements.json", 'r') as f:
        d = json.load(f)[a[key]['type']]
    return {**a[key], 'name': key, 'max_health': a[key]["health"], d}

def Magic_Damage_2_Enemy(player, enemy, player_action):
    return player, enemy

def Decide_Action(enemy):
    if enemy["int"] == 1:
        action = random.choice(["attack", "nothing"])
    elif enemy["int"] == 2: # I have to remove the functionality for low intel creatures to use magic
        action = "attack"
    elif enemy["int"] == 3:
        decision = random.random()
        if decision < 0.6:
            action = "attack"
        elif decision < 0.9:
            if enemy["can_use_magic"]:
                action = "heal"
            else:
                action = "block"
        else:
            action = random.choice("attack", "afflict")
    elif enemy["int"] == 4:
        decision = random.random()
        if decision < 0.7:
            action = "attack"
        elif enemy["health"]/enemy["max_health"] <= 0.3:
            if player.health <= enemy["attack"]:
                action = "attack"
            else:
                if enemy["can_use_magic"]:
                    action = "heal"
                else:
                    action = "block"
        else:
            action = random.choice("attack", "afflict")
    else:
        action = 'There has been a bug with the enemy INT json file. the range for INT has to be 1-4'
    return(action)

def enemy_player_interaction(player, enemy, player_action):
    enemy_action = Decide_Action(enemy)
    if player_action == 'run':
        if random.random() < 0.7:
            if enemy_action == 'heal':
                b = 'healing itself'
            elif enemy_action == 'afflict':
                b = 'trying to sneeze on you'
            else: 
                b = enemy_action + 'ing'
            a = ['ran', b]
    elif enemy_action == 'block':
        if player_action == 'attack':
            if random.random() < 0.2:
                t = round(player.cal_damage*0.4)
                enemy.health -= t
                a = f'The {enemy["name"]} effectively blocked your attack. Dealt {t} damage'
            else:
                t = round(player.cal_damage*0.6)
                enemy.health -= t
                a = f'The {enemy["name"]} blocked your attack. Dealt {t} damage'
        elif isinstance(player_action, dict):
            player, enemy = Magic_Damage_2_Enemy(player, enemy, player_action)
        elif player_action == 'run':
            a = f'The {enemy["name"]}blocked thin air. you ran but he caught up with you. Unlucky'
        else:
            a = f"The {enemy["name"]} for some reason tried to block while you were standing at a reasonable distance."
    elif enemy_action == 'heal':
        if player_action == 'attack':
            if random.random() < 0.2: 
                t = player.cal_damage*2
                enemy["health"] -= t
                if enemy["health"] <= 0:
                    a = f'The {enemy["name"]} tried to heal itself but you ruthlessly killed it with {t} damage before it could.'
                else:
                    
            if random.random() < 0.2:
                t = round(player.cal_damage*0.4)
                enemy.health -= t
                a = f'The {enemy["name"]} effectively blocked your attack. Dealt {t} damage'
            else:
                t = round(player.cal_damage*0.6)
                enemy.health -= t
                a = f'The {enemy["name"]} blocked your attack. Dealt {t} damage'
        elif isinstance(player_action, dict):
            player, enemy = Magic_Damage_2_Enemy(player, enemy, player_action)
        elif player_action == 'run':
            a = f'The {enemy["name"]}blocked thin air. you ran but he caught up with you. Unlucky'
        else:
            a = f"The {enemy["name"]} for some reason tried to block while you were standing at a reasonable distance."


    a = 'string for happening'
    return player, enemy, a
