########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

Stmt = namedtuple('Stmt', ['instr', 'arg1', 'arg2'])

def solve_1(input_str):
    prog = parse_input(input_str)
    a, b = run(prog, 0)
    return b

def solve_2(input_str):
    prog = parse_input(input_str)
    a, b = run(prog, 1)
    return b

def parse_input(input_str):
    program = []
    for line in input_str.strip().split('\n'):
        instr = line[0:3]
        args = line[4:].split(',')
        arg1 = args[0]
        if instr == 'jmp':
            arg1 = int(arg1)
        try:
            arg2 = int(args[1])
        except IndexError:
            arg2 = None
        program.append(Stmt(instr, arg1, arg2))
    return program

def run(prog, a):
    b = 0
    ptr = 0
    while 0 <= ptr < len(prog):
        a, b, ptr = run_stmt(prog, a, b, ptr)
    return a, b

def run_stmt(prog, a, b, ptr):
    stmt = prog[ptr]
    if stmt.instr == 'hlf':
        if stmt.arg1 == 'a':
            a /= 2
        elif stmt.arg1 == 'b':
            b /= 2
        else:
            assert(False)
        ptr += 1
    elif stmt.instr == 'tpl':
        if stmt.arg1 == 'a':
            a *= 3
        elif stmt.arg1 == 'b':
            b *= 3
        else:
            assert(False)
        ptr += 1
    elif stmt.instr == 'inc':
        if stmt.arg1 == 'a':
            a += 1
        elif stmt.arg1 == 'b':
            b += 1
        else:
            assert(False)
        ptr += 1
    elif stmt.instr == 'jmp':
        ptr += stmt.arg1
    elif stmt.instr == 'jie':
        if (stmt.arg1 == 'a' and a % 2 == 0) or (stmt.arg1 == 'b' and b % 2 == 0):
            ptr += stmt.arg2
        else:
            ptr += 1
    elif stmt.instr == 'jio':
        if (stmt.arg1 == 'a' and a == 1) or (stmt.arg1 == 'b' and b == 1):
            ptr += stmt.arg2
        else:
            ptr += 1
    else:
        assert(False)
    return a, b, ptr

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
inc a
jio a, +2
tpl a
inc a
""", 0),
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
