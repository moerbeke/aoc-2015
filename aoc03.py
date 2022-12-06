########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    x = 0
    y = 0
    visits = set()
    visits.add((x, y))
    for c in input_str.strip():
        x, y = move(x, y, c)
        visits.add((x, y))
    return len(visits)

def solve_2(input_str):
    santa_x = 0
    santa_y = 0
    robo_santa_x = 0
    robo_santa_y = 0
    santa_visits = set()
    santa_visits.add((santa_x, santa_y))
    robo_santa_visits = set()
    robo_santa_visits.add((robo_santa_x, robo_santa_y))
    i = 0
    path = input_str.strip()
    while i < len(path):
        santa_x, santa_y = move(santa_x, santa_y, path[i])
        santa_visits.add((santa_x, santa_y))
        i += 1
        if i < len(path):
            robo_santa_x, robo_santa_y = move(robo_santa_x, robo_santa_y, path[i])
            robo_santa_visits.add((robo_santa_x, robo_santa_y))
            i += 1
    return len(santa_visits.union(robo_santa_visits))

def move(from_x, from_y, towards):
    if towards == '^':
        x = from_x
        y = from_y + 1
    elif towards == 'v':
        x = from_x
        y = from_y - 1
    elif towards == '>':
        x = from_x + 1
        y = from_y
    elif towards == '<':
        x = from_x - 1
        y = from_y
    return x, y

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (">", 2),
                ("^>v<", 4),
                ("^v^v^v^v^v", 2),
                ]
        self.tc_2 = [
                ("^>", 3),
                ("^>v<", 3),
                ("^v^v^v^v^v", 11),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
