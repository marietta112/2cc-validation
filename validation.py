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




# def multiplyPropMatrices(og_props):
    """
    This method multiplies all the propagation matrices with each other, in every possible order.

    :param og_props: A list of all original propagation matrices.
    :return: A list of all possible combinations of A * B, where A and B are propagation matrices.
    """

    # multiplied_matrices = set() # store matrix multiplications of og * og and og * new (= og * og)
    # triples = [] # store the equation A * B = C as (A,B,C)
    #
    # # multiply any two original prop matrices with each other
    # print("Multiplying og * og")
    # for i in range(len(og_props)):
    #     for j in range(len(og_props)):
    #         mat_mul = np.matmul(og_props[i], og_props[j])  # multiply two original prop matrices
    #         normalised_mat = (mat_mul > 0).astype(int)  # any +ve entry is set to 1
    #         print("Multiplying the two matrices: \n", og_props[i], "\n*\n" ,og_props[j])
    #         print("Matrix multiplication: ", normalised_mat)
    #         triples.append((f'og_matrix_{i}', f'og_matrix_{j}', normalised_mat))  # store triple
    #         product_tuple = tuple(normalised_mat.flatten()) # flatten to store in a set
    #         # print(triples[j])
    #         # if product_tuple not in multiplied_matrices:
    #         multiplied_matrices.add(product_tuple)
    # print("Number of prop matrices after og_prop * og_prop = ", len(multiplied_matrices))
    # print("--------------------------------------------------------------------------------------")
    # # found_new = True
    # i = 0
    # new_props_count = 1
    #
    # while new_props_count >= 1:
    #     # found_new = False
    #     i += 1
    #     new_props_count = 0
    #     # print("Number of matrices in multiplied_matrices beginning = ", len(multiplied_matrices))
    #     # Multiply og props with new props (resulting from og prop * og prop)
    #     current_props = list(multiplied_matrices)
    #     print("No. of elements in multiplied_matrices = ", len(current_props))
    #     for idx, matrix in enumerate(current_props):
    #
    #         matrix = np.array(matrix).reshape(9,9)
    #
    #         for og_idx, og_matrix in enumerate(og_props):
    #             product = np.matmul(matrix, og_matrix)
    #             print("Multiplying the two matrices: \n", matrix, "\n*\n" ,og_matrix)
    #             normalised_prod = (product > 0).astype(int)
    #             print("Matrix multiplication: ", normalised_prod)
    #             triples.append((f'new_matrix_{idx}', f'og_matrix_{og_idx}', normalised_prod))
    #             product_tuple = tuple(normalised_prod.flatten())
    #             if product_tuple not in multiplied_matrices:
    #                 multiplied_matrices.add(product_tuple)
    #                 # current_props.append(product_tuple)
    #                 found_new = True
    #                 new_props_count += 1
    #                 print("New prop between new %d and old %d" %(idx, og_idx))
    #
    #             product = np.matmul(og_matrix, matrix)
    #             print("Multiplying the two matrices: \n", og_matrix,"\n*\n" ,matrix)
    #             normalised_prod = (product > 0).astype(int)
    #             print("Matrix multiplication: ", normalised_prod)
    #             product_tuple = tuple(normalised_prod.flatten())
    #             triples.append((f'og_matrix_{og_idx}', f'new_matrix_{idx}', normalised_prod))
    #             if product_tuple not in multiplied_matrices:
    #                 multiplied_matrices.add(product_tuple)
    #                 # current_props.append(product_tuple)
    #                 found_new = True
    #                 new_props_count += 1
    #                 print("New prop between old %d and new %d" %(og_idx, idx))
    #
    #         # print("Number of current props after og * current = ", len(current_props))
    #         for other_idx, other_matrix in enumerate(current_props):
    #             other_matrix = np.array(other_matrix).reshape(9,9)
    #             product = np.matmul(matrix, other_matrix)
    #             print("Multiplying the two matrices: \n", matrix,"\n*\n", other_matrix)
    #             normalised_prod = (product > 0).astype(int)
    #             print("Matrix multiplication: ", normalised_prod)
    #             product_tuple = tuple(normalised_prod.flatten())
    #             triples.append((f'new_matrix_{idx}', f'new_matrix_{other_idx}', normalised_prod))
    #             if product_tuple not in multiplied_matrices:
    #                 multiplied_matrices.add(product_tuple)
    #                 # current_props.append(product_tuple)
    #                 found_new = True
    #                 new_props_count += 1
    #                 print("New prop between new %d and new %d" %(idx, other_idx))
    #
    #     print("End of Iteration %d, new props found = %d" %(i, new_props_count))
    #     print("--------------------------------------------------------------------------------------")
    #
    #     # print("Number of matrices in multiplied_matrices end = ", len(multiplied_matrices))
    #
    #
    #
    # multiplied_matrices = [np.array(matrix).reshape(9,9) for matrix in multiplied_matrices]
    #
    # # for record in triples:
    # #     print(f"{record[0]} * {record[1]} = \n{record[2]}\n")
    #
    # print("Numer of unique matrices found: ", len(multiplied_matrices))
    #
    #
    # return multiplied_matrices, triples, i

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
        print("Number of new matrices found = ", num_new)
        # print("Number of matrices total = ", len(all_props))

        props_tuple = set(tuple(array.flatten()) for array in temp)
        print("Number of unique original props in temp = ", len(props_tuple))
        props_arrays = [np.array(matrix).reshape(9, 9) for matrix in props_tuple]
        all_props = all_props + props_arrays
        new_props = props_arrays.copy()
        print("-------------------------------------------------------------------------------")
        i += 1


    print("Total number of prop matrices = ", len(all_props))
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
    triples = []

    for triple in records:
        if np.all(np.diagonal(triple[2]) == 0):
            if not already_exists(triple[0], leads_to_zero_diagonal):
                leads_to_zero_diagonal.append(triple[0])
            if not already_exists(triple[1], leads_to_zero_diagonal):
                leads_to_zero_diagonal.append(triple[1])
            if not already_exists(triple[2], leads_to_zero_diagonal):
                leads_to_zero_diagonal.append(triple[2])

            # triples.append((triple[2], triple[2], np.matmul(triple[2], triple[2]))) - this did not change the result!
            triples.append(triple)

    return leads_to_zero_diagonal, triples

