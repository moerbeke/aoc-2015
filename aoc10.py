########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    parse_input(input_str)
    s = _first
    for i in range(40):
        s = successor(s)
    return len(s)

def solve_2(input_str):
    parse_input(input_str)
    s = _first
    for i in range(50):
        s = successor(s)
    return len(s)

def parse_input(input_str):
    global _first
    _first = input_str.strip()

def successor(element):
    s = ''
    i = 0
    while i < len(element):
        c = element[i]
        n = 1
        while i+n < len(element) and element[i+n] == c:
            n += 1
        s += str(n) + c
        i += n
    return s

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

    def test_successor(self):
        self.assertEqual(successor('1'), '11')
        self.assertEqual(successor('11'), '21')
        self.assertEqual(successor('21'), '1211')
        self.assertEqual(successor('1211'), '111221')
        self.assertEqual(successor('111221'), '312211')
