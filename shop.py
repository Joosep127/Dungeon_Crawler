import os
from math import ceil
import json
import random
import time
from misc_functions import Hud
from Classes.Equipment_create import Create_Equipment

def Display_Shop_Items(shop_inverntory):

    print("Shop Inventory \n")
    a = ''
    for x, i in enumerate(shop_inverntory):
        if not isinstance(i, dict): continue
        a += "{:^10} {:<10} {:<10} {:<15} \n".format(str([x+1]), f'{i["cost"]}$', f'*{i["amount"]}',i["name"])
    if a != '':  
        print("Items:")
        print("{:^10} {:<10} {:<10} {:<15}".format("Index", "Cost", "Amount Left","Name"))
        print(a)
        c = x
    else:
        c = 0
        
    b = ''
    for i in shop_inverntory:
            if isinstance(i, dict): 
                continue
            for x, p in enumerate(i):
                b += "{:^10} {:<15} {:<10}\n".format(str([c+x+1]), f'{p[1]}$',p[0].name)
            c += x
    
    if b != '':
        print("Equipment:")
        print("{:^10} {:<15} {:<10}".format("Index", "Cost","Name"))
        print(b)
    
    if a == '' and b == '':
        print("The store shelf's are completely empty.")


def Generate_Equipment(stat, probability):
    if probability >= random.randint(0, 100):
        return Create_Equipment(random.randint(*stat))

def Generate_Shop_Inv(depth):
    with open("Data/Shop_Items.json", 'r') as f:
        shop_data = json.load(f)
    player_depth_str = str(depth)
    shop_items = []
    if player_depth_str in shop_data:
        for item_name, item_properties in shop_data[player_depth_str].items():
            probability = item_properties.get("probability", 100)
            if probability >= random.randint(0, 100):
                if item_name == "Armor":
                    for _ in range(random.randint(1, item_properties.get("max", 1))):
                        equipment = [Generate_Equipment(item_properties["effect"], probability), random.randint(*item_properties["cost"])]
                        shop_items.extend(equipment)
                else:
                    shop_items.append({
                        "name": item_name,
                        "effect": random.randint(*item_properties["effect"]),
                        "cost": random.randint(*item_properties["cost"]),
                        "amount": random.randint(1, item_properties.get("max", 1))
                    })
    return(shop_items)

def Shop(player):
    
    shop_items = Generate_Shop_Inv(player.depth)

    while True:
        Hud(player)
        Display_Shop_Items(shop_items)
        a = int(input("Select what Item to buy: \n"))-1

        print(shop_items[a])
        if 0 < a <= len(shop_items):
            if isinstance(shop_items[a], dict):
                if player.coin >= shop_items[a]['cost']:
                    player.coin -= shop_items[a]['cost']
                    player.add_inventory({'name' : shop_items[a]['name'], 'effect' : shop_items[a]['effect']})
                else:
                    print("You don't have enough money")
            elif isinstance(shop_items[a], dict):
                if player.coin >= shop_items[a][1]:
                    player.coin -= shop_items[a][1]
                    player.add_inventory(shop_items[a][0])
                else:
                    print("You don't have enough money")

        print(player.inventory)
        exit()

        break