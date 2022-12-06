########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

ReindeerProfile = namedtuple('ReindeerProfile', ['name', 'speed', 'fly_time', 'rest_time'])

def solve_1(input_str):
    return compute_winner_at(parse_input(input_str), 2503)

def solve_2(input_str):
    return compute_winner_by_points_at(parse_input(input_str), 2503)

def parse_input(input_str):
    '''
    Reindeer:
    0     1   2   3  4    5   6  7        8   9    10   11   12  13  14
    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    '''
    reindeer_profiles = list()
    for line in input_str.strip().split('\n'):
        words = line.split()
        name = words[0]
        speed = int(words[3])
        fly_time = int(words[6])
        rest_time = int(words[13])
        reindeer_profiles.append(ReindeerProfile(name, speed, fly_time, rest_time))
    return reindeer_profiles

def compute_winner_at(reindeer_profiles, seconds):
    max_distance = 0
    for r in reindeer_profiles:
        period = r.fly_time + r.rest_time
        last_start = seconds - (seconds % period)
        n_periods = seconds // period
        last_flying_interval = min(r.fly_time, seconds - last_start)
        flying_time = n_periods * r.fly_time + last_flying_interval
        distance = r.speed * flying_time
        max_distance = max(max_distance, distance)
    return max_distance

def compute_winner_by_points_at(reindeer_profiles, seconds):
    reindeers = dict()
    for r in reindeer_profiles:
        reindeers[r.name] = Reindeer(r)
    for t in range(1, seconds+1):
        current_distance = {}
        for name in reindeers:
            current_distance[name] = reindeers[name].distance_at(t)
        lead_distance = max(current_distance.values())
        for name in current_distance:
            if current_distance[name] == lead_distance:
                reindeers[name].add_point()
    max_points = 0
    for name in reindeers:
        max_points = max(max_points, reindeers[name].get_points())
    return max_points

class Reindeer:

    def __init__(self, reindeer_profile):
        self.name = reindeer_profile.name
        self.speed = reindeer_profile.speed
        self.fly_time = reindeer_profile.fly_time
        self.rest_time = reindeer_profile.rest_time
        self.period = self.fly_time + self.rest_time
        self.points = 0

    def add_point(self):
        self.points += 1

    def get_points(self):
        return self.points

    def distance_at(self, t):
        d = 0
        last_start = t - (t % self.period)
        n_periods = t // self.period
        last_flying_interval = min(self.fly_time, t - last_start)
        flying_time = n_periods * self.fly_time + last_flying_interval
        d = self.speed * flying_time
        return d

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
        self.input_str = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])

    def test_compute_winner_at(self):
        self.assertEqual(compute_winner_at(parse_input(self.input_str), 1000), 1120)

    def test_compute_winner_by_points_at(self):
        self.assertEqual(compute_winner_by_points_at(parse_input(self.input_str), 1000), 689)
