from math import floor
import json
from collections import Counter
from Adventure.loot import Loot
import os
import time

clear = lambda: os.system('cls')

def Debug_Create(name, health, mana, damage, coin, clss):
    return(Player(name, health, mana, damage, coin, clss)) # Player("Mr. Moneybags", 100, 100, 100, 100, "The Monopoly man")
class Player:
    equipment = {
        "Helmet": None,
        "Chestplate": None,
        "Leggings": None,
        "Boots": None,
        "Sword": None    
}
    def __init__(self, name, health, mana, damage, coin, clss):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.damage = damage
        self.xp = 0
        self.level = 1
        self.coin = coin
        self.clss = clss
        self.multipliers = {
            "xp": 1.0,
            "dmg": 2,
            "hp": 2, #default 2
            "mana": 2, #default 2
            "lvl_up": 1.5, #default 1.5
            "coin": 1.0,
            "equipment": 0.5,
            "luck": 1.0
        }
        self.affliction_multipliers = {
            "do_damage" : 1.0,
            "do_damage_additive" : 0,
            "take_damage" : 1.0
        }
        self.skills = Counter(fight=0,magic=0,rest=0)
        self.spells = {}
        self.afflictions = {}
        self.inventory = {"Equipment": []}
        self.depth = 1
        self.zone = None
        self.timer = 0 #How long you have stayed in one zone
        self.conditionals = []

    def cal_damage(self):
        return( (self.equipment_damage() + self.damage**self.affliction_multipliers['do_damage'] + self.affliction_multipliers["do_damage_additive"])**self.affliction_multipliers['do_damage'])
    
    def cal_defence(self):
        return(sum([self.equipment[i].stat for i in self.equipment.keys() if i != 'Sword' and self.equipment[i] is not None]))
    
    def add_coin(self, add):
        self.coin += add * self.multipliers["coin"]
        
    def lose_hp(self, lost, args=()):
        lost *= self.affliction_multipliers['take_damage']
        self.health -= round(lost)
        
        if self.health <= 0:
            if args == ():
                print('You died due to a heart attack\n\n')
            elif args == "affliction":
                print('You died due to your afflictions\n\n')
            elif args == "stupid":
                print('You died due to your own stupidity :P\n\n')
                
            input("[ENTER] to close the game")
            exit()

        return(lost)
        
    def add_hp(self, add):
        self.health += add
        if self.health > self.max_health:
            self.health = self.max_health

    def add_mana(self, add):
        self.mana += add
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def lose_mana(self, lost):
        self.mana -= lost
        if self.mana < 0:
            self.mana = 0
            return('No Mana')
        return(None)

    def add_xp(self, add):
        xp_gained = floor(add * self.multipliers["xp"])
        print(f"You gained {xp_gained} xp.")
        self.xp += xp_gained
        base_xp = floor(20 * (self.multipliers["lvl_up"] ** (self.level - 1)))
        lvl = False

        while self.xp >= base_xp:
            self.xp -= base_xp
            self.level += 1
            self.max_health += self.multipliers["hp"]
            self.health = self.max_health
            self.max_mana += self.multipliers["mana"]
            self.mana = self.max_mana
            self.damage += self.multipliers["dmg"]
            print("Level Up!")
            self = Loot(self, "Levelup")
            lvl = True
            
        if lvl:
            return(["Levelup", xp_gained])
        return(["None",xp_gained])

    def add_spell(self, a):
        spell = find_spell(a)
        if isinstance(spell, dict):
            if a in self.spells:
                self.spells[a]["lvl"] += 1
            else:
                self.spells[a] = {**spell, "lvl": 1}

    def info_spell(self, a):
        if a not in self.spells:
            print("Spell such as {a} has not been found")
            time.sleep(1)
            return("damage", "grass", 0, 0)
        
        spell = self.spells[a]

        mult = spell["lvl"] ** spell["attribute"]["strength_modifier"]
        value = round(spell["attribute"]["value"] * mult)
        cost = round(spell["cost"] * mult)

        return({"type":spell["attribute"]["type"], "element":spell["attribute"]["element"], "value":value, "cost":cost, "lvl":spell["lvl"]})

    def reset_afflictions(self):
        self.afflictions = {}

    def add_afflictions(self, a):
        a = a.lower()
        name = a
        a = find_affliction(a)
        if not a:
            print("NO AFFLICTION FOUND AS " + a)
            time.sleep(1)
            return
        if name in self.afflictions:
            if "gain" in a.keys():
                if a["gain"] in self.afflictions():
                    return (f"An affliction {list(a.keys())[0]} was cast on you but you could attain it because you had an upgraded version of it already called {a.get('gain', 'unknown')}.")
                else:
                    self.afflictions[a["gain"]] = find_affliction(a["gain"])
                    return(f"An affliction {list(a.keys())[0]} was cast on you but it upgraded to {a.get('gain', 'unknown')}.")
        self.afflictions[name] = a
        return(f"An affliction {list(a.keys())[0]} was cast on you.")
    
    def round_start(self):
        t = ''
        do_damage = 1
        do_damage_additive = 0
        take_damage = 1
        lose_hp = 0
        add_hp = 0
        lose_mana = 0
        for x, i in self.afflictions.items():
            if "activated" in i:
                if i['activated'] == 0:
                    i["activated"] = 1
                    if i['lose_half_max_hp']:
                        self.health /= 2
                        self.max_health /= 2
                    elif i['type'] == "take_damage_half_hp":
                        lose_hp += self.health/2
                else:
                    continue
            
            if i['type'] == "do_damage":
                if i["operator"] == "multiplicative":
                    do_damage *= i['value']
                elif i["operator"] == "additive":
                    do_damage_additive += i['value']
                else:
                    print(f'unknown operator type {i["operator"]}')

            elif i['type'] == "take_damage":
                if i["operator"] == "multiplicative":
                    take_damage *= i['value']
                elif i["operator"] == "additive":
                    lose_hp += i['value']
                else:
                    print(f'unknown operator type {i["operator"]}')
            
            elif i['type'] == "lose_hp":
                lose_hp += i['value']

            elif i['type'] == 'lose_mana':
                lose_mana += i['value']

            elif i['type'] == 'do_nothing':
                pass
            
            else:
                print(f"Unknown affliction {i}")


            if "lose_next_turn" in i.keys():
                if i["lose_next_turn"] <= 0:
                    del self.afflictions[x]
                else:
                    self.afflictions[x]["lose_next_turn"] -= 1
        
        self.affliction_multipliers["do_damage"] = do_damage
        self.affliction_multipliers["do_damage_additive"] = do_damage_additive
        self.affliction_multipliers["take_damage"] = take_damage
        self.add_hp(add_hp)
        self.lose_hp(lose_hp, "affliction")

        t0 = "\nDue to your afflictions you gained "
        t1 = add_hp-lose_hp
        t2 = do_damage_additive
        t3 = take_damage

        if t1 == 0 and t2 == 0 and t3 == 1:
            return("")
        if t1 != 0:
            t0 += f"{t1} hp"
        if t2 == 0 and t3 == 1:
            return(t0 + ".")
        else:
            t0 += " "
        if t1 != 0:
            t0 += "and gained multipliers to your stats: "
        else:
            t0 += "multipliers to your stats: "
        if t2 != 0:
            t0 += f"{t2} * dmg "
        if t3 != 1:
            t0 += f"{t3} * Damage taken."

        return(t0)
    
    def add_inventory(self, item):
        if not isinstance(item, dict):
            self.inventory["Equipment"].append(item)
        elif item["name"] in self.inventory:
            self.inventory[item["name"]].append(item["effect"])
        else:
            self.inventory[item["name"]] = [item["effect"]]
        for i in self.inventory:
            if isinstance(self.inventory[i], list):
                if i != "Equipment": 
                    self.inventory[i].sort()
                elif i == "Equipment": 
                    slot_order = ['Boots', 'Leggings', 'Chestplate', 'Helmet', 'Sword']
                    self.inventory[i].sort(key=lambda x: (slot_order.index(x.slot), x.stat), reverse=True)
    
    def use_inventory(self, item):
        if not isinstance(item, dict):
            self.add_equipment(item)
            return()
        elif item["name"] == "Health Potion":
            self.add_hp(item['value'])
            t = f"You gained +{item['value']} hp."
        elif item["name"] == "Mana Potion":
            self.add_mana(item['value'])
            t = f"You gained +{item['value']} mana."
        else:
            t = "You used an item that cannot be used. Gongrats. You lost the " + item["name"] + " now."
        self.lose_inventory({'name': item["name"], 'effect': item['value']})
        return(t)

    def lose_inventory(self, item):
        if not isinstance(item, dict):
            del self.inventory["Equipment"][self.inventory["Equipment"].index(item)]
            return()

        elif item["name"] not in self.inventory:
            print("[ERROR]Item that you wanted to remove does not exist in your invetory")
            time.sleep(2)
            return()
        
        self.inventory[item["name"]].remove(item["effect"])
        if self.inventory[item["name"]] == []:
            del self.inventory[item["name"]]
             
    def add_equipment(self, item): #name, slot stat
        if self.equipment[item.slot] == None: 
            self.equipment[item.slot] = item
        else:
            self.add_inventory(self.equipment[item.slot])
            self.equipment[item.slot] = item
        self.lose_inventory(item)

    def remove_equipment(self, item): #name, slot stat
        self.equipment[item.slot] = None
        add_inventory(item)
    
    def equipment_damage(self):
        if self.equipment['Sword'] == None:
            return(0)
        return(self.equipment['Sword'].stat)

    def add_skill(self, a, amount=None):
        if a in self.skills:
            if amount:
                self.skills[a] += amount
            else:
                self.skills[a] += 1

def find_affliction(a):
    try:
        with open("Data/Afflictions.json") as f:
            return(json.load(f)[a])
    except:
        print("No affliction was found with the name " + a)
        time.sleep(1)
        return None
    
def find_spell(a):
    try:
        with open("Data/Spells.json") as f:
            return(json.load(f)[a])
    except:
        print("No affliction was found with the name " + a)
        time.sleep(1)
        return None

def Change_name():
    t = ''
    while True:
        clear()
        print(t)
        name = input("Enter your name: ")
        if len(name) > 20:
            t = "*Name is too long. It must be 20 characters or less."
        else:
            try:
                name.encode('ascii')
            except UnicodeEncodeError:
                t = "*Name contains non-ASCII characters. Please enter a valid Player name."
            else:
                name = name.title()
            break
    clear()
    t = ''
    while True:
        a = input(f"{name}. Is this username correct? \n Index \n  [0] - No \n  [1] - Yes \n {t} \nSelect Index: ")
        if a == '0':
            clear()
            return Change_name()
        elif a == '1':
            return name
        else:
            clear()
            t = '*Please insert you answer again.'
        

def Create(name=None):
    clear()
    t = ''
    if not name:
        name = Change_name()
    game_classes = {
    'The Regular Guy': {
        'name': '*Has a ketchup stain on his shirt',
        'health': 500,
        'mana': 25,
        'damage': 50,
        'coin': 100,
        'multipliers': {}
    },
    'The Thief': {
        'name': '*Is decked out with handbags and whatnot from having stolen soo much loot from old ladies',
        'health': 400,
        'mana': 10,
        'damage': 50,
        'coin': 50,
        'multipliers': {"coin": 2.0}
    },
    'The Knight': {
        'name': "*Despite the sword's steel blade haven fallen off from countless battles, he still uses the wooden handle to beat monsters into submission",
        'health': 450,
        'mana': 30,
        'damage': 70,
        'coin': 200,
        'multipliers': {}
    },
    'The Rogue': {
        'name': '*Fast and agile, adapts.',
        'health': 500,
        'mana': 70,
        'damage': 70,
        'coin': 75,
        'multipliers': {"xp": 2.7, "dmg": 2, "hp": 4, "lvl_up": 1.35,}
    },
    'The Physically Ill': {
        'name': '*Has the sniffles ): ',
        'health': 200,
        'mana': 10,
        'damage': 50,
        'coin': 10,
        'multipliers': {"xp": 0.7, "dmg": 1, "hp": 1, "mana": 1, "lvl_up": 1.65, "coin": 0.7}
    }    
}
    while True:
        clear()
        print(f'Hello {name}. \n{t}\nClasses: \n')
        for x, (j, i) in enumerate(game_classes.items()):
            print(f'[{x + 1}] : {j} ({i["name"]}) | \n'
                  f'                    Hp: {i["health"]} \n'
                  f'                    Mana: {i["mana"]} \n'
                  f'                    Dmg: {i["damage"]} \n'
                  f'                    Coin: {i["coin"]}')
        choice = input("\nEnter Index: ")

        if choice.isdigit() and 1 <= int(choice) <= len(game_classes):
            selected_class = list(game_classes.keys())[int(choice) - 1]
            print(f'You have chosen: {selected_class}')
            time.sleep(0.6)
            break
        else:
            t = "Invalid choice. Please enter a valid number."

    while True:
        clear()
        print(f"{name}, {selected_class}")
        answer = input(f"Is this correct? \n Index \n  [0] - No \n  [1] - Yes \n{t}\nSelect Index: ").lower()
        if answer == "1":
            break
        elif answer == "2":
            return Create(name)
        else:
            clear()
            t = '*Please insert you answer again.'

    selected_class_data = game_classes[selected_class]
    multipliers = selected_class_data["multipliers"]
    player = Player(name, selected_class_data["health"], selected_class_data["mana"], selected_class_data["damage"], selected_class_data["coin"], selected_class)
    
    for j, i in multipliers.items():
        player.multipliers[j] = i

    return player