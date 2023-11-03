from math import floor
import os
import time
clear = lambda: os.system('cls')

def Debug_Create(name, health, mana, damage, coin, clss):
    return(Player(name, health, mana, damage, coin, clss))
class Player:
    equipment = {
        "Helmet": None,
        "Chestplate": None,
        "Leggings": None,
        "Boots": None,
        "Sword": None    
}
    # Player("Mr. Moneybags", 100, 100, 100, 100, "The Monopoly man")
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
            "equipment": 0.5
        }
        self.spells = {}
        self.inventory = {}
        self.depth = 1
        self.zone = None
        self.timer = 0 #How long you have stayed in one zone
    
    def add_coin(self, add):
        self.coin += add * self.multipliers["coin"]
        
    def lose_hp(self, lost):
        self.health -= lost
        if self.health <= 0:
            print('U ded')
            exit()
        
    def add_hp(self, add):
        self.health += add
        if self.health > self.max_health:
            self.health = self.max_health
        
    def add_xp(self, add):
        xp_gained = floor(add * self.multipliers["xp"])
        self.xp += xp_gained
        base_xp = floor(20 * (self.multipliers["lvl_up"] ** (self.level - 1)))

        while self.xp >= base_xp:
            self.xp -= base_xp
            self.level += 1
            self.max_health += self.multipliers["hp"]
            self.health = self.max_health
            self.max_mana += self.multipliers["mana"]
            self.mana = self.max_mana
            self.damage += self.multipliers["dmg"]
            return(["Levelup", xp_gained])

        return([xp_gained])
    
    def add_spell(self, spell):
        if spell in self.spells:
            self.spells[spell] += 1
        else:
            self.spells[spell] = 1
    
    def add_inventory(self, item):
        if type(item) != dict:
            self.inventory[item] = 'Equipment'
        elif item["name"] in self.inventory:
            self.inventory[item["name"]].append(item["effect"])
        else:
            self.inventory[item["name"]] = [item["effect"]]
    
    def lose_inventory(self, item):
        if item["name"] not in self.inventory:
            print("[ERROR]Item that you wanted to remove does not exist in your invetory")
            time.sleep(2)
            return()
        self.inventory[item["name"]].remove(item["effect"])
        if self.inventory[item["name"]] == []:
            del self.inventory[item["name"]]
    
    def add_equipment(self, item): #name, slot stat
        self.equipment[item.slot] = item

    def remove_equipment(self, item): #name, slot stat
        self.equipment[item.slot] = None
        add_inventory(item)

def Change_name():
    while True:
        name = input("Enter your name: ")
        if len(name) > 20:
            print("Name is too long. It must be 20 characters or less.")
        else:
            try:
                name.encode('ascii')
            except UnicodeEncodeError:
                print("Name contains non-ASCII characters. Please enter a valid Player name.")
            else:
                return(name.title())

def Create():
    name = Change_name()
    game_classes = {
    'The Regular Guy': {
        'name': '*Has a ketchup stain on his shirt',
        'health': 100,
        'mana': 50,
        'damage': 20,
        'coin': 100,
        'multipliers': {}
    },
    'The Thief': {
        'name': '*Is decked out with handbags and whatnot from having stolen soo much loot from old ladies',
        'health': 80,
        'mana': 100,
        'damage': 30,
        'coin': 50,
        'multipliers': {"coin": 2.0}
    },
    'The Knight': {
        'name': "*Despite the sword's steel blade haven fallen off from countless battles, he still uses the wooden handle to beat monsters into submission",
        'health': 150,
        'mana': 30,
        'damage': 40,
        'coin': 200,
        'multipliers': {}
    },
    'The Rogue': {
        'name': '*Fast and agile, adapts.',
        'health': 60,
        'mana': 70,
        'damage': 25,
        'coin': 75,
        'multipliers': {"xp": 2.7, "dmg": 2, "hp": 4, "lvl_up": 1.35,}
    },
    'The Physically Ill': {
        'name': '*Has the sniffles ): ',
        'health': 50,
        'mana': 10,
        'damage': 10,
        'coin': 10,
        'multipliers': {"xp": 0.7, "dmg": 1, "hp": 1, "mana": 1, "lvl_up": 1.65, "coin": 0.7}
    }    
}
    while True:
        clear()
        print(f'Hello {name}. Please choose your character class: ')
        for x, (j, i) in enumerate(game_classes.items()):
            print(f'[{x + 1}] : {j} ({i["name"]}) | \n'
                  f'                    Hp: {i["health"]} \n'
                  f'                    Mana: {i["mana"]} \n'
                  f'                    Dmg: {i["damage"]} \n'
                  f'                    Coin: {i["coin"]}')
        choice = input("Enter the number corresponding to your choice: ")

        if choice.isdigit() and 1 <= int(choice) <= len(game_classes):
            selected_class = list(game_classes.keys())[int(choice) - 1]
            print(f'You have chosen: {selected_class}') 
            time.sleep(1)
            break
        else:
            print("Invalid choice. Please enter a valid number.") 
            time.sleep(1)

    while True:
        clear()
        print(f"{name}, {selected_class}")
        answer = input("Is this correct? [yes, no]: ").lower()
        if answer == "yes":
            break
        elif answer == "no":
            clear()
            return Create()

    selected_class_data = game_classes[selected_class]
    multipliers = selected_class_data["multipliers"]
    player = Player(name, selected_class_data["health"], selected_class_data["mana"], selected_class_data["damage"], selected_class_data["coin"], selected_class)

    for j, i in multipliers.items():
        player.multipliers[j] = i

    return player