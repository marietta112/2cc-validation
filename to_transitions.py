

if __name__ == '__main__':
    transitions = []
    aut = {0: (False, {1: 7, 35: 3, 37: 1, 7: 4, 16: 4, 21: 4, 23: 4, 30: 5}), 1: (False, {1: 2, 35: 0, 37: 0, 7: 0, 16: 0, 21: 0, 23: 0, 30: 0}), 2: (False, {1: 1, 35: 0, 37: 0, 7: 0, 16: 0, 21: 0, 23: 0, 30: 3}), 3: (True, {1: 4, 35: 0, 37: 0, 7: 0, 16: 0, 21: 0, 23: 0, 30: 0}), 4: (False, {1: 3, 35: 0, 37: 0, 7: 0, 16: 0, 21: 0, 23: 0, 30: 0}), 5: (True, {1: 6, 35: 0, 37: 4, 7: 0, 16: 0, 21: 0, 23: 0, 30: 0}), 6: (True, {1: 5, 35: 0, 37: 0, 7: 0, 16: 0, 21: 0, 23: 0, 30: 0}), 7: (True, {1: 0, 35: 4, 37: 8, 7: 3, 16: 3, 21: 3, 23: 3, 30: 10}), 8: (False, {1: 9, 35: 0, 37: 0, 7: 0, 16: 0, 21: 0, 23: 0, 30: 0}), 9: (False, {1: 8, 35: 0, 37: 0, 7: 0, 16: 0, 21: 0, 23: 0, 30: 4}), 10: (True, {1: 11, 35: 0, 37: 3, 7: 0, 16: 0, 21: 0, 23: 0, 30: 0}), 11: (True, {1: 10, 35: 0, 37: 0, 7: 0, 16: 0, 21: 0, 23: 0, 30: 0})}
    print(type(aut))




    # Prepare a list to hold the formatted strings
    formatted_strings = []

    for i in range(len(aut.keys())):
        # Extract the outer key (0 in this case)
        outer_key = list(aut.keys())[i]
        # Extract the inner dictionary from the tuple
        inner_dict = aut[outer_key][1]
        # Loop through the inner dictionary
        for key, value in inner_dict.items():
            # Format each string as "outer_key:inner_key>value"
            formatted_string = f"s{outer_key}:{key}>s{value}"
            formatted_strings.append(formatted_string)

    # Join the formatted strings with newline characters
    result = '\n'.join(formatted_strings)


    f = open("transitions.txt", "a")
    # s0:0>s0
    f.write(result)
    f.close()