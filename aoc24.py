########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from itertools import combinations as comb
from math import inf, prod

def solve_1(input_str):
    pkgs = parse_input(input_str)
    qe = arrange3(pkgs)
    return qe

def solve_2(input_str):
    pkgs = parse_input(input_str)
    qe = arrange4(pkgs)
    return qe

def parse_input(input_str):
    pkgs = [int(pkg) for pkg in input_str.strip().split('\n')]
    return pkgs

def arrange3(pkgs):
    total_weight = sum(pkgs)
    group_weight = total_weight // 3
    assert(group_weight * 3 == total_weight)
    min_qe = inf
    for n in range(1, len(pkgs)-1):
        for g1 in comb(pkgs, n):
            if sum(g1) != group_weight:
                continue
            if prod(g1) > min_qe:
                continue
            pkgs_not_in_g1 = set(pkgs) - set(g1)
            for m in range(1, len(pkgs_not_in_g1)):
                for g2 in comb(pkgs_not_in_g1, m):
                    if sum(g2) != group_weight:
                        continue
                    g3 = set(pkgs_not_in_g1) - set(g2)
                    assert(sum(g3) == group_weight)
                    qe = prod(g1)
                    if qe < min_qe:
                        min_qe = qe
                    print(g1, g2, g3, qe, min_qe)
        if min_qe < inf:
            break
    return min_qe

def arrange4(pkgs):
    total_weight = sum(pkgs)
    group_weight = total_weight // 4
    assert(group_weight * 4 == total_weight)
    min_qe = inf
    for n in range(1, len(pkgs)-2):
        for g1 in comb(pkgs, n):
            if sum(g1) != group_weight:
                continue
            if prod(g1) > min_qe:
                continue
            pkgs_not_in_g1 = set(pkgs) - set(g1)
            for m in range(1, len(pkgs_not_in_g1)-1):
                for g2 in comb(pkgs_not_in_g1, m):
                    if sum(g2) != group_weight:
                        continue
                    pkgs_not_in_g1_g2 = set(pkgs_not_in_g1) - set(g2)
                    for l in range(1, len(pkgs_not_in_g1_g2)):
                        for g3 in comb(pkgs_not_in_g1_g2, l):
                            if sum(g3) != group_weight:
                                continue
                            g4 = set(pkgs_not_in_g1_g2) - set(g3)
                    assert(sum(g4) == group_weight)
                    qe = prod(g1)
                    if qe < min_qe:
                        min_qe = qe
                    print(g1, g2, g3, g4, qe, min_qe)
        if min_qe < inf:
            break
    return min_qe

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
1
2
3
4
5
7
8
9
10
11
""", 99),
                ]
        self.tc_2 = [
                (
"""
1
2
3
4
5
7
8
9
10
11
""", 44),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
