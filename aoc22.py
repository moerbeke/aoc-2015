########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from math import inf

"""
    Magic Missile costs 53 mana. It instantly does 4 damage.
    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
    Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
    Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.

    Spell          Effect  Damage  Heal  Armor  Mana  Cost
    -------------------------------------------------------
    Magic_Missile       0       4     0      0     0    53
    Drain               0       2     2      0     0    73
    Shield              6       0     0      7     0   113
    Poison              6       3     0      0     0   173
    Recharge            5       0     0      0   101   229
"""

# Spells
S_Magic_Missile = 'M'
S_Drain         = 'D'
S_Shield        = 'S'
S_Poison        = 'P'
S_Recharge      = 'R'
SPELLS = [
    S_Magic_Missile,
    S_Drain,
    S_Shield,
    S_Poison,
    S_Recharge,
]

EFFECT = {
    S_Magic_Missile: 0,
    S_Drain:         0,
    S_Shield:        6,
    S_Poison:        6,
    S_Recharge:      5
}

DAMAGE = {
    S_Magic_Missile: 4,
    S_Drain:         2,
    S_Shield:        0,
    S_Poison:        3,
    S_Recharge:      0
}

HEAL = {
    S_Magic_Missile: 0,
    S_Drain:         2,
    S_Shield:        0,
    S_Poison:        0,
    S_Recharge:      0
}

ARMOR = {
    S_Magic_Missile: 0,
    S_Drain:         0,
    S_Shield:        7,
    S_Poison:        0,
    S_Recharge:      0
}

MANA = {
    S_Magic_Missile: 0,
    S_Drain:         0,
    S_Shield:        0,
    S_Poison:        0,
    S_Recharge:    101
}

COST = {
    S_Magic_Missile: 53,
    S_Drain:         73,
    S_Shield:       113,
    S_Poison:       173,
    S_Recharge:     229
}

initial_player_hit = 50
initial_player_mana = 500
#initial_player_hit = 10
#initial_player_mana = 250
g_min_mana_spent = None

def solve_1(input_str):
    global g_min_mana_spent
    g_min_mana_spent = inf
    initial_enemy_hit, enemy_damage = parse_input(input_str)
    initial_shield_timer = 0
    initial_poison_timer = 0
    initial_recharge_timer = 0
    min_mana_spent = play(1,
                          initial_player_hit, initial_player_mana,
                          initial_shield_timer, initial_poison_timer, initial_recharge_timer,
                          initial_enemy_hit, enemy_damage)
    return min_mana_spent

def solve_2(input_str):
    global g_min_mana_spent
    g_min_mana_spent = inf
    initial_enemy_hit, enemy_damage = parse_input(input_str)
    initial_shield_timer = 0
    initial_poison_timer = 0
    initial_recharge_timer = 0
    min_mana_spent = play(1,
                          initial_player_hit, initial_player_mana,
                          initial_shield_timer, initial_poison_timer, initial_recharge_timer,
                          initial_enemy_hit, enemy_damage,
                          hard=True)
    return min_mana_spent

def play(turn, player_hit, player_mana, shield_timer, poison_timer, recharge_timer, enemy_hit, enemy_damage, mana_spent=0, spells='', hard=False):
    print("[DBG] turn #%d,  SPENT: %d,  PLAYER: hit=%d mana=%d st=%d pt=%d rt=%d,  ENEMY: hit=%d damage=%d" % (
        turn, mana_spent, player_hit, player_mana, shield_timer, poison_timer, recharge_timer, enemy_hit, enemy_damage))
    global g_min_mana_spent
    for spell in SPELLS:
        next_mana_spent = mana_spent
        # 1. Player's turn
        # 1.1. Apply effect
        # 1.2. Cast spell
        # 2. Enemy's turn
        # 2.1. Apply effect
        # 2.2. Do damage to player
        print("-- Player turn --")
        print("- Player has %d hit points, %d armor, %d mana" % (player_hit, 0, player_mana))
        print("- Boss has %d hit points" % (enemy_hit))
        next_player_hit = player_hit
        next_enemy_hit = enemy_hit
        if hard:
            next_player_hit -= 1
        if next_player_hit > 0:
            next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit = apply_effect(
                    next_player_hit, 0, player_mana, shield_timer, poison_timer, recharge_timer, enemy_hit, enemy_damage)
        if next_player_hit > 0 and next_enemy_hit > 0:
            if COST[spell] > player_mana:
                print("[DBG] Cannot aford: %s --------------------------------------" % (spell))
                continue
            if (spell == S_Shield and shield_timer > 1) or (spell == S_Poison and poison_timer > 1) or (spell == S_Recharge and recharge_timer > 1):
                print("[DBG] Already active: %s ------------------------------------" % (spell))
                continue
            next_mana_spent += COST[spell]
            if next_mana_spent > g_min_mana_spent:
                print("[DBG] More expensive (%d) than the cheapest -----------------" % next_mana_spent)
                continue
            next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit = cast_spell(
                    next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit, enemy_damage, spell)
            print("[DBG] Spells: %s" % (spells + ' ' + spell))
            if next_player_hit > 0 and next_enemy_hit > 0:
                print("-- Boss turn --")
                print("- Player has %d hit points, %d armor, %d mana" % (next_player_hit, next_player_armor, next_player_mana))
                print("- Boss has %d hit points" % (next_enemy_hit))
                next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit = apply_effect(
                        next_player_hit, 0, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit, enemy_damage)
                if next_player_hit > 0 and next_enemy_hit > 0:
                    next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit = damage_player(
                            next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit, enemy_damage)
        if next_player_hit <= 0 or next_enemy_hit <= 0:
            # End of game
            if next_player_hit > 0:
                # Player wins
                total_mana_spent = next_mana_spent
                g_min_mana_spent = min(g_min_mana_spent, total_mana_spent)
                print("[DBG] !!!!!!!!!!!!!!!!!!!!!! Player wins (mana spent: %d) - min mana: %d - spells: %s" % (total_mana_spent, g_min_mana_spent, spells + ' ' + spell))
            elif next_enemy_hit > 0:
                print("[DBG] ?????????????????????? Enemy wins")
                # Enemy wins
                pass
            else:
                AssertionError
            # Next try
            continue
        else:
            # Next turn
            play(turn+1, next_player_hit, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit, enemy_damage, next_mana_spent, spells + ' ' + spell, hard)
            print("[DBG] turn #%d,  SPENT: %d,  PLAYER: hit=%d mana=%d st=%d pt=%d rt=%d,  ENEMY: hit=%d damage=%d" % (
                turn, mana_spent, player_hit, player_mana, shield_timer, poison_timer, recharge_timer, enemy_hit, enemy_damage))
    print("[DBG] <--- Go back")
    return g_min_mana_spent

def apply_effect(player_hit, player_armor, player_mana, shield_timer, poison_timer, recharge_timer, enemy_hit, enemy_damage):
    player_damage = 0
    delta_heal = 0
    delta_armor = 0
    delta_mana = 0
    shield_delta_timer = 0
    poison_delta_timer = 0
    recharge_delta_timer = 0
    if shield_timer > 0:
        player_damage += DAMAGE[S_Shield]
        delta_heal += HEAL[S_Shield]
        delta_armor += ARMOR[S_Shield]
        delta_mana += MANA[S_Shield]
        shield_delta_timer = 1
        print("Shield provides %d armor; its timer is now %d" % (delta_armor, shield_timer-1)) 
    if poison_timer > 0:
        player_damage += DAMAGE[S_Poison]
        delta_heal += HEAL[S_Poison]
        delta_armor += ARMOR[S_Poison]
        delta_mana += MANA[S_Poison]
        poison_delta_timer = 1
        print("Poison provides %d hit; its timer is now %d" % (player_damage, poison_timer-1)) 
    if recharge_timer > 0:
        player_damage += DAMAGE[S_Recharge]
        delta_heal += HEAL[S_Recharge]
        delta_armor += ARMOR[S_Recharge]
        delta_mana += MANA[S_Recharge]
        recharge_delta_timer = 1
        print("Recharge provides %d mana; its timer is now %d" % (delta_mana, recharge_timer-1)) 
    next_player_hit = player_hit + delta_heal
    next_player_armor = player_armor + delta_armor
    next_player_mana = player_mana + delta_mana
    next_shield_timer = shield_timer - shield_delta_timer
    next_poison_timer = poison_timer - poison_delta_timer
    next_recharge_timer = recharge_timer - recharge_delta_timer
    next_enemy_hit = enemy_hit - player_damage
    print("apply_effect - armor: %d -> %d" % (player_armor, next_player_armor))
    return next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit

def cast_spell(player_hit, player_armor, player_mana, shield_timer, poison_timer, recharge_timer, enemy_hit, enemy_damage, spell):
    print("Player casts %s" % spell)
    player_damage = 0
    delta_heal = 0
    delta_armor = 0
    delta_mana = 0
    if spell == S_Shield:
        assert(shield_timer == 0)
        shield_timer = EFFECT[S_Shield]
    elif spell == S_Poison:
        assert(poison_timer == 0)
        poison_timer = EFFECT[S_Poison]
    elif spell == S_Recharge:
        assert(recharge_timer == 0)
        recharge_timer = EFFECT[S_Recharge]
    else:
        player_damage = DAMAGE[spell]
        delta_heal = HEAL[spell]
        delta_armor = ARMOR[spell]
        delta_mana = MANA[spell]
    next_player_hit = player_hit + delta_heal
    next_player_armor = player_armor
    if shield_timer == 0:
        next_player_armor = 0
    next_player_mana = player_mana + delta_mana - COST[spell]
    next_shield_timer = shield_timer
    next_poison_timer = poison_timer
    next_recharge_timer = recharge_timer
    next_enemy_hit = enemy_hit - player_damage
    print("cast_spell - armor: %d -> %d" % (player_armor, next_player_armor))
    return next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit

def damage_player(player_hit, player_armor, player_mana, shield_timer, poison_timer, recharge_timer, enemy_hit, enemy_damage):
    effective_damage = max(1, enemy_damage - player_armor)
    next_player_hit = player_hit - effective_damage
    next_player_armor = player_armor
    next_player_mana = player_mana
    next_shield_timer = shield_timer
    next_poison_timer = poison_timer
    next_recharge_timer = recharge_timer
    next_enemy_hit = enemy_hit
    print("Boss atacks for %d - %d = %d damage!" % (enemy_damage, player_armor, effective_damage))
    print("damage_player - armor: %d -> %d" % (player_armor, next_player_armor))
    return next_player_hit, next_player_armor, next_player_mana, next_shield_timer, next_poison_timer, next_recharge_timer, next_enemy_hit

def parse_input(input_str):
    hit_line, damage_line = input_str.strip().split('\n')
    hit = int(hit_line.split(': ')[1])
    damage = int(damage_line.split(': ')[1])
    return hit, damage

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
""", None),
                ]
        self.tc_2 = [
                (
"""
""", None),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
