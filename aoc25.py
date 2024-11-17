########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    return value_at((3010, 3019))

def solve_2(input_str):
    return None

def parse_input(input_str):
    pass

def value_at(cell):
    code = 20151125
    a = cell[0]
    b = cell[1]
    n = 1
    while True:
        for i in range(n):
            r = n - i
            c = 1 + i
            #print(r, c, code)
            if r == a and c == b:
                return code
            code = (code * 252533) % 33554393
        n += 1

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

    def test_value_at(self):
        vals = {
                (1,1): 20151125,
                (2,1): 31916031,
                (1,2): 18749137,
                (3,1): 16080970,
                (2,2): 21629792,
                (1,3): 17289845,
                (4,1): 24592653
                }
        for cell in vals:
            self.assertEqual(value_at(cell), vals[cell])
