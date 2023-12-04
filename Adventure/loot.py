import random

def Level_Up(player):
    return player

def Loot(player, condition="None"):
    if condition == "Zone":
        pass
    elif condition == "Enemy":
        pass
    elif condition == "Levelup":
        player = Level_Up(player)
        
    elif condition == "None":
        pass
    return(player)