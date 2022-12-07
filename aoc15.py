########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

properties = ['capacity', 'durability', 'flavor', 'texture', 'calories']
        
def solve_1(input_str):
    ingredients = parse_input(input_str)
    return find_best_recipe(ingredients)

def solve_2(input_str):
    return None

def parse_input(input_str):
    '''
    0             1        2   3          4   5      6  7       8  9        10
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    '''
    ingredients = list()
    for line in input_str.strip().split('\n'):
        words = line.split()
        name = words[0][:-1]
        ingredient = Ingredient(name)
        assert(len(words[1:]) % 2 == 0)
        for i in range(len(words[1:])//2):
            propname = words[1+2*i]
            propvalue = int(words[1+2*i+1].split(',')[0])
            ingredient.add_property(propname, propvalue)
        ingredients.append(ingredient)
    return ingredients

def find_best_recipe(ingredients):
    total_teaspoons = 100
    recipes = list()
    compute_cookie(total_teaspoons, recipes, ingredients)
    return max(recipes)

def compute_cookie(total_teaspoons, recipes, ingredients, t=list()):
    assert(sum(t) <= total_teaspoons)
    if len(t) < len(ingredients) - 1:
        for i in range(0, total_teaspoons):
            if sum(t) + i > total_teaspoons:
                continue
            t.append(i)
            compute_cookie(total_teaspoons, recipes, ingredients, t)
            del t[len(t)-1]
    elif len(t) == len(ingredients) - 1:
        j = total_teaspoons - sum(t)
        t.append(j)
        cookie = compute_value(ingredients, t)
        if cookie > 0:
            recipes.append(cookie)
        del t[len(t)-1]
    else:
        assert(False)

def compute_value(ingredients, t):
    cookie = 1
    for p in properties[:-1]:
        value = sum([t[i] * ingredients[i].get_property(p) for i in range(len(t))])
        value = max(value, 0)
        cookie *= value
        if cookie == 0:
            break
    return cookie

class Ingredient:

    def __init__(self, name):
        self.name = name
        self.properties = dict()

    def add_property(self, name, value):
        self.properties[name] = value

    def get_property(self, name):
        return self.properties[name]

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
""", 62842880),
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
