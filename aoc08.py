########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def parse_input(input_str):
    global _string_codes
    _string_codes = input_str.strip().split('\n')

def solve_1(input_str):
    parse_input(input_str)
    strings = [load_str(scode) for scode in _string_codes]
    return len(''.join(_string_codes)) - len(''.join(strings))

def solve_2(input_str):
    parse_input(input_str)
    strings = [encode_str(scode) for scode in _string_codes]
    return len(''.join(strings)) - len(''.join(_string_codes))

def load_str(scode):
    s = ''
    i = 0
    c = scode[i]
    assert(c == '"')
    i += 1
    while i < len(scode) - 1:
        c = scode[i]
        if c == '\\':
            i += 1
            c = scode[i]
            if c == '\\' or c == '"':
                s += c
            elif c == 'x':
                ascii_hex = scode[i+1:i+3]
                i += 2
                s += chr(int(ascii_hex, 16))
            else:
                assert(False)
        else:
            s += c
        i += 1
    c = scode[i]
    assert(c == '"')
    return s

def encode_str(scode):
    s = '"'
    i = 0
    while i < len(scode):
        c = scode[i]
        if c == '"':
            s += '\\"'
        elif c == '\\':
            s += '\\\\'
        else:
            s += c
        i += 1
    s += '"'
    return s

########################################################################
# Tests
########################################################################

import unittest
import os

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
""
"abc"
"aaa\\"aaa"
"\\x27"
""".strip(), 12),
                ]
        self.tc_2 = [
                (
"""
""
"abc"
"aaa\\"aaa"
"\\x27"
""".strip(), 19),
                ]
        self._test_filename = '8.in.test'
        with open(self._test_filename, 'w') as f:
            f.write(self.tc_1[0][0])

    def tearDown(self):
        os.remove(self._test_filename)

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])

    def test_solve_1_file(self):
        self.assertEqual(solve_1(self.tc_1[0][0]), self.tc_1[0][1])
