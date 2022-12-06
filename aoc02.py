########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

import copy

def solve_1(input_str):
    parse_input(input_str)
    paper = 0
    for box in boxes:
        paper += compute_box_paper(box[0], box[1], box[2])
    return paper

def solve_2(input_str):
    parse_input(input_str)
    ribbon = 0
    for box in boxes:
        ribbon += compute_box_ribbon(box[0], box[1], box[2])
    return ribbon

def parse_input(input_str):
    global boxes
    boxes = list()
    for line in input_str.split():
        boxes.append([int(a) for a in line.split('x')])

def compute_box_paper(l, w, h):
    paper = 2*l*w + 2*w*h + 2*h*l + min(l*w, l*h, w*h)
    return paper

def compute_box_ribbon(l, w, h):
    ribbon = min(2*l+2*w, 2*l+2*h, 2*w+2*h) + l*w*h
    return ribbon

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
2x3x4
1x1x10
""", 58+43),
                ]
        self.tc_2 = [
                (
"""
2x3x4
1x1x10
""", 34+14),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])

    def test_box_paper(self):
        self.assertEqual(compute_box_paper(2, 3, 4), 58)
        self.assertEqual(compute_box_paper(1, 1, 10), 43)

    def test_box_ribbon(self):
        self.assertEqual(compute_box_ribbon(2, 3, 4), 34)
        self.assertEqual(compute_box_ribbon(1, 1, 10), 14)

