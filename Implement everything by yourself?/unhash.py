import re

def simplifiedHash(input_string):
    input_string = input_string + "#is the length o"

    h665 = input_string[16:32]

    sta = [] #How far should each char be shifted
    for char in h665:
        sta.append(ord(char))

    h664 = input_string[:16]

    print(f"h664: {h664}")

    for i in range(16):
        h664 = (h664[:i] +
                f2(h664[i], sta[i]) +
                h664[i + 1:])

    input_string = ""
    for i in range(0,16):
        input_string += h664[i]
        input_string += h665[i]

    return input_string.replace(" ", "_")

def f2(v1, v2):
    v3 = (ord(v1) + v2) %126
    it = 0
    while (v3 < 32 or v3 > 126):
        v3 = (v3 + ord(v1) + v2 + it) % 126
        it = it + 1
    return chr(v3)


def unhash(hashed_string):
    reversed_h665 = ""
    reversed_h664 = ""
    for i in range(0, 16):
        reversed_h664 += (hashed_string[i*2])
        reversed_h665 += (hashed_string[i*2+1])

    sta = [] #How far should each char be shifted
    for char in reversed_h665:
        sta.append(ord(char))

    possible_substitutions = {}

    for i in range(16 - 1, 0 - 1, -1):
        possibilities = reverse_f2(ord(reversed_h664[i]), sta[i])
        if len(possibilities) >= 1:
            reversed_h664 = (reversed_h664[:i] +
                    chr(possibilities[0]) +
                    reversed_h664[i + 1:])
        
        if len(possibilities) > 1:
            possible_substitutions[i] = possibilities[1:]
    
    # convert list to set
    possible_h664s = set()
    possible_h664s.add(reversed_h664)

    # generate all possible combinations of the possible substitutions
    old_len = len(reversed_h664)
    new_len = 0
    while old_len != new_len:
        old_len = new_len
        possible_h664s_tmp = set()

        for key in possible_substitutions:
            for h664 in possible_h664s:
                for possibility in possible_substitutions[key]:
                    possible_h664s_tmp.add(h664[:key] + chr(possibility) + h664[key+1:])

        possible_h664s = possible_h664s.union(possible_h664s_tmp)
        new_len = len(possible_h664s)

    # add the h665 back to the possible h664s to complete the original input string
    possible_input_strings = set(p + reversed_h665 for p in possible_h664s)

    return possible_input_strings


def reverse_f2(v3, known_v2):
    possibilities = []
    # v1 = (v3 - known_v2)
    # if v1 < 0:
    #     v1 = v1 + 126
    #     if v1 >= 32 and v1 <= 126:
    #         possibilities.append(v1)
    # else:
    #     v1 = v1 % 126
    #     if v1 >= 32 and v1 <= 126:
    #         possibilities.append(v1)
        
    
    # for oldv3 in range(0, 127):
    #     for realv1 in range(32, 127):
    #         if (oldv3 + realv1 + known_v2) % 126 == v3 and oldv3 == (realv1 + known_v2) % 126 and realv1 not in possibilities:
    #             possibilities.append(realv1)

    # older_v3_list = []
    # if possibilities:
    #     older_v3_list = [possibilities[0]]
    # else:
    #     older_v3_list = [(v3 - known_v2) % 126]
    # for it in range(0,5):
    #     print(it)
    #     older_v3_list_tmp = []
    #     for older_v3 in older_v3_list:
    #         for oldv3 in range(0, 127):
    #             for realv1 in range(32, 127):
    #                 if (oldv3 + realv1 + known_v2) % 126 == v3 and oldv3 == (older_v3 + realv1 + known_v2) % 126:
    #                     if realv1 not in possibilities:
    #                         possibilities.append(realv1)
    #                 else:
    #                     older_v3_list_tmp.append(oldv3)
    #     older_v3_list = older_v3_list_tmp


    # reverse the while loop in f2 to find the original v1 by brute force
    for realv1 in range(32, 127):
        tmp = ord(f2(chr(realv1), known_v2))
        if tmp == v3 and tmp not in possibilities:
            possibilities.append(realv1)

    # print(f"possibilities: {[chr(x) for x in possibilities]}, inputchar: {chr(v3)}, known_v2: {chr(known_v2)}")
    return possibilities


""" def reverse_f2(v3):
    possibilities = []
    for v1 in range(33, 127):
        for v2 in range(33, 127):
            if (v3 - v2) % 126 == v1:
                possibilities.append((v1, v2))
    return possibilities """

# def reverse_f3(v3):
#     v3o = (ord(v2) + v1) %126
#     for i in range(v1):
#         v3 = (v3o + ord(v2) + v1 + i) % 126
#     return v3 == -1


def unhash_underscore(hashed_string):
    # generate all possible combinations, where the underscore is replaced by a space
    input_strings = set()
    input_strings.add(hashed_string.replace("_", " "))

    old_len = len(input_strings)
    new_len = 0

    while old_len != new_len:
        old_len = new_len
        tmp_set = set()

        for input_string in input_strings:
            for i in range(0, len(input_string)):
                if input_string[i] == " ":
                    tmp_set.add(input_string[:i] + "_" + input_string[i+1:])
            
        input_strings = input_strings.union(tmp_set)
        new_len = len(input_strings)
    
    unhashed_strings = set()
    for input_string in input_strings:
        unhashed_strings = unhashed_strings.union(unhash(input_string))
    
    unhashed_strings_list = list(unhashed_strings)

    # sort unhashed_strings_list by the number of special characters in each string
    unhashed_strings_list.sort(key=lambda x: re.findall(r"[^a-zA-Z0-9\s]", x).__len__())
    
    # reverse list
    unhashed_strings_list.reverse()

    # this return all possible unhashed strings
    return unhashed_strings_list


def get_flag(unhashed_strings):
    # get the flag from the unhashed string
    possible_flags = []
    
    for unhashed_string in unhashed_strings:
        possible_flags += re.findall(r"fl4g{.*}", unhashed_string)
    
    # remove duplicates but keep the order
    possible_flags = list(dict.fromkeys(possible_flags))

    return possible_flags

def main():
    intput_string = input("Enter the hashed string but without the '{ ' and ' }' that might be at the beginning and end of the given string:\n")
    unhash_strings = unhash_underscore(intput_string)
    possible_flags = get_flag(unhash_strings)

    print("=" * 50)
    print("Possible flags:")

    for flag in possible_flags:
        print(flag)


if __name__ == "__main__":
    main()