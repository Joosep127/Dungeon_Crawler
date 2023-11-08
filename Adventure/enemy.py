import random
import json

def Select_Enemy(depth, zone):
    with open("Data/Enemies.json", 'r') as f:
        a = json.load(f)[depth][zone]
    key = random.choice(list(a.keys()))
    with open("Data/Enemy_Element_Weaknesses.json", 'r') as f:
        d = json.load(f)[a[key]['type'].title()]
    return {**a[key], 'name': key, 'max_health': a[key]["health"], 'weaknesses': d, 'afflictions': []}

def Affliction_Select(player):
    with open("Data/Gain_Afflictions.json", 'r') as f:
        a = json.load(f)[player.zone]
    return(player.add_afflictions(a))

def Magic_Damage_2_Enemy(player, enemy, player_action):
    temp = enemy['weaknesses'][player_action["element"]]
    if isinstance(player_action["value"], int):
        player_action["value"] = round(player_action["value"]*temp)

    if temp < 0.9:
        temp = "Due to the enemies element, your spell was weakened.\n"
    elif temp > 1.1:
        temp = "Due to the enemies element, your spell was strengthened.\n"
    else:
        temp = "\n"

    if player_action["type"] == "damage":
        enemy['health'] -= player_action["value"]
        temp += f'The {player_action["name"]} spell did {player_action["value"]} damage.'
    elif player_action["type"] == "healing":
        player.add_hp(player_action["value"])
        temp += f'The {player_action["name"]} spell healed you for {player_action["value"]}.'
    elif player_action["type"] == "self_duration":
        player.add_afflictions(player_action["name"])
    elif player_action["type"] == "duration":
        enemy['afflictions'].append({player_action["type"]: player_action["value"]})
        temp += f'The {player_action["name"]} afflicted the enemy for {player_action["value"]} rounds.'
    elif player_action["type"] == "disruption":
        enemy['afflictions'].append({player_action["type"]: {'value':player_action["value"], 'duration': 3}})
        temp += f'The {player_action["name"]} afflicted the enemy for {player_action["value"]} rounds.'
    else:
        temp += f'No such spell type as  {player_action["type"]} exists. This spell has the name of {player_action["name"]}'

    return [player, enemy, temp]

def Damage_Dolen(enemy):
    if enemy['can_use_magic']:
        raw_mana = random.uniform(enemy['mana_range'][0], enemy['mana_range'][1])
        mana = min(max(raw_mana, 0), 1)
        minimum_damage = max(round(enemy["attack"] * 0.1), 1)
        damage_dolen = round(enemy["attack"] * (1 - random.uniform(*enemy['attack_health_modifier_range'])) * (mana + 0.1))
        damage_dolen = max(damage_dolen * enemy['int'] / 4, minimum_damage)
    else:
        damage_dolen = max(round(enemy["attack"] * enemy['int'] / 4 * (1 - random.uniform(*enemy['attack_health_modifier_range']))),1)
    return(damage_dolen)

def Decide_Action(enemy, player):
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
            action = random.choice(["attack", "afflict"])
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
            action = random.choice("afflict")
    else:
        action = 'There has been a bug with the enemy INT json file. the range for INT has to be 1-4'
    return(action)

def Enemy_Player_Interaction(player, enemy, player_action, message):

    enemy_action = Decide_Action(enemy, player)

    if player_action == 'run' and random.random() < 0.4: #If you succesfully run away
        if enemy_action == 'heal':
            b = 'healing itself.'
        elif enemy_action == 'afflict':
            b = 'trying to sneeze on you.'
        else: 
            b = enemy_action + 'ing' + ' you.'
        a = [True, 'You miraculously ran away while the enemy was ' + b]

    elif enemy_action == 'nothing':
        if player_action == 'attack':
            t = player.cal_damage()
            if random.random() < 0.3: 
                t = round(t*1.5)
                a = "[Critical Hit!]\n"
            else: a = ""
            enemy["health"] -= t
            if enemy["health"] <= 0:
                a += f'The {enemy["name"]} was just standing there non-threateningly when you ruthlessly killed it with {t} damage.'
            else:
                enemy["health"] -= t
                a += f'While the {enemy["name"]} was sitting on the ground and picking flowers for it\'s dead grandmother you brutally smashed it with {t} damage'
        elif player_action == 'run':
            a = f'You somehow failed to run away from the enemy, who was doing nothing to stop you from escaping.'
        elif isinstance(player_action, dict):
            player, enemy, a  = Magic_Damage_2_Enemy(player, enemy, player_action)
            if enemy["health"] <= 0:
                a += f'The {enemy["name"]} tried to block your attack but you ruthlessly cast {player_action["name"]} easily by passing its attempt, killing it instantly.'
        else:
            a = "The both of you just sit and look at each other."


    elif enemy_action == 'block':
        if player_action == 'attack':
            if random.random() < 0.2:
                t = round(player.cal_damage()*0.4)
                enemy.health -= t
                a = f'\nThe {enemy["name"]} effectively blocked your attack. Dealt {t} damage'
            else:
                t = round(player.cal_damage()*0.6)
                enemy["health"] -= t
                a = f'The {enemy["name"]} blocked your attack. Dealt {t} damage'
            if enemy["health"] <= 0:
                a += f'The aftershock of the attack, made the {enemy["name"]} pass out.'
        elif isinstance(player_action, dict):
            player, enemy, a = Magic_Damage_2_Enemy(player, enemy, player_action)
            if enemy["health"] <= 0:
                a += f'The {enemy["name"]} tried to block your attack but you ruthlessly cast {player_action["name"]} easily by passing its attempt, killing it instantly.'
            else:
                a += f'The {enemy["name"]} was sitting on the floor when you ruthlessly cast {player_action["name"]} dealing {player_action["value"]}'
        elif player_action == 'run':
            a = f'While the {enemy["name"]} blocked thin air. You tried ran but he caught up with you. Unlucky'
        else:
            a = f'The {enemy["name"]} for some reason tried to block while you were standing at a reasonable distance.'
    

    elif enemy_action == 'heal':
    
        healt = 0.4*enemy["max_health"]

        if player_action == 'attack':
            t = player.cal_damage()
            if random.random() < 0.3: 
                t *= 1.5
                a = "[Critical Hit!]\n"

            enemy["health"] -= t
            if enemy["health"] <= 0:
                a += f'The {enemy["name"]} tried to heal itself but you ruthlessly killed it with {t} damage before it could.'
            else:
                enemy["health"] += healt
                a += f'You battered The {enemy["name"]} with {t} damage, but he healed for {healt}'
        elif player_action == 'run':
            a = f'The {enemy["name"]} was healing itself when you started booking it but he somehow caught up with you. Unlucky'
        elif isinstance(player_action, dict):
            player, enemy, a = Magic_Damage_2_Enemy(player, enemy, player_action)
            if enemy["health"] <= 0:
                a += f'The {enemy["name"]} tried to heal itself but you ruthlessly cast {player_action["name"]} before it could.'
            else:
                a += f'You cast {player_action["name"]} on the {enemy["name"]} but it quickly healed itself for {healt} Hp.'

        else:
            a = f'The {enemy["name"]} healed itself while you were standing at a reasonable distance. Good job 👍'
        

    elif enemy_action == 'attack':
    
        damage_dolen = Damage_Dolen(enemy)
        player.lose_hp(damage_dolen)

        if player_action == 'attack':
            t = player.cal_damage()
            if random.random() < 0.1: 
                t *= 2
                a = "[Critical Hit!]\n"
            else:
                a = ""
            
            player.lose_hp(damage_dolen)
            
            enemy["health"] -= t

            if enemy["health"] <= 0:
                if enemy['can_use_magic']:
                    a += f'The {enemy["name"]} cast a [{enemy["type"]}] type spell on you dealing {damage_dolen}. This however angered you and you administered an outrageous ass-whooping dealing {t}'
                else:
                    a += f'''The {enemy["name"]} smacked you with all of it's might dealing {damage_dolen}. This however angered you and you administered an outrageous ass-whooping dealing {t}'''
            else:
                if enemy['can_use_magic']:
                    a += f'The {enemy["name"]} cast a [{enemy["type"]}] type spell on you dealing {damage_dolen}, while the Ass goblin(you) dealt {t}.'
                else:
                    a += f'''The 2 idiots smacked themselves the {enemy["name"]} dealt {damage_dolen}. and the Ass goblin(you) dealt {t} dmg to it's enemy.'''

        elif isinstance(player_action, dict):
            player, enemy, a = Magic_Damage_2_Enemy(player, enemy, player_action)
            if enemy["health"] <= 0:
                a += f'\nThe {enemy["name"]} enemy dealt {damage_dolen} damage to you before fainting from your attack.'
            else:
                a += f'\nThe {enemy["name"]} got mad at your mad skills so it dealt {damage_dolen} damage to you in retaliation.'
            

        elif player_action == 'run': 
            if enemy['can_use_magic']:
                a = f'The {enemy["name"]} cast a [{enemy["type"]}] type spell while you were running away dealing {damage_dolen-2}. You fell on your face dealing an extra 2 damage, the enemy caught up with you.'
            else:
                a = f'''When you tried running away the {enemy["name"]} teleported infront of you saying 'お前はもう死んでいる' and it smacked you for {damage_dolen}.'''
            
        else:
            if enemy['can_use_magic']:
                a = f'The {enemy["name"]} cast a [{enemy["type"]}] type spell while you were obliviously standing there dealing {damage_dolen} damage'
            else:
                a = f'While you were doing jackshit the {enemy["name"]} walked infront of you and kneecapped you for {damage_dolen} damage'
            
    
    elif enemy_action == 'afflict':
        player, temp = Affliction_Select(player)
        if player_action == 'attack':
            t = player.cal_damage()
            if random.random() < 0.1: 
                t *= 2
                a = "[Critical Hit!]\n"

            enemy["health"] -= t

            if enemy["health"] <= 0:
                a += f'The {enemy["name"]} was trying to cast an affliction on you but you being a no nonsense bossman kind of person killed him before that, dealing {t} damage'
            else:
                a += f"{temp}, while the Ass goblin(you) dealt {t}."

        elif isinstance(player_action, dict):
            player, enemy, a = Magic_Damage_2_Enemy(player, enemy, player_action)
            if enemy["health"] <= 0:
                a += f'\nThe {enemy["name"]} afflicted you with {temp} before fainting from your attack.'
            else:
                a += f"\n{temp}"
        elif player_action == 'run': 
            a = f"{temp}, while you were trying to run away. The enemy despite this caught up with you."
        else:
            a = f"{temp}, while you were standing at a reasonable distance."
    if isinstance(a, list):
        return player, enemy, a
    return player, enemy, a + message