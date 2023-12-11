import os
from math import floor
from Adventure.fight import Fight
from misc_functions import Camping_Hud
import random
import time 
clear = lambda: os.system('cls')

def cal_inv_index_size(inv):
    return sum([len(set(i)) for i in inv.values()])

def Inventory(player):
    happening = "\n"
    while True:
        inv = player.inventory.copy()
        e_inv = inv.pop("Equipment", None) 
        Camping_Hud(player)
        print(happening)
        print('-'*22)
        print("{:^10}".format('Index'))
        print(f"\n{'0':^10}Exit the inventory")
        
        print('-'*22)

        index = 1
        dic = {}
        if inv != {}:
            print("Consumables: ")
            print("{:^10} [{:<5}] {:<12} {:<5}".format("", "Amount", "Item", "Effectivness"))
            for item, values in inv.items():
                dic[index] = item
                for value in sorted(set(values)):
                    print(f"{index:^10} [{values.count(value):^5}] {item:<20} {value:<5}")
                    index += 1

        
        if e_inv != []:
            print("{:^10} {:<5} {:<12} {:<5}".format("", "Slot", "Stat", "Name"))
            print("Equipement: ")
            for item in e_inv:
                dic[index] = item
                print(f"{index:^10} [{item.slot:^5}] {item.stat:<20} {item.name:<5}")
                index += 1  
        
        a = input("Select: ")
        
        if not a.isdigit():
            happening = "Please Enter an index."
            time.sleep(0.4)
            continue
        
        if a == '0':
            return player
        if 0 < int(a) < index:
            pass
        else:
            happening = "Please select a correct index."
            continue
        a = int(a)

        if a-1 < len(inv):
            for i in dic.keys():
                if i <= a:
                    d = i
            
            happening = player.use_inventory({"name": dic[d], "value": player.inventory[dic[d]][a-d]})
        else:
            a -= cal_inv_index_size(inv)+1
            happening = player.add_equipment(e_inv[a])
        index -= 1

def Set_Camp(player): 
    happening = '\n'
    while True:
        clear()
        options = ['Inventory', 'Upgrade(Once per zone)' if 'Upgrade(Once per zone)' not in player.conditionals else '', 'Rest(once per zone)'if 'Rest(once per zone)' not in player.conditionals else '', 'Hunt']
        if '' in options: options.remove('')

        Camping_Hud(player)
        print("{:^10} {:^5}\n".format("Index", "Options"))
        print(f"{'0':^10}Exit\n")
        for x, i in enumerate(options):
            print("{:^10} {:^5}".format(x+1, i))    
        print('- '*11)
        print(happening)
        a = input("Select: ")
        if not a.isdigit():
            happening = "\nPlease select a correct index."
            continue
        if not 0 <= int(a) <= len(options):
            happening = "\nPlease select a correct index."
            continue
        if a == "0":
            break
        a = options[int(a)-1]

        if a == "Inventory":
            player = Inventory(player)
            happening = "\nYou closed your inventory."

        elif a == 'Upgrade(Once per zone)':

            if 'Upgrade(Once per zone)' not in player.conditionals:

                temp = input(f"Pick something to upgrade [Helmet, Chestplate, ...] or 0 to exit.\nSelect:")
                if temp == "0":
                    happening = "\nYou stopped upgrading."
                
                if temp in player.equipment.keys():
                    if "+" not in player.equipment[temp].name:
                        player.conditionals.append('Upgrade(Once per zone)')
                        print(".")
                        time.sleep(0.2)
                        print("..")
                        time.sleep(0.2)
                        print("...")
                        player.equipment[temp].name += "+"
                        player.equipment[temp].stat = round(player.equipment[temp].stat*1.5)
                    else:
                        happening = "This equipment has already been upgraded"
                else:
                    happening = "\nYou stopped upgrading."
            else:
                happening = "\nYou've already improved your equipment this zone."

        elif a == 'Rest(once per zone)':
            if 'Rest(once per zone)' not in player.conditionals:
                player.conditionals.append('Rest(once per zone)')
                print(".")
                time.sleep(0.2)
                print("..")
                time.sleep(0.2)
                print("...")
                time.sleep(0.2)
                h = (player.max_health-player.health)/0.3
                happening = f"\nYou gained {h} hp from resting."
            else:
                happening = "\nYou've already rested this zone."

        elif a == 'Hunt':
            player = Fight(player)



    return(player)