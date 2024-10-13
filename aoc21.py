########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from itertools import combinations
from math import inf

"""
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

# Weapons
W_Dagger     = 'WD'
W_Shortsword = 'WS'
W_Warhammer  = 'WW'
W_Longsword  = 'WL'
W_Greataxe   = 'WG'
WEAPONS = [
        W_Dagger,
        W_Shortsword,
        W_Warhammer,
        W_Longsword,
        W_Greataxe
        ]

# Armor
A_Leather    = 'AL'
A_Chainmail  = 'AC'
A_Splintmail = 'AS'
A_Bandedmail = 'AB'
A_Platemail  = 'AP'
ARMORS = [
        A_Leather,
        A_Chainmail,
        A_Splintmail,
        A_Bandedmail,
        A_Platemail
        ]

# Rings
R_Damage_1 = 'R1'
R_Damage_2 = 'R2'
R_Damage_3 = 'R3'
R_Defense_1 = 'r1'
R_Defense_2 = 'r2'
R_Defense_3 = 'r3'
RINGS = [
        R_Damage_1,
        R_Damage_2,
        R_Damage_3,
        R_Defense_1,
        R_Defense_2,
        R_Defense_3
        ]


COST = {
        # Weapons
        W_Dagger:      8,
        W_Shortsword: 10,
        W_Warhammer:  25,
        W_Longsword:  40,
        W_Greataxe:   74,

        # Armor,
        A_Leather:    13,
        A_Chainmail:  31,
        A_Splintmail: 53,
        A_Bandedmail: 75,
        A_Platemail: 102,

        # Rings
        R_Damage_1:  25,
        R_Damage_2:  50,
        R_Damage_3: 100,
        R_Defense_1: 20,
        R_Defense_2: 40,
        R_Defense_3: 80
        }

DAMAGE = {
        # Weapons
        W_Dagger:      4,
        W_Shortsword:  5,
        W_Warhammer:   6,
        W_Longsword:   7,
        W_Greataxe:    8,

        # Armor,
        A_Leather:     0,
        A_Chainmail:   0,
        A_Splintmail:  0,
        A_Bandedmail:  0,
        A_Platemail:   0,

        # Rings
        R_Damage_1:   1,
        R_Damage_2:   2,
        R_Damage_3:   3,
        R_Defense_1:  0,
        R_Defense_2:  0,
        R_Defense_3:  0
        }

ARMOR = {
        # Weapons
        W_Dagger:      0,
        W_Shortsword:  0,
        W_Warhammer:   0,
        W_Longsword:   0,
        W_Greataxe:    0,

        # Armor,
        A_Leather:     1,
        A_Chainmail:   2,
        A_Splintmail:  3,
        A_Bandedmail:  4,
        A_Platemail:   5,

        # Rings
        R_Damage_1:   0,
        R_Damage_2:   0,
        R_Damage_3:   0,
        R_Defense_1:  1,
        R_Defense_2:  2,
        R_Defense_3:  3
        }

min_gold_to_win = None
max_gold_to_lose = None

def solve_1(input_str):
    global min_gold_to_win, max_gold_to_lose
    if min_gold_to_win is None:
        min_gold_to_win, max_gold_to_lose = play(input_str)
    return min_gold_to_win

def solve_2(input_str):
    global min_gold_to_win, max_gold_to_lose
    if min_gold_to_win is None:
        min_gold_to_win, max_gold_to_lose = play(input_str)
    return max_gold_to_lose

def play(input_str):
    """Rules

    Buy:
    Number of weapons: 1
    Number of armor: 0 or 1
    Number of rings: 0, 1 or 2

    Damage = max(1, damage1-armor2)
    """
    enemy_hit, enemy_damage, enemy_armor = parse_input(input_str)
    player_hit = 100
    n_weapons = [1]
    n_armors = [0, 1]
    n_rings = [0, 1, 2]
    min_gold_to_win = inf
    max_gold_to_lose = -inf
    for nw in n_weapons:
        for weapons in combinations(WEAPONS, nw):
            for na in n_armors:
                for armors in combinations(ARMORS, na):
                    for nr in n_rings:
                        for rings in combinations(RINGS, nr):
                            gold = compute_gold(weapons, armors, rings)
                            if player_wins(player_hit, weapons, armors, rings, enemy_hit, enemy_damage, enemy_armor):
                                min_gold_to_win = min(min_gold_to_win, gold)
                            else:
                                max_gold_to_lose = max(max_gold_to_lose, gold)
    return min_gold_to_win, max_gold_to_lose

def compute_gold(weapons, armors, rings):
    gold = sum([COST[o] for o in weapons]) + sum([COST[o] for o in armors]) + sum([COST[o] for o in rings])
    return gold

def player_wins(player_hit, weapons, armors, rings, enemy_hit, enemy_damage, enemy_armor):
    while True:
        # Player turn
        damage = sum([DAMAGE[o] for o in weapons]) + sum([DAMAGE[o] for o in armors]) + sum([DAMAGE[o] for o in rings])
        damage -= enemy_armor
        enemy_hit -= max(1, damage)
        if enemy_hit <= 0:
            player_winner = True
            break
        # Enemy turn
        armor = sum([ARMOR[o] for o in weapons]) + sum([ARMOR[o] for o in armors]) + sum([ARMOR[o] for o in rings])
        damage = enemy_damage - armor
        player_hit -= max(1, damage)
        if player_hit <= 0:
            player_winner = False
            break
    return player_winner

def parse_input(input_str):
    hit_line, damage_line, armor_line = input_str.strip().split('\n')
    hit = int(hit_line.split(': ')[1])
    damage = int(damage_line.split(': ')[1])
    armor = int(armor_line.split(': ')[1])
    return hit, damage, armor

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                ]
        self.tc_2 = [
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
