# Code to validate results, version 07.07.2024

import numpy as np
from enum import Enum
from itertools import combinations

'''
Steps for this validation: 

1. Transform tiles into propagations matrices (remember to flip end vertices!!) DONE
2. Get closure of the propagation matrices DONE
2a. Multiply the existing tiles all with each other 
2b. Check for new ones, multiply those with existing
2c. Repeat until no new ones have been found
2d. Matrix binning 
3. Find & store those which have a 0 in (0,0) and (1,0) DONE
4. Find those that might lead to a 4-chrom propagation OQO!
5. Construct the transition function for the automata OQO!
6. Check they agree with previous result OQO!
7. Maybe, construct automata and check that our characterisation is actually correct
'''

class Indices(Enum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8


def get_index(first, second):
    """
    A function to indicate in which position a 1 is stored in a propagation matrix.
    :param first: integer corresponding to the first entry in an input/output propagation.
    :param second: integer corresponding to the second entry in an input/output propagation.
    :return: integer representing the row/coloumn co-ordinate of a matrix.
    """
    if first == 1:
        if second == 1:
            return Indices.ONE.value
        elif second == 2:
            return Indices.TWO.value
        elif second == 3:
            return Indices.THREE.value
    elif first == 2:
        if second == 1:
            return Indices.FOUR.value
        elif second == 2:
            return Indices.FIVE.value
        elif second == 3:
            return Indices.SIX.value
    elif first == 3:
        if second == 1:
            return Indices.SEVEN.value
        elif second == 2:
            return Indices.EIGHT.value
        elif second == 3:
            return Indices.NINE.value


def get_prop_matrix(concrete_prop):
    """
    This function produces a 9x9 matrix representing the propagation graph of a tile.

    :param concrete_props: a list of all concrete propagations that are allowed by some tile.
    :return: a 9x9 matrix representing all possible 3-colourings of a tile.
    """
    # Each tile T has a 9x9 propagation matrix related to it. Each entry is a 0 (if the prop is allowed for T) or 1 (otherwise)
    prop_matrix = np.zeros((9,9), dtype = int)

    # Each tile has two input colours and two output colours
    for entry in concrete_prop:
        i1 = int(entry[0])
        i2 = int(entry[1])
        idx1 = get_index(i1, i2)
        o1 = int(entry[3])
        o2 = int(entry[2])
        idx2 = get_index(o1, o2)
        prop_matrix[idx1][idx2] = 1

    return prop_matrix

def already_exists(matrix, list_of_matrices):
    """
    Method to determine whether matrix is already in list_of_matrices or not.

    :param matrix: NumPy array representing a matrix.
    :param list_of_matrices: a list of NumPy arrays.
    :return: true if matrix is in list_of_matrices, false otherwise.
    """

    for array in list_of_matrices:
        if np.array_equal(matrix, array):
            return True
    return False

def get_closure(og_props):
    """
    Function takes a list of propagation matrices and gets their closure by multiplying all possible combinations of A.B
    where A and B are propagation matrices.

    :param og_props: list of NumPy arrays.
    :return : final list of all unique NumPy arrays in the closure and list of triples (A,B,C) s.t. A*B = C
    """
    all_props = og_props.copy()
    new_props = og_props.copy()
    temp = []

    records = []

    # num_new = 0
    i = 0

    while i <= 3:
        num_new = 0
        temp.clear()
        for og_prop in all_props:
            for matrix in new_props:
                prod1 = np.matmul(og_prop, matrix)
                prod1 = (prod1 > 0).astype(int)
                records.append((og_prop, matrix, prod1))
                prod2 = np.matmul(matrix, og_prop)
                prod2 = (prod2 > 0).astype(int)
                # records.append((og_prop, matrix, prod2)) - wrong one
                records.append((matrix, og_prop, prod2))
                if (not already_exists(prod1, all_props)) and (not already_exists(prod1, temp)):
                    # all_props.append(prod1)
                    temp.append(prod1)
                    # next_props.append(prod1)
                    num_new += 1
                if (not already_exists(prod2, all_props)) and (not already_exists(prod2, temp)):
                    # all_props.append(prod2)
                    temp.append(prod2)
                    # next_props.append(prod2)
                    num_new += 1

        # all_props = all_props + temp
        # new_props = temp.copy()
        # print("Number of new matrices found = ", num_new)
        # print("Number of matrices total = ", len(all_props))

        props_tuple = set(tuple(array.flatten()) for array in temp)
        # print("Number of unique original props in temp = ", len(props_tuple))
        props_arrays = [np.array(matrix).reshape(9, 9) for matrix in props_tuple]
        all_props = all_props + props_arrays
        new_props = props_arrays.copy()
        # print("-------------------------------------------------------------------------------")
        i += 1


    # print("Total number of prop matrices = ", len(all_props))
    return all_props, records

def check_diagonal(props):
    """
    Function that checks whether the diagonal elements of each array in a list of arrays is zero.

    :param props: list of NumPy arrays.
    :return: list of NumPy arrays whose diagonal entries are all zero.
    """
    not_three_colourable = []
    for prop in props:
        if np.all(np.diagonal(prop) == 0):
            not_three_colourable.append(prop)

    return not_three_colourable

def leads_to_zero_diag(records):
    leads_to_zero_diagonal = []

    for triple in records:
        if np.all(np.diagonal(triple[2]) == 0):
            if not already_exists(triple[0], leads_to_zero_diagonal):
                leads_to_zero_diagonal.append(triple[0])
            if not already_exists(triple[1], leads_to_zero_diagonal):
                leads_to_zero_diagonal.append(triple[1])
            if not already_exists(triple[2], leads_to_zero_diagonal):
                leads_to_zero_diagonal.append(triple[2])

    return leads_to_zero_diagonal

def are_triples_equal(triple1, triple2):
    return all(np.array_equal(a, b) for a, b in zip(triple1, triple2))

def generate_automata(special_matrices, prop_matrices, records):
    tiles_dict = dict()
    states = dict()  # Relate integer to prop matrix
    idx = 0
    original_aut_transitions = []

    for triple in records:
        if already_exists(triple[0], special_matrices) and already_exists(triple[2], special_matrices) and already_exists(triple[1], special_matrices):
            if already_exists(triple[1], prop_matrices):  # Check that B is a tile, since tiles form the alphabet
                if not already_exists(triple[0], list(states.values())):
                    states.update({idx: triple[0]})
                    idx += 1
                if not already_exists(triple[1], list(states.values())):
                    states.update({idx: triple[1]})
                    idx += 1
                if not already_exists(triple[1], list(tiles_dict.values())):
                    tiles_dict.update({idx: triple[1]})
                if not already_exists(triple[2], list(states.values())):
                    states.update({idx: triple[2]})
                    idx += 1

                original_aut_transitions.append(triple)

    return states, tiles_dict, original_aut_transitions


def compare_dict_values(dict1, dict2):
    # Check they have the same length
    assert len(dict1) == len(dict2)

    # Check if all values in dict1 are in dict2 using numpy array comparison
    map = dict()
    reverse_map = dict()
    num_matches = 0
    for key1, value1 in dict1.items():
        for key2, value2 in dict2.items():
            if np.array_equal(value1, value2):
                num_matches += 1
                map.update({key1: key2})
                reverse_map.update({key2: key1})
                continue

    assert num_matches == len(dict1)
    assert num_matches == len(dict2)

    return map, reverse_map

def get_key(my_dict, val):
    for key, value in my_dict.items():
        if np.array_equal(val, value):
            return key

    print("OQO!!")

def convert_raw_transitions(raw_transitions, dict):
    converted_transitions = []
    for transition in raw_transitions:
        converted_transitions.append((get_key(dict, transition[0]), get_key(dict, transition[1]), get_key(dict, transition[2])))

    return converted_transitions

def convert_num_transitions(numbered_transitions, mapping):
    converted_transitions = []
    for transition in numbered_transitions:
        converted_transitions.append((mapping[transition[0]], mapping[transition[1]], mapping[transition[2]]))

    return converted_transitions

def compare_automata_transitions(trans1, trans2):
    if set(trans1) == set(trans2):
        return True
    else:
        return False
