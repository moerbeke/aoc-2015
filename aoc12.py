########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

import json

def solve_1(input_str):
    book = json.loads(input_str.strip())
    return sum_numbers(book)
    return None

def solve_2(input_str):
    book = json.loads(input_str)
    return sum_numbers(book, True)

def parse_input(input_str):
    pass

def sum_numbers(b, rm_red=False):
    if type(b) == int:
        return b
    elif type(b) == str:
        return 0
    elif type(b) == list:
        return sum([sum_numbers(i, rm_red) for i in b])
    elif type(b) == dict:
        s = 0
        if (not rm_red) or (not "red" in b.values()):
            for k in b:
                assert((type(k) == str))
                s += sum_numbers(b[k], rm_red)
        return s


########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                ('[1,2,3]', 6),
                ('{"a":2,"b":4}', 6),
                ('[[[3]]]', 3),
                ('{"a":{"b":4},"c":-1}', 3),
                ('{"a":[-1,1]}', 0),
                ('[-1,{"a":1}]', 0),
                ('[]', 0),
                ('{}', 0),
                ]
        self.tc_2 = [
                ('[1,2,3]', 6),
                ('[1,{"c":"red","b":2},3]', 4),
                ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
                ('[1,"red",5]', 6),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
