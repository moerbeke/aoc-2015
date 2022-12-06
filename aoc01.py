########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    return input_str.count('(') - input_str.count(')')

def solve_2(input_str):
    floor = 0
    p = 0
    while floor >= 0:
        c = input_str[p]
        if c == '(':
            floor += 1
        else:
            floor -= 1
        p += 1
    return p

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                ("(())", 0),
                ("()()", 0),
                ("(((", 3),
                ("(()(()(", 3),
                ("))(((((", 3),
                ("())", -1),
                ("))(", -1),
                (")))", -3),
                (")())())", -3),
                ]
        self.tc_2 = [
                (')', 1),
                ('()())', 5),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
