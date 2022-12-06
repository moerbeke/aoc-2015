########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

TURN_OFF = 'turn off'
TURN_ON = 'turn on'
TOGGLE = 'toggle'

TURN_OFF_OP = 0
TURN_ON_OP = 1
TOGGLE_OP = 2

P = namedtuple('P', ['x', 'y'])

Ins = namedtuple('Ins', ['op', 'p1', 'p2'])

LEN = 1000

op = {
        TURN_OFF_OP: lambda l: 0,
        TURN_ON_OP: lambda l: 1,
        TOGGLE_OP: lambda l: 1 - l
        }

op_b = {
        TURN_OFF_OP: lambda l: max(0, l - 1),
        TURN_ON_OP: lambda l: l + 1,
        TOGGLE_OP: lambda l: l + 2
        }

_program = None
_lights = None

def solve_1(input_str):
    parse_input(input_str)
    run_program()
    return count_lights_lit()

def solve_2(input_str):
    parse_input(input_str)
    run_program_b()
    return count_lights_lit()

def parse_input(input_str):
    global _program
    instructions = input_str.strip().split('\n')
    _program = list()
    for i in instructions:
        _program.append(parse_ins(i))

def parse_ins(i):
    turn_off_len = len(TURN_OFF)
    turn_on_len = len(TURN_ON)
    toggle_len = len(TOGGLE)
    if TURN_OFF in i:
        op = TURN_OFF_OP
        p1_str, p2_str = [p.strip() for p in i[turn_off_len:].split('through')]
    elif TURN_ON in i:
        op = TURN_ON_OP
        p1_str, p2_str = [p.strip() for p in i[turn_on_len:].split('through')]
    elif TOGGLE in i:
        op = TOGGLE_OP
        p1_str, p2_str = [p.strip() for p in i[toggle_len:].split('through')]
    else:
        raise ValueError("Unknown instruction: %s" % i)
    p1_x, p1_y = [int(e.strip()) for e in p1_str.split(',')]
    p2_x, p2_y = [int(e.strip()) for e in p2_str.split(',')]
    return Ins(op, P(p1_x, p1_y), P(p2_x, p2_y))

def run_program():
    global _lights
    _lights = [0] * LEN*LEN
    for ins in _program:
        run_ins(ins)

def run_ins(ins):
    for i in range(ins.p1.x, ins.p2.x+1):
        for j in range(ins.p1.y, ins.p2.y+1):
            _lights[i*LEN + j] = op[ins.op](_lights[i*LEN + j])

def count_lights_lit():
    return sum(_lights)

def run_program_b():
    global _lights
    _lights = [0] * LEN*LEN
    for ins in _program:
        run_ins_b(ins)

def run_ins_b(ins):
    for i in range(ins.p1.x, ins.p2.x+1):
        for j in range(ins.p1.y, ins.p2.y+1):
            _lights[i*LEN + j] = op_b[ins.op](_lights[i*LEN + j])

########################################################################
# main
########################################################################

if __name__ == '__main__':
    aocbase.run(Aoc6)
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
