import random
import json
from math import ceil
#gei
class Equipment:
    def __init__(self, name, slot, stat):
        self.name = name
        self.slot = slot
        self.stat = stat 

def None_Equipment(a):
    Equipment("None", a, 0)

def Create_Equipment(a, slot=None):
    if slot == None:
        slot = random.choice([
            "Helmet",
            "Chestplate",
            "Leggings",
            "Boots",
            "Sword"])
    
    with open("Data/Equipment_types.json", 'r') as f: 
        weapon = random.choice(json.load(f)[slot])
    name = "The " + random.choice(open('Data/names.txt').readlines()).replace("\n", "") + " " + weapon["weapon"]

    return(Equipment(name, slot, ceil(a*weapon["mod"])))