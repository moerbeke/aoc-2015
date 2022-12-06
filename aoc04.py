########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

import hashlib

def solve_1(input_str):
    return find_match(input_str.strip(), '00000')

def solve_2(input_str):
    return find_match(input_str.strip(), '000000')

def find_match(key, pattern):
    n = 0
    pl = len(pattern)
    while True:
        x = key + str(n)
        if hash(x)[:pl] == pattern:
            break
        n += 1
    return n

def hash(x):
    return hashlib.md5(x.encode()).hexdigest()

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                ("abcdef", 609043),
                ("pqrstuv", 1048970),
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
