########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

good_old_sue = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1,
        }

def solve_1(input_str):
    aunts = parse_input(input_str)
    for i in aunts:
        if match_exact(aunts[i], good_old_sue):
            return i
    assert(False)

def solve_2(input_str):
    aunts = parse_input(input_str)
    for i in aunts:
        if match_range(aunts[i], good_old_sue):
            return i
    assert(False)

def parse_input(input_str):
    '''
    0   1  2         3  4      5  6       7
    Sue 1: goldfish: 6, trees: 9, akitas: 0
    '''
    aunts = dict()
    for line in input_str.strip().split('\n'):
        words = line.split(' ')
        sue = int(words[1][:-1])
        aunts[sue] = dict()
        for i in range(len(words[2:])//2):
            compound = words[2+2*i].split(':')[0]
            assert(compound in good_old_sue.keys())
            n = int(words[2+2*i+1].split(',')[0])
            aunts[sue][compound] = n
    return aunts

def match_exact(aunt, amounts):
    sue_match = True
    for compound in aunt:
        if aunt[compound] != amounts[compound]:
            sue_match = False
            break
    return sue_match

def match_range(aunt, amounts):
    sue_match = True
    for compound in aunt:
        if compound in ['trees', 'cats']:
            if aunt[compound] <= amounts[compound]:
                sue_match = False
        elif compound in ['pomeranians', 'goldfish']:
            if aunt[compound] >= amounts[compound]:
                sue_match = False
        else:
            if aunt[compound] != amounts[compound]:
                sue_match = False
        if not sue_match:
            break
    return sue_match

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
