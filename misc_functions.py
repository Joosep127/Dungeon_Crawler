import os
from Classes.player import Debug_Create 
clear = lambda: os.system('cls')

def Hud(player):
    clear()
    print(f"{player.name}, {player.clss}")
    print(f"Hp: {player.health}/{player.max_health} | Magic: {player.mana}/{player.max_mana} | {player.coin}$ | Lvl: {player.level}")
    #xp_needed = floor(20 * (player.multipliers["lvl_up"] ** (player.level - 1)) - player.xp)
    #print(f"xp: {player.xp}\n")
    print("\n")

def Combat_Hud(player, enemy):
    clear()
    print("{:<41}|	{}".format(f'{player.name}, {player.clss}', enemy['name']))
    print("Hp: {:<14}| Magic: {:<14}|	Hp: {:<14}".format(f'{player.health}/{player.max_health}', f'{player.mana}/{player.mana}', f'{enemy["health"]}/{enemy["max_health"]}'))
    print("DMG: {:<13}| DEF: {:<16}|	DMG: {:<13} \n".format(f'{player.damage}(+{player.equipment_damage()})', player.equipment_defence(), enemy["attack"]))