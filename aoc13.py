########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from itertools import permutations

def solve_1(input_str):
    people = parse_input(input_str)
    return compute_optimal_happiness(people)

def solve_2(input_str):
    people = parse_input(input_str)
    people.append(Person('Willen van Moerbeke'))
    return compute_optimal_happiness(people)

def parse_input(input_str):
    '''
    Line sample:
    0     1     2    3  4         5     6  7       8    9  10
    Alice would gain 54 happiness units by sitting next to Bob.
    '''
    people = dict()
    for line in input_str.strip().split('\n'):
        words = line.split()
        subject = words[0]
        feeling_type = words[2]
        amount = int(words[3])
        the_other = words[10].split('.')[0]
        if not subject in people:
            people[subject] = Person(subject)
        people[subject].add_feeling(feeling_type, amount, the_other)
        if not the_other in people:
            people[the_other] = Person(the_other)
    return list(people.values())

def compute_optimal_happiness(people):
    max_happiness = 0
    for table in generate_tables(people):
        max_happiness = max(max_happiness, table.get_happiness())
    return max_happiness

def generate_tables(people):
    n = len(people)
    tables = list()
    for arrangement in permutations(people):
        tables.append(Table(arrangement))
    return tables

class Person:

    def __init__(self, name):
        self.name = name
        self.feeling = dict()

    def add_feeling(self, feeling_type, amount, name):
        if feeling_type == 'gain':
            self.feeling[name] = amount
        elif feeling_type == 'lose':
            self.feeling[name] = -amount
        else:
            assert(False)

    def get_feeling(self, name):
        try:
            f = self.feeling[name]
        except KeyError:
            f = 0
        return f

class Table:

    def __init__(self, seats):
        self.seats = seats
        self.n = len(seats)

    def get_happiness(self):
        return sum([self.seats[i].get_feeling(self.seats[i-1].name) + self.seats[i].get_feeling(self.seats[(i+1)%self.n].name) for i in range(self.n)])

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
""", 330),
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

    @unittest.skip('no test cases')
    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
