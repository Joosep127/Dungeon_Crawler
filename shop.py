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


def Generate_Equipment(stat,cost,amount, probability):
    return [[Create_Equipment(random.randint(*stat)),random.randint(*cost)] for i in range(amount) if probability >= random.randint(0, 100)]

def Generate_Shop_Inv(depth):
    with open("Data/Shop_Items.json", 'r') as f:
        shop_data = json.load(f)
        player_depth_str = str(depth)
        shop_items = [{"name":j,"effect":random.randint(*i["effect"]), "cost":random.randint(*i["cost"]), "amount": random.randint(1,i["max"])}
                        if (j != "Armor") else Generate_Equipment(i["effect"], i["cost"], random.randint(1,i["max"], i.get("probability", 0)))
                        for j, i in shop_data[player_depth_str].items() 
                        if i.get("probability", 0) >= random.randint(0, 100) and j != 'Armor']    
    return(shop_items)

def Shop(player):
    
    shop_items = Generate_Shop_Inv(player.depth)

    while True:
        Hud(player)
        Display_Shop_Items(shop_items)
        a = input("Select what Item to buy: \n")


        break