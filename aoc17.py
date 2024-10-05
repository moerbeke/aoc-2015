########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from itertools import combinations as comb

def solve_1(input_str, liters=150):
    p = parse_input(input_str)
    n = len(p)
    indexes = [i for i in range(n)]
    count = 0
    for i in range(1,n):
        for c in comb(indexes,i):
            l = [p[i] for i in c]
            sl = sum(l)
            if sl == liters:
                count += 1
    return count

def solve_2(input_str, liters=150):
    p = parse_input(input_str)
    n = len(p)
    indexes = [i for i in range(n)]
    count = 0
    for i in range(1,n):
        for c in comb(indexes,i):
            l = [p[i] for i in c]
            sl = sum(l)
            if sl == liters:
                count += 1
        if count > 0:
            break
    return count

def parse_input(input_str):
    return [int(c) for c in input_str.split()]

########################################################################
# Tests
    return None

def parse_input(input_str):
    return [int(c) for c in input_str.split()]

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
20
15
10
5
5
""", 4, 25),
                ]
        self.tc_2 = [
                (
"""
20
15
10
5
5
""", 3, 25),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0], t[2]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0], t[2]), t[1])
