import argparse
"""
--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of course,
the list is encrypted and full of decoy data, but the instructions to decode
the list are barely hidden nearby. Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes)
followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters in
the encrypted name, in order, with ties broken by alphabetization. For example:

    aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters
    are a (5), b (3), and then a tie between x, y, and z, which are listed
    alphabetically.
    a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are
    all tied (1 of each), the first five are listed alphabetically.
    not-a-real-room-404[oarel] is a real room.
    totally-real-room-200[decoy] is not.

Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?


"""

def compare(a, b):
    result = 0

    if a[1] > b[1]:
        result = -1
    elif a[1] < b[1]:
        result = 1
    else:
        if a[0] < b[0]:
            result = -1
        elif a[0] > b[0]:
            result = 1
        else:
            result = 0

    return result


def extract_checksum(code):
    return code[-6:-1]


def extract_sector_id(code):
    return int(code[code.rfind('-')+1:-7])


def extract_letters(code):
    return code[0:code.rfind('-')]


def count_letters(string):
    result = {}
    string = [s for s in string if s != '-']
    for s in string:
        result[s] = result.get(s, 0) + 1

    return result


def validate_code(letters, checksum):
    counts = count_letters(letters)
    sorted_items = sorted(counts.items(), cmp=compare, reverse=False)
    result = True
    for i in range(len(checksum)):
        if checksum[i] != sorted_items[i][0]:
            result = False

    return result


def extract_sector_value(code):
    result = 0
    letters = extract_letters(code)
    checksum = extract_checksum(code)
    if validate_code(letters, checksum):
        result += extract_sector_id(code)

    return result

def shift_name(letters, number):
    result = ''
    for l in letters:
        if l == '-':
            result += ' '
        else:
            result += shift_letter(l, number)

    return result

def shift_letter(letter, number):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    letter_position = alphabet.find(letter)
    new_position = (letter_position + number) % len(alphabet)
    return alphabet[new_position]

def extract_shifted_name(code):
    sector_id = extract_sector_id(code)
    letters = extract_letters(code)

    new_name = shift_name(letters, sector_id)
    return new_name

def sum_sector_values(code_list):
    acum = 0
    for code in code_list:
        acum += extract_sector_value(code)

    return acum


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 04: Security through obscurity')

    parser.add_argument('in_file', help='Input codes file')

    args = parser.parse_args()

    fi = open(args.in_file)
    codes = [line.rstrip() for line in fi.readlines()]

    fi.close()

    sector_id_sum = sum_sector_values(codes)


    print "The sector_ids for the true codes sum {}".format(sector_id_sum)

    for code in codes:
        shifted_name = extract_shifted_name(code)
        print shifted_name, extract_sector_id(code)
        # if shifted_name == 'north pole objects':
        #    print extract_sector_id(code)

