########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

_chars = [chr(i) for i in range(ord('a'), ord('z')+1)]
_charslen = len(_chars)
_invalid_letters = ['i', 'o', 'l']

_part1 = None

def solve_1(input_str):
    global _part1
    _part1 = next_passwd(input_str.strip())
    return _part1

def solve_2(input_str):
    global _part1
    if _part1 is None:
        _part1 = next_passwd(input_str.strip())
    return next_passwd(_part1)

def parse_input(input_str):
    pass

def incr(c):
    if c < 'a' or c > 'z':
        raise ValueError
    nextindex = (ord(c) - ord('a') + 1) % _charslen
    if isinvalid_letter(_chars[nextindex]):
        c = _chars[nextindex]
        nextindex = (ord(c) - ord('a') + 1) % _charslen
        nextindex = (_chars.index(c) + 1) % _charslen
    return _chars[nextindex]

def isinvalid_letter(c):
    return c in _invalid_letters

def nextstr(s):
    l = len(s)
    sl = list(s)
    invalid_letter = False
    for i in range(l):
        c = sl[i]
        if isinvalid_letter(c):
            invalid_letter = True
            sl[i] = incr(sl[i])
            for j in range(i+1, l):
                sl[j] = 'a'
    if invalid_letter:
        nslist = list(reversed(sl))
    else:
        nslist = list(reversed([s[i] for i in range(l)]))
        for i in range(l):
            c = nslist[i]
            nc = incr(c)
            nslist[i] = nc
            if nc != 'a':
                break
    return ''.join(list(reversed(nslist)))

def isvalid_passwd(passwd):
    return (includes_validletters(passwd) and
            includes_straight(passwd) and 
            includes_twopairs(passwd))

def includes_validletters(passwd):
    for c in passwd:
        if isinvalid_letter(c):
            return False
    return True

def includes_straight(passwd):
    for i in range(len(passwd)-2):
        if ord(passwd[i+1]) == ord(passwd[i]) + 1 and ord(passwd[i+2]) == ord(passwd[i+1]) + 1 :
            return True
    return False

def includes_twopairs(passwd):
    for i in range(len(passwd)-3):
        pair1_index, pair1 = index_pair(passwd)
        if pair1_index >= 0:
            j = i + 2
            while j < len(passwd)-1:
                pair2_index, pair2 = index_pair(passwd[j:])
                if pair2_index >= 0 and pair1 != pair2:
                    return True
                j += 1
    return False

def index_pair(s):
    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            return i, s[i:i+2]
    return -1, None

def next_passwd(passwd):
    while True:
        passwd = nextstr(passwd)
        #print(passwd)
        if isvalid_passwd(passwd):
            break
    return passwd

########################################################################

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                ("abcdefgh", 'abcdffaa'),
                ("ghijklmn", 'ghjaabcc'),
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

    def test_incr(self):
        t = {
                'a': 'b',
                'h': 'j',
                'i': 'j',
                'b': 'c',
                'y': 'z',
                'z': 'a'}
        for x in t:
            self.assertEqual(incr(x), t[x])
        with self.assertRaises(ValueError):
            incr('1')

    def test_nextstr(self):
        t = {
                'a': 'b',
                'aa': 'ab',
                'az': 'ba',
                'zz': 'aa',
                'azb': 'azc',
                'abz': 'aca',
                'zbz': 'zca',
                'bzz': 'caa',
                'zzy': 'zzz',
                'zzz': 'aaa',
                'ghijklmn': 'ghjaaaaa',
                }
        for x in t:
            self.assertEqual(nextstr(x), t[x])

    def test_includes_validletters(self):
        self.assertFalse(includes_validletters('hijklmmn'))
        self.assertTrue(includes_validletters('abbceffg'))
        self.assertTrue(includes_validletters('abbcegjk'))
        self.assertTrue(includes_validletters('abcdffaa'))
        self.assertTrue(includes_validletters('ghjaabcc'))

    def test_includes_straight(self):
        self.assertTrue(includes_straight('hijklmmn'))
        self.assertFalse(includes_straight('abbceffg'))
        self.assertFalse(includes_straight('abbcegjk'))
        self.assertTrue(includes_straight('abcdffaa'))
        self.assertTrue(includes_straight('ghjaabcc'))

    def test_includes_twopairs(self):
        self.assertFalse(includes_twopairs('hijklmmn'))
        self.assertTrue(includes_twopairs('abbceffg'))
        self.assertFalse(includes_twopairs('abbcegjk'))
        self.assertTrue(includes_twopairs('abcdffaa'))
        self.assertTrue(includes_twopairs('ghjaabcc'))

    def test_isvalid_passwd(self):
        self.assertFalse(isvalid_passwd('hijklmmn'))
        self.assertFalse(isvalid_passwd('abbceffg'))
        self.assertFalse(isvalid_passwd('abbcegjk'))
        self.assertTrue(isvalid_passwd('abcdffaa'))
        self.assertTrue(isvalid_passwd('ghjaabcc'))
