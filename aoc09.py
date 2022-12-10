########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

import itertools
from math import inf

_dist = None
_nodes = None

def solve_1(input_str):
    parse_input(input_str)
    d = compute_shortest_dist()
    return d

def solve_2(input_str):
    parse_input(input_str)
    d = compute_longest_dist()
    return d


def parse_input(input_str):
    global _dist
    global _nodes
    _dist = dict()
    _nodes = set()
    for line in input_str.strip().split('\n'):
        locations, distance = [x.strip() for x in line.split('=')]
        l1, l2 = [l.strip() for l in locations.split('to')]
        d = int(distance)
        _dist[(l1, l2)] = d
        _dist[(l2, l1)] = d
        _nodes.add(l1)
        _nodes.add(l2)

def compute_shortest_dist():
    routes = list()
    perms = list(itertools.permutations(_nodes))
    for p in perms:
        if is_valid_route(p):
            routes.append(p)
    min_d = +inf
    print(len(perms), len(routes))
    for route in routes:
        d = compute_route_dist(route)
        if d < min_d:
            min_d = d
    return min_d

def is_valid_route(route):
    valid = True
    prev_node = route[0]
    for node in route[1:]:
        valid = valid and ((prev_node, node) in _dist)
        prev_node = node
    return valid

def compute_route_dist(route):
    d = 0
    node_1 = route[0]
    for i in range(1, len(route)):
        node_1 = route[i-1]
        node_2 = route[i]
        d += _dist[(node_1, node_2)]
    return d

def compute_longest_dist():
    routes = list()
    perms = list(itertools.permutations(_nodes))
    for p in perms:
        if is_valid_route(p):
            routes.append(p)
    max_d = -inf
    print(len(perms), len(routes))
    for route in routes:
        d = compute_route_dist(route)
        if d > max_d:
            max_d = d
    return max_d

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""".strip(), 605),
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
