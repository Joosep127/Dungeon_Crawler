import os
clear = lambda: os.system('cls')

def Hud(player):
    clear()
    print(f"{player.name}, {player.clss}")
    print(f"Hp: {player.health}/{player.max_health} | Magic: {player.mana}/{player.max_mana} | {player.coin}$ | Lvl: {player.level}")
    #xp_needed = floor(20 * (player.multipliers["lvl_up"] ** (player.level - 1)) - player.xp)
    #print(f"xp: {player.xp}\n")
    print("\n")