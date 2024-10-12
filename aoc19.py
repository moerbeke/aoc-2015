########################################################################
# Advent of Code 2015 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from math import inf

g_atoms = None
g_min_steps = inf
g_medicine = None
g_medicine_str = None
g_medicine_str_len = 0
g_initial_atom = 'e'

def solve_1(input_str):
    replacements, medicine = parse_input(input_str)
    molecules = compute_molecules(replacements, medicine)
    return len(molecules)

def solve_2(input_str):
    global g_min_steps
    g_min_steps = inf
    replacements, medicine = parse_input(input_str)
    reverse_replacements_unsorted = dict()
    print(replacements)
    for atom in replacements:
        for replacement in replacements[atom]:
            replacement_str = synthesise(replacement)
            reverse_replacements_unsorted[replacement_str] = atom
    print(reverse_replacements_unsorted)
    global g_reverse_replacements
    g_reverse_replacements = dict()
    for replacement_str in sorted(reverse_replacements_unsorted, key=len, reverse=True):
        g_reverse_replacements[replacement_str] = reverse_replacements_unsorted[replacement_str]
    print(g_reverse_replacements)
    global g_patterns
    g_patterns = list(g_reverse_replacements.keys())
    make_medicine()
    return g_min_steps

def parse_input(input_str):
    replacements_str, medicine_str = input_str.split('\n\n')
    replacements = dict()
    for line in replacements_str.strip().split('\n'):
        atom, replacement_str = line.split(' => ')
        #replacement_components = analyse_atom(replacement)
        if atom not in replacements:
            replacements[atom] = list()
        replacements[atom].append(replacement_str)
    global g_atoms
    g_atoms = replacements.keys()
    for atom in g_atoms:
        molecules_str = replacements[atom]
        replacements[atom] = []
        for molecule_str in molecules_str:
            replacements[atom].append(analyse(molecule_str))
    medicine = analyse(medicine_str.strip())
    global g_medicine
    g_medicine = medicine.copy()
    global g_medicine_str
    global g_medicine_str_len
    g_medicine_str = synthesise(medicine)
    g_medicine_str_len = len(g_medicine_str)
    return replacements, medicine

def synthesise(molecule):
    return ''.join(molecule)

def analyse(molecule_str):
    molecule = list()
    while molecule_str != '':
        atom = get_next_atom(molecule_str)
        molecule.append(atom)
        molecule_str = molecule_str[len(atom):]
    return molecule

def get_next_atom(molecule_str):
    if len(molecule_str) == 1:
        next_atom = molecule_str
    else:
        next_atom = molecule_str[:2]
        if next_atom not in g_atoms:
            next_atom = molecule_str[0]
    return next_atom

def compute_molecules(replacements, medicine):
    molecules = set()
    n = len(medicine)
    molecule = medicine.copy()
    for i in range(n):
        atom = medicine[i]
        if atom in replacements:
            for replacement in replacements[atom]:
                molecule[i] = synthesise(replacement)
                molecules.add(synthesise(molecule))
            molecule[i] = atom
    return molecules

def make_medicine():
    """Example of iteration - backwards strategy

Replacements:
e => H
e => O
H => HO
H => OH
O => HH

Start molecule: e
Longest output length: 2
Iteration order:
- After a replacement, start at index 0
- While at a given index, explore all replacements at index 
- Move index

Medicine: HOH
#   Step  Input   Index  Pattern  Match  Action     Output
--------------------------------------------------------------------------
1   1     HOH     0      HO       Y      HO <= H    HH
2   2     HH      0      HH       Y      HH <= O    O
3   3     O       0      O        Y      O <= e     e  EUREKA!!! - goto 2
4   2     HH      0      H        Y      H <= e     too long - goto 2
5   2     HH      1      H        Y      H <= e     too long - goto 1
6   1     HOH     0      H        Y      H <= e     too long - goto 1
7   1     HOH     1      OH       Y      OH <= H    HH visited - goto 1
8   1     HOH     1      O        Y      O <= e     too long - goto 1
9   1     HOH     2      H        Y      H <= e     too long - END!!!

Medicine: HOHOHO
#   Step  Input   Index  Pattern  Match  Action     Output
---------------------------------------------------------------------------
1   1     HOHOHO  0      HO       Y      HO <= H    HHOHO
2   2     HHOHO   0      HH       Y      HH <= O    OOHO
3   3     OOHO    0      O        Y      O <= e     too long - goto 3
4   3     OOHO    1      OH       Y      OH <= H    OHO
5   4     OHO     0      OH       Y      OH <= H    HO
6   5     HO      0      HO       Y      HO <= H    H
7   6     H       0      H        Y      H <= e     EUREKA!!! - goto 6
8   5     HO      0      H        Y      H <= e     too long - goto 6
9   5     HO      1      O        Y      O <= e     too long - goto 5
10  4     OHO     0      O        Y      O <= e     too long - goto 5
11  4     OHO     1      HO       Y      HO <= H    OH
12  5     OH      0      OH       Y      OH <= H    H  visited - goto 12
13  5     OH      0      O        Y      O <= e     too long - goto 12
14  5     OH      1      H        Y      H <= e     too long - goto 11
15  4     OHO     1      H        Y      H <= e     too long - goto 11
16  4     OHO     2      O        Y      O <= e     too long - goto 5
17  4     OHO     1      H        Y      H <= e     too long - goto 5
18  4     OHO     2      O        Y      O <= e     too long - goto 4
19  3     OOHO    1      O        Y      O <= e     too long - goto 4
20  3     OOHO    2      HO       Y      HO <= H    OOH
21  4     OOH     0      O        Y      O <= e     too long - goto 21
22  4     OOH     1      OH       Y      OH <= H    OH  visited - goto 21
23  4     OOH     1      O        Y      O <= e     too long - goto 21
24  4     OOH     2      H        Y      H <= e     too long - goto 4
25  3     OOHO    2      H        Y      H <= e     too long - goto 4
26  3     OOHO    3      O        Y      H <= e     too long - goto 3
27  3     OOHO    1      O        Y      O <= e     too long - goto 3
28  3     OOHO    2      HO       Y      HO <= H    OOH  visited - goto 3
29  3     OOHO    2      H        Y      H <= e     too long - goto 3
30  3     OOHO    3      O        Y      O <= e     too long - goto 2
31  2     HHOHO   0      H        Y      H <= e     too long - goto 2
32  2     HHOHO   1      HO       Y      HO <= H    HHHO
33  3     HHHO    0      HH       Y      HH <= O    OHO  visited - goto 33
34  3     HHHO    0      H        Y      H <= e     too long - goto 33
35  3     HHHO    1      HH       Y      HH <= O    HOO
36  4     HOO     0      HO       Y      HO <= H    HO  visited - goto 36
37  4     HOO     0      H        Y      H <= e     too long - goto 36
38  4     HOO     1      O        Y      O <= e     too long - goto 36
39  4     HOO     2      O        Y      O <= e     too long - goto 33
40  3     HHHO    1      H        Y      H <= e     too long - goto 33
41  3     HHHO    2      HO       Y      HO <= H    HHH
42  4     HHH     0      HH       Y      HH <= O    OH  visited - goto 42
43  4     HHH     0      H        Y      H <= e     too long - goto 42
44  4     HHH     1      HH       Y      HH <= O    HO  visited - goto 42
45  4     HHH     1      H        Y      H <= e     too long - goto 42
46  4     HHH     2      H        Y      H <= e     too long - goto 33
47  3     HHHO    2      H        Y      H <= e     too long - goto 33
48  3     HHHO    3      O        Y      O <= e     too long - goto 32
49  2     HHOHO   1      H        Y      H <= e     too long - goto 32
50  2     HHOHO   2      OH       Y      OH <= H    HHHO  visited - goto 32
51  2     HHOHO   2      O        Y      O <= e     too long - goto 32
52  2     HHOHO   3      HO       Y      HO <= H    HHOH
53  3     HHOH    0      HH       Y      HH <= O    OOH  visited - goto 53
54  3     HHOH    0      H        Y      H <= e     too long - goto 53
55  3     HHOH    1      HO       Y      HO <= H    HHH  visited - goto 53
56  3     HHOH    1      H        Y      H <= e     too long - goto 53
57  3     HHOH    2      OH       Y      OH <= H    HHH  visited - goto 53
58  3     HHOH    2      O        Y      O <= e     too long - goto 53
59  3     HHOH    3      H        Y      H <= e     too long - goto 32
60  2     HHOHO   3      H        Y      H <= e     too long - goto 32
61  2     HHOHO   4      O        Y      O <= e     too long - goto 2
62  2     HHOHO   1      H        Y      H <= e     too long - goto 2
63  2     HHOHO   2      OH       Y      OH <= H    HHHO  visited - goto 2
64  2     HHOHO   2      O        Y      O <= e     too long - goto 2
65  2     HHOHO   3      HO       Y      HO <= H    HHOH  visited - goto 2
66  2     HHOHO   3      H        Y      H <= e     too long - goto 2
67  2     HHOHO   4      O        Y      O <= e     too long - goto 1
68  1     HOHOHO  0      H        Y      H <= e     too long - goto 1
69  1     HOHOHO  1      OH       Y      OH <= H    HHOHO  visited - goto 1
70  1     HOHOHO  1      O        Y      O <= e     too long - goto 1
71  1     HOHOHO  2      HO       Y      HO <= H    HOHHO
72  2     HOHHO   0      HO       Y      HO <= H    HHHO  visited - goto 72
73  2     HOHHO   0      H        Y      H <= e     too long - goto 72
74  2     HOHHO   1      OH       Y      OH <= H    HHHO  visited - goto 72
75  2     HOHHO   1      O        Y      O <= e     too long - goto 72
76  2     HOHHO   2      HH       Y      HH <= O    HOOO
77  3     HOOO    0      HO       Y      HO <= H    HOO  visited - goto 77
78  3     HOOO    0      H        Y      H <= e     too long - goto 77
79  3     HOOO    1      O        Y      O <= e     too long - goto 77
80  3     HOOO    2      O        Y      O <= e     too long - goto 77
81  3     HOOO    3      O        Y      O <= e     too long - goto 72
82  2     HOHHO   2      H        Y      H <= e     too long - goto 72
83  2     HOHHO   3      HO       Y      HO <= H    HOHH
84  3     HOHH    0      HO       Y      HO <= H    HHH  visited - goto 84
85  3     HOHH    0      H        Y      H <= e     too long - goto 84
86  3     HOHH    1      OH       Y      OH <= H    HHH  visited - goto 84
87  3     HOHH    1      O        Y      O <= e     too long - goto 84
88  3     HOHH    2      HH       Y      HH <= O    HOO  visited - goto 84
89  3     HOHH    2      H        Y      H <= e     too long - goto 84
90  3     HOHH    3      H        Y      H <= e     too long - goto 72
91  2     HOHHO   3      H        Y      H <= e     too long - goto 72
92  2     HOHHO   4      O        Y      O <= e     too long - goto 1
93  1     HOHOHO  2      H        Y      H <= e     too long - goto 1
94  1     HOHOHO  3      OH       Y      OH <= H    HOHHO  visited - goto 1
95  1     HOHOHO  3      O        Y      O <= e     too long - goto 1
96  1     HOHOHO  4      HO       Y      HO <= H    HOHOH
97  2     HOHOH   0      HO       Y      HO <= H    HHOH  visited - goto 97
98  2     HOHOH   0      H        Y      H <= e     too long - goto 97
99  2     HOHOH   1      OH       Y      OH <= H    HHOH  visited - goto 97
100 2     HOHOH   1      O        Y      O <= e     too long - goto 97
101 2     HOHOH   2      HO       Y      HO <= H    HOHH  visited - goto 97
102 2     HOHOH   2      H        Y      H <= e     too long - goto 97
103 2     HOHOH   3      OH       Y      OH <= H    HOHH  visited - goto 97
104 2     HOHOH   3      O        Y      O <= e     too long - goto 97
105 2     HOHOH   4      H        Y      H <= e     too long - goto 1
106 1     HOHOHO  4      H        Y      H <= e     too long - goto 1
107 1     HOHOHO  5      O        Y      O <= e     too long - END!!!
...
    """
    global g_n
    g_n = 0
    global g_tested_molecules
    g_tested_molecules = list()
    initial_molecule = g_medicine.copy()
    initial_step = 0
    iterate(initial_step, initial_molecule)

def iterate(step, molecule):
    """
Start molecule: e
Longest output length: 2
Iteration order:
- After a replacement, start at index 0
- While at a given index, explore all replacements at index 
- Move index
#   Step  Input   Index  Pattern  Match  Action     Output
    """
    global g_n
    global g_min_steps
    global g_tested_molecules
    molecule_str = synthesise(molecule)
    #print("%s == %s ?" % (molecule_str, g_initial_atom))
    if molecule_str == g_initial_atom:
        g_min_steps = min(g_min_steps, step)
        #print("EUREKA!")
        return
    if g_initial_atom in molecule or len(molecule_str) > len(g_medicine_str):
        #print(molecule_str, "too long EXIT", '-'*100)
        return
    for index in range(len(molecule)):
        matching_patterns = find_patterns(molecule_str, index)
        for pattern_str in matching_patterns:
            reverse_replacement = g_reverse_replacements[pattern_str]
            next_molecule_str = replace_reverse_pattern(molecule_str, index, pattern_str, reverse_replacement)
            next_molecule = analyse(next_molecule_str)
            g_n += 1
            print("#%9d  [%4s %6d]  %4d  (%3d) %-60s  %3d  %-10s <= %-2s  (%3d) %-20s" %(
                g_n, str(g_min_steps), len(g_tested_molecules), step, len(molecule_str), molecule_str[:60], index,
                pattern_str, reverse_replacement, len(next_molecule_str), next_molecule_str[:20]))
            if next_molecule in g_tested_molecules:
                #print(next_molecule, "visited - EXIT", '-'*100)
                continue
            iterate(step+1, next_molecule)
            g_tested_molecules.append(next_molecule)

def find_patterns(molecule_str, index):
    sub_molecule_str = molecule_str[index:]
    matching_patterns = list()
    for pattern in g_patterns:
        if sub_molecule_str.find(pattern) == 0:
            matching_patterns.append(pattern)
    return matching_patterns

def replace_reverse_pattern(molecule_str, index, pattern_str, reverse_replacement):
    #print("replace_reverse_pattern 0", molecule_str, index, pattern_str, reverse_replacement)
    next_molecule_str = molecule_str[:index]
    #print("replace_reverse_pattern 1", index, next_molecule_str)
    next_molecule_str += reverse_replacement
    #print("replace_reverse_pattern 2", next_molecule_str)
    next_molecule_str += molecule_str[index+len(pattern_str):]
    #print("replace_reverse_pattern 3", next_molecule_str)
    return next_molecule_str

def iterate_1(step, molecule, replacements, medicine):
    """Example of iteration - forewards strategy, in depth first

Replacements:
e => H
e => O
H => HO
H => OH
O => HH

Medicine
HOH

Start molecule: e

Action      Step      Output
----------------------------------
1:e => H      1         H
1:H => HO     2         HO
1:H => HO     3         HOO
1:H => HO     4         HOOO backtrack
1:H <= HO     3         HOO
1:H => OH     4         OHOO backtrack
1:H <= OH     3         HOO
2:O => HH     4         HHHO backtrack
2:O <= HH     3         HOO
3:O => HH     4         HOHH backtrack
3:O <= HH     3         HOO
1:H <= HO     2         HO
2:O => HH     3         HHH
1:H => HO     4         HOHH backtrack
...
1:e => O      1         O
1:O => HH     2         HH
1:H => HO     3         HOH EUREKA!!! backtrack
1:H <= HO     2         HH
...
    """
    global g_n
    g_n += 1
    global g_min_steps
    #if step > g_min_steps:
        #print("0 EXIT", '-'*100)
        #return
    molecule_str = synthesise(molecule)
    #print("step", step, g_min_steps, molecule_str[:60]+"[...]"+molecule_str[-60:], len(molecule_str))
    print(g_n, "step", step, "["+str(g_min_steps)+"]", len(molecule_str), molecule_str)
    if molecule == medicine:
        g_min_steps = min(g_min_steps, step)
        print("EUREKA!")
        return
    if len(molecule_str) > len(g_medicine_str):
        print("1 EXIT", '-'*100)
        return
    for atom_index in range(len(molecule)):
        #print("atom_index?", atom_index)
        #if molecule_str[:atom_index] != g_medicine_str[:atom_index]:
            #print("2 EXIT", molecule_str[:atom_index], '-'*100)
            #break
        atom = molecule[atom_index]
        if atom in replacements:
            #print("index", atom_index, atom)
            for replacement in replacements[atom]:
                next_molecule = replace_atom(molecule, replacement, atom_index)
                iterate_1(step+1, next_molecule, replacements, medicine)
                next_molecule = replace_atom(next_molecule, molecule[atom_index], atom_index)
                next_molecule[atom_index] = molecule[atom_index]

def replace_atom(molecule, replacement, atom_index):
    next_molecule = molecule[:atom_index]
    next_molecule.extend(replacement)
    next_molecule.extend(molecule[atom_index+1:])
    return next_molecule

########################################################################
# Tests
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
H => HO
H => OH
O => HH

HOH
""", 4),
                (
"""
H => HO
H => OH
O => HH

HOHOHO
""", 7),
                ]
        self.tc_2 = [
                (
"""
e => H
e => O
H => HO
H => OH
O => HH

HOH
""", 3),
                (
"""
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
""", 6),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
