########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

AND = 'AND'
OR = 'OR'
NOT = 'NOT'
LSHIFT = 'LSHIFT'
RSHIFT = 'RSHIFT'

MAX_SIGNAL = 1 << 16

indent = 0

_ins = None
_signal = None

def solve_1(input_str):
    parse_input(input_str)
    wire = 'a'
    compute_wire_signal(wire)
    return _signal[wire]

def solve_2(input_str):
    parse_input(input_str)
    wire = 'a'
    signal_a = compute_wire_signal(wire)
    for w in _signal:
        _signal[w] = None
    _signal['b'] = signal_a
    compute_wire_signal(wire)
    return _signal[wire]


def parse_input(input_str):
    global _ins
    global _signal
    _ins = dict()
    _signal = dict()
    for line in input_str.strip().split('\n'):
        ins, wire = [e.strip() for e in line.split('->')]
        _ins[wire] = ins
        _signal[wire] = None

def compute_wire_signal(w):
    #global indent
    #print("%scompute_wire_signal: %s" % (' '*indent, w))
    #indent += 1
    ins = _ins[w]
    s = _signal[w]
    if s is not None:
        # Already computed
        assert(isinstance(s, int))
    elif is_signal(ins):
        # Input: signal
        s = int(ins)
    elif is_wire(ins):
        # Input: wire
        s = _signal[ins]
        if s is None:
            s = compute_wire_signal(ins)
    elif is_gate(AND, ins):
        # Input: AND gate
        w1, w2 = [w.strip() for w in ins.split(AND)]
        s1 = get_signal(w1)
        s2 = get_signal(w2)
        if s1 is None:
            s1 = compute_wire_signal(w1)
        if s2 is None:
            s2 = compute_wire_signal(w2)
        s = s1 & s2
    elif is_gate(OR, ins):
        # Input: OR gate
        w1, w2 = [w.strip() for w in ins.split(OR)]
        s1 = get_signal(w1)
        s2 = get_signal(w2)
        if s1 is None:
            s1 = compute_wire_signal(w1)
        if s2 is None:
            s2 = compute_wire_signal(w2)
        s = s1 | s2
    elif is_gate(NOT, ins):
        # Input: NOT gate
        *w0, w1 = [w.strip() for w in ins.split(NOT)]
        s1 = get_signal(w1)
        if s1 is None:
            s1 = compute_wire_signal(w1)
        s = MAX_SIGNAL - 1 - s1
    elif is_gate(LSHIFT, ins):
        # Input: LSHIFT gate
        w1, w2 = [w.strip() for w in ins.split(LSHIFT)]
        s1 = get_signal(w1)
        s2 = get_signal(w2)
        if s1 is None:
            s1 = compute_wire_signal(w1)
        if s2 is None:
            s2 = compute_wire_signal(w2)
        s = (s1 << int(s2)) & (MAX_SIGNAL - 1)
    elif is_gate(RSHIFT, ins):
        # Input: RSHIFT gate
        w1, w2 = [w.strip() for w in ins.split(RSHIFT)]
        s1 = get_signal(w1)
        s2 = get_signal(w2)
        if s1 is None:
            s1 = compute_wire_signal(w1)
        if s2 is None:
            s2 = compute_wire_signal(w2)
        s = s1 >> int(s2)
    _signal[w] = s
    #print("%s%d" % (' '*indent, s))
    #indent -= 1
    return s

def is_signal(ins):
    return ins.isdecimal()

def is_wire(ins):
    return ins in _signal

def is_gate(gate, ins):
    return gate in ins

def get_signal(w):
    if is_signal(w):
        s = int(w)
    elif is_wire(w):
        s = _signal[w]
    else:
        assert(False)
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
