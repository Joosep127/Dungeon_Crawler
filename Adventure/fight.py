import time
import json
import random
from misc_functions import Combat_Hud
from Adventure.enemy import Select_Enemy, Decide_Action, Enemy_Player_Interaction
from Adventure.misc_zones import Loot


def Magic(player,enemy, can_see_stats):
    spells = player.spells
    if spells == {}:
        return player, 'No spells'
    has_used_spells = False
    happening = ""
    while True:
        Combat_Hud(player, enemy, can_see_stats)
        print(happening)
        print(f"{'0':^10}Exit the Spell menu")
        print('-'*22)
        print("{:^10} {:^5} {:^5} {:^15} {:^7} {}".format("Index", "Cost", "LVL", "Spell", "Element", "Base_effect"))
        

        for x, i in enumerate(sorted(player.spells.keys()), start=1):
            spell = player.info_spell(i)
            print("{:^10} {:^5} [{:^5}] {:^15} {:^7} {}".format(x, spell["cost"], spell["lvl"], i, spell["element"], spell["value"]))
        print('-'*22)
        a = input("Select: ")
        if not a.isdigit():
            happening = "Please select a correct index."
            continue
        a = int(a)

        if a == 0 and not has_used_spells:
            return player, "exit"
        if a == 0:
            return player, ""
        if 0 < a <= len(player.spells.keys()):
            pass
        else:
            happening = "Please select a correct index."
            continue
        name = sorted(player.spells.keys())[a-1]
        a = player.info_spell(name)
        break
    
    return player, {"type":a["type"], "element":a["element"], "value":a["value"], "name":name}
#UNFINISHED

def Inventory(player,enemy, can_see_stats):
    inv = {x:i for x,i in player.inventory.items() if i != 'Equipment'}
    has_consumed_item = False
    happening = "\n"
    while True:
        Combat_Hud(player, enemy, can_see_stats)
        print(happening)
        print('-'*22)
        print("{:^10} [{:<5}] {:<12} {:<5}".format("Index", "Amount", "Item", "Effectivness"))
        t = "\n"
        print(f"\n{'0':^10}Exit the inventory")
        print('-'*22)
        
        index = 1
        dic = {}
        for item, values in inv.items():
            dic[index] = item
            for value in values:
                print(f"{index:^10} [{values.count(value):^5}] {item:<20} {value:<5}")
                index += 1
        a = input("Select: ")
        
        if not a.isdigit():
            happening = "Please Enter an index."
            time.sleep(0.4)
            continue
        
        if a == '0' and not has_consumed_item:
            return player, "exit"
        has_consumed_item = True
        if a == '0':
            return player, ""
        if 0 < int(a) < index:
            pass
        else:
            happening = "Please select a correct index."
            continue
        a = int(a)
        for i in dic.keys():
            if i <= a:
                d = i
        
        happening = player.use_inventory(dic[d], player.inventory[dic[d]][a-d])
        index -= 1


def Fight(player):

    escaped = [False]
    enemy = Select_Enemy(str(player.depth), player.zone)
    happening = "\n\n\n\n\n"
    happening += random.choice([
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
    happening += "\n"
    t = "\n"

    while True:

        while happening.count("\n") > 5:
            happening = happening[happening.find("\n")+1:]

        if t == "\n":

            is_slip = False
            can_see_stats = True
            can_attack = True
            can_cast_magic = True

            for x, i in player.afflictions.keys():
                if i["type"] == "can_attack":
                    afflicted_attack = x
                    can_attack = False
                elif i["type"] == "can_cast_magic":
                    afflicted_magic = x
                    can_cast_magic = False
                elif i["type"] == 'chance_to_fail_attack':
                    is_slip = True
                elif i["type"] == 'cant_see_enemy_stats':
                    can_see_stats = False

            happening += player.round_start()


            if not can_attack or not can_cast_magic:
                happening += "\nDue to your afflictions you can't "
                if not can_attack:
                    happening += "Attack"
                    if not can_use_magic:
                        happening += " or"
                    else:
                        happening += "."
                if not can_use_magic:
                    happening += " use magic."

  
        options = ['Attack' if can_attack else 'Struggle', 'Magic' if can_cast_magic else "", "Rest", 'Inventory', 'Run']
        if '' in options: options.remove('')

        if escaped[0]:
            Combat_Hud(player, enemy, can_see_stats)
            print(happening)
            print('\n')
            input('[ENTER] To continue')
            break
        Combat_Hud(player, enemy, can_see_stats)
        print(happening)

        if enemy["health"] <= 0:
            print(f"With the {enemy['name']} as good dead you continue on your jurney.")
            input("\n[ENTER] to continue")
            break

        print("{}{:^10} {:<5}".format(t, "Index", "Action"))
        t = "\n"
        print('-'*22)
        for x,i in enumerate(options, start=1):
            print(f'{x:^10} {i:<5}')
        
        

        a = input("Select: ")
        if a.isdigit():
            a = int(a)
            if 0 <= int(a)-1 < len(options):
                a = options[a-1]
                if a == 'Attack':
                    if is_slip:
                        if random.random() < 0.2:
                            print("Due to it being extremely slippery you slipped and your attack was canceled ♿. The enemy got an extra turn.")
                            a = ''
                            time.sleep(0.8)
                elif a == 'Struggle':
                    if (random.random()*10)**(1+player.multipliers["luck"])/10 < 0.8:
                        del player.afflictions[afflicted_attack]
                        print("By struggling you managed to break free of the " + afflicted_attack + ". You can use attack again!")
                        time.sleep(0.6)
                    else:
                        print("You tried to but you couldn't break free of the " + afflicted_attack)
                        time.sleep(0.4)

                elif a == 'Magic':
                    player, a = Magic(player,enemy, can_see_stats)
                    if a == "No spells":
                        t = "*You have no spells to Cast\n"
                        continue
                    if a == "No magic":
                        t = "*You cancel the magic\n"
                        continue
                elif a == 'Magic_Struggle':
                    if (random.random()*10)**(1+player.multipliers["luck"])/10 < 0.8:
                        del player.afflictions[afflicted_magic]
                        print("You bent your will and you managed to break free of the " + afflicted_magic + ". You can use magic again!")
                        time.sleep(0.6)
                    else:
                        print("You tried to but you couldn't break free of the " + afflicted_magic)
                        time.sleep(0.4)
                elif a == 'Inventory':
                    player, a = Inventory(player,enemy, can_see_stats)
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
        
        if isinstance(a, str):
            a = a.lower()
        player, enemy, temp = Enemy_Player_Interaction(player, enemy, a, t)

        if isinstance(temp, list):
            escaped = True
            happening += temp[1]
        else:
            happening += temp

        
        
    if "undead" in player.afflictions:
        player.health *= 2
        player.max_health *= 2

    player.reset_afflictions()

    if random.random() < 0.3 and enemy["health"] <= 0:
        #player = Loot(player, enemy["name"])
        pass
    
    return(player)