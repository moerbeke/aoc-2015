########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

P = namedtuple('P', ['x', 'y'])

ON = '#'
OFF = '.'

def solve_1(input_str, n_steps=100):
    grid = parse_input(input_str)
    grid.run_steps(n_steps)
    return grid.n_lights_on

def solve_2(input_str, n_steps=100):
    grid = parse_input(input_str, stuck_corners=True)
    grid.run_steps(n_steps)
    return grid.n_lights_on

def parse_input(input_str, stuck_corners=False):
    state = list()
    for line in input_str.split():
        state.append(list(line))
    return Grid(state, stuck_corners)

class Grid:

    def __init__(self, initial_state, stuck_corners):
        self._Y = len(initial_state)
        self._X = len(initial_state[0])
        self._state = dict()
        for x in range(self._X):
            for y in range(self._Y):
                p = P(x,y)
                self._state[P(x,y)] = initial_state[y][x]
        self._stuck_corners = stuck_corners
        if self._stuck_corners:
            self._corners = [P(0,0), P(self._X-1,0), P(0,self._Y-1), P(self._X-1,self._Y-1)]
            for p in self._corners:
                self._state[p] = ON

    @property
    def n_lights_on(self):
        return len([p for p in self._state if self._state[p] == ON])

    def print(self):
        printable = ""
        for y in range(self._Y):
            for x in range(self._X):
                printable += self._state[P(x,y)]
            printable += "\n"
        print(printable)

    def run_steps(self, n):
        #self.print()
        for i in range(n):
            self.run_step()
            #self.print()

    def run_step(self):
        prev_state = self._state
        self._state = {}
        for p in prev_state:
            if self._stuck_corners and p in self._corners:
                self._state[p] = ON
            else:
                self._state[p] = self._next_light_state(p, prev_state)

    def _next_light_state(self, p, state):
        p_light_state = state[p]
        n_neighbours_on = self._count_neighbours_on(p, state)
        if p_light_state == ON:
            if 2 <= n_neighbours_on <= 3:
                next_state = ON
            else:
                next_state = OFF
        else:
            if n_neighbours_on == 3:
                next_state = ON
            else:
                next_state = OFF
        return next_state

    def _count_neighbours_on(self, p, state):
        count = 0
        for x in range(max(0, p.x-1), min(self._X-1, p.x+1)+1):
            for y in range(max(0, p.y-1), min(self._Y-1, p.y+1)+1):
                if P(x,y) == p:
                    continue
                if state[P(x,y)] == ON:
                    count += 1
        return count

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""", 4, 4),
                ]
        self.tc_2 = [
                (
"""
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""", 17, 5),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0], t[2]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0], t[2]), t[1])
