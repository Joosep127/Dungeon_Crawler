from math import floor

class Player:
    
    multipliers = {
    "xp": 1.1,
    "dmg": 1,
    "hp": 2, #default 2
    "lvl_up": 1.1, #default 1.5
    "coin": 1.0
}
    equipment = {
    
}
    
    def __init__(self, name, health, mana, damage, coin):
        self.name = name
        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.damage = damage
        self.xp = 0
        self.level = 1
        self.coin = coin
    
    def add_coin(self, add):
        self.coin += add*self.multipliers["coin"]
        
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
        self.xp += floor(add*self.multipliers["xp"])
        base_xp = floor(20 * (self.multipliers["lvl_up"] ** (self.level - 1)))
        while self.xp >= base_xp:
            self.xp -= base_xp
            self.level += 1
            self.max_health += self.multipliers["hp"]
            self.health = self.max_health
            self.damage += self.multipliers["dmg"]
            print('Level up!')

