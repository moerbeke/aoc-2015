########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    return count_nice_strings(input_str.split())

def solve_2(input_str):
    return count_nicer_strings(input_str.split())

def count_nice_strings(str_list):
    n = 0
    for s in str_list:
        if is_nice(s):
            n += 1
    return n

def is_nice(s):
    nice = (
            contains_three_vowels(s) and
            contains_double_letter(s) and
            does_not_contain_disallowed_str(s))
    return nice

def contains_three_vowels(s):
    n_vowels = 0
    i = 0
    while n_vowels < 3 and i < len(s):
        if s[i] in ['a', 'e', 'i', 'o', 'u']:
            n_vowels += 1
        i += 1
    return n_vowels >= 3

def contains_double_letter(s):
    double_letter = False
    prev_letter = None
    i = 0
    while not double_letter and i < len(s):
        c = s[i]
        if c == prev_letter:
            double_letter = True
        prev_letter = c
        i += 1
    return double_letter

def does_not_contain_disallowed_str(s):
    allowed = True
    disallowed_str = ['ab', 'cd', 'pq', 'xy']
    for d in disallowed_str:
        if d in s:
            allowed = False
            break
    return allowed


def count_nicer_strings(str_list):
    n = 0
    for s in str_list:
        if is_nicer(s):
            n += 1
    return n

def is_nicer(s):
    nicer = (
            contains_double_pair(s) and
            contains_symetric_letter(s))
    return nicer

def contains_double_pair(s):
    """
    It contains a pair of any two letters that appears at least twice 
    in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa),
    but not like aaa (aa, but it overlaps).
    """
    double_pair = 0
    i = 0
    while i <= len(s) - 4:
        j = i + 2
        ts = s[i:j]
        if ts in s[j:]:
            double_pair += 1
        i += 1
    return double_pair >= 1

def contains_symetric_letter(s):
    """
    It contains at least one letter which repeats with exactly 
    one letter between them, like xyx, abcdefeghi (efe), or even aaa.
    """
    symetric_letter = False
    i = 2
    while i < len(s) and s[i] != s[i-2]:
        i += 1
    return i < len(s)

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
""", 2),
                ]
        self.tc_2 = [
                (
"""
qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy
""", 2),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])

    def test_is_nice(self):
        self.assertTrue(is_nice('ugknbfddgicrmopn'))
        self.assertTrue(is_nice('aaa'))
        self.assertFalse(is_nice('jchzalrnumimnmhp'))
        self.assertFalse(is_nice('haegwjzuvuyypxyu'))
        self.assertFalse(is_nice('dvszwmarrgswjxmb'))

    def test_contains_double_pair(self):
        self.assertTrue(contains_double_pair('xyxy'))
        self.assertTrue(contains_double_pair('aabcdefgaa'))
        self.assertFalse(contains_double_pair('aaa'))

    def test_contains_symetric_letter(self):
        self.assertTrue(contains_symetric_letter('abcdefeghi'))

    def test_is_nicer(self):
        self.assertTrue(is_nicer('qjhvhtzxzqqjkmpb'))
        self.assertTrue(is_nicer('xxyxx'))
        self.assertFalse(is_nicer('uurcxstgmygtbstg'))
        self.assertFalse(is_nicer('ieodomkazucvgmuy'))
