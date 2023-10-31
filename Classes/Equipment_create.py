import random
import json
#gei
class Equipment:
    def __init__(self, name, slot, stat):
        self.name = name
        self.slot = slot
        self.stat = stat

def Create_Equipment(a):
    slot = random.choice([
        "Helmet",
        "Chestplate",
        "Leggings",
        "Boots",
        "Sword"])
    
    with open("Data/Equipment_types.json", 'r') as f: 
        weapon = random.choice(json.load(f)[slot])
    name = "The " + random.choice(open('Data/names.txt').readlines()).replace("\n", "") + " " + weapon["weapon"]

    return(Equipment(name, slot, int(a*weapon["mod"])))