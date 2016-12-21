import argparse
import time
import hashlib

"""
--- Day 5: How About a Nice Game of Chess? ---

You are faced with a security door designed by Easter Bunny engineers that seem
to have acquired most of their security knowledge by watching hacking movies.

The eight-character password for the door is generated one character at a time
by finding the MD5 hash of some Door ID (your puzzle input) and an increasing
integer index (starting with 0).
    
A hash indicates the next character in the password if its hexadecimal
representation starts with five zeroes. If it does, the sixth character in the
hash is the next character of the password.

For example, if the Door ID is abc:

    The first index which produces a hash that starts with five zeroes is
    3231929, which we find by hashing abc3231929; the sixth character of the
    hash, and thus the first character of the password, is 1.

    5017308 produces the next interesting hash, which starts with 000008f82...,
    so the second character of the password is 8.

    The third time a hash starts with five zeroes is for abc5278568,
    discovering the character f.

In this example, after continuing this search a total of eight times,
the password is 18f47a30.

Given the actual Door ID, what is the password?

Input: ugkcyxxp

"""


def hash_meets_condition(string):
    encoded_string = string.encode("hex")
    return encoded_string[0:5] == '00000'


def compute_md5_hash_code(string):
    current_hash = hashlib.md5()
    current_hash.update(string)
    hashed_code = current_hash.digest()
    return hashed_code


def find_next_hash_number(door_id, attached_number):
    current_code = '{}{}'.format(door_id, attached_number)
    current_hash = compute_md5_hash_code(current_code)

    while not hash_meets_condition(current_hash):
        attached_number += 1
        current_code = '{}{}'.format(door_id, attached_number)
        current_hash = compute_md5_hash_code(current_code)

    return attached_number


def find_hash_password(door_id, pass_length):
    attached_number = 0
    password = ''
    for i in range(pass_length):
        attached_number = find_next_hash_number(door_id, attached_number)
        valid_code = '{}{}'.format(door_id, attached_number)
        valid_hash = compute_md5_hash_code(valid_code).encode("hex")
        password += valid_hash[5]
        attached_number += 1

    return password

def find_hash_password_part_two(door_id, pass_length):
    attached_number = 0
    password = ['_']*pass_length

    while '_' in password:
        attached_number = find_next_hash_number(door_id, attached_number)
        valid_code = '{}{}'.format(door_id, attached_number)
        valid_hash = compute_md5_hash_code(valid_code).encode("hex")
        position = int('0x{}'.format(valid_hash[5]), 16)
        if position < pass_length and password[position] == '_':
            password[position] = valid_hash[6]
            print ''.join(password)

        attached_number += 1

    return ''.join(password)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 05: Game of chess')

    parser.add_argument('code', help='Input code')

    args = parser.parse_args()


    start = time.time()
    password = find_hash_password(args.code, 8)
    end = time.time()

    print "The password is {}".format(password)
    print "It took {} seconds to hack".format(str(end-start))

    start = time.time()
    password_two = find_hash_password_part_two(args.code, 8)
    end = time.time()

    print "The new password is {}".format(password_two)
    print "It took {} seconds to hack".format(str(end-start))
