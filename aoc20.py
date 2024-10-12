########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    n = parse_input(input_str) // 10
    print(n*10)
    i0 = n//2 + n%2
    for i in range(1, n+1):
        hi = compute_elves(i)
        print(i, hi*10)
        if hi >= n:
            return i
    assert(False)

def compute_elves(i):
    return sum(divisors(i))

def divisors(n):
    ds = [1]
    if n != 1:
        ds.extend([i for i in range(2,int(n**.5)+1) if n % i == 0])
        ds.extend([n//i for i in ds])
    ds = list(set(ds))
    return ds

def solve_2(input_str):
    return None

def parse_input(input_str):
    return int(input_str)

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (10, 1),
                (30, 2),
                (40, 3),
                (70, 4),
                (60, 4),
                (120, 6),
                (80, 6),
                (150, 8),
                (130, 8),
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
