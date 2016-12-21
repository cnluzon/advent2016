import argparse
import time
import hashlib

"""
--- Day 6: Signals and Noise ---

Something is jamming your communications with Santa. Fortunately, your signal
is only partially jammed, and protocol in situations like this is to switch to
a simple repetition code to get the message through.

In this model, the same message is sent repeatedly. You've recorded the
repeating message signal (your puzzle input), but the data seems quite
corrupted - almost too badly to recover. Almost.

All you need to do is figure out which character is most frequent for each
position. For example, suppose you had recorded the following messages:

eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar

The most common character in the first column is e; in the second, a; in the
third, s, and so on. Combining these characters returns the error-corrected
message, easter.

Given the recording in your puzzle input, what is the error-corrected version
of the message being sent?


"""


def parse_input(fi):
    result = []
    for line in fi.readlines():
        result.append(list(line.rstrip()))

    return result


def count_column(message_matrix, column):
    counts = {}
    for i in range(len(message_matrix)):
        character = message_matrix[i][column]
        counts[character] = counts.get(character, 0) + 1

    return counts


def get_least_frequent_character(message_matrix, column):
    counts = count_column(message_matrix, column)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=False)

    return sorted_counts[0][0]


def get_most_frequent_character(message_matrix, column):
    counts = count_column(message_matrix, column)
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_counts[0][0]


def decode_message_most_frequent_character(message_matrix):
    message = ''
    for i in range(len(message_matrix[0])):
        message += get_most_frequent_character(message_matrix, i)

    return message


def decode_message_least_frequent_character(message_matrix):
    message = ''
    for i in range(len(message_matrix[0])):
        message += get_least_frequent_character(message_matrix, i)

    return message

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 06: Signals and noise')

    parser.add_argument('in_file', help='Input signal')

    args = parser.parse_args()

    fi = open(args.in_file)
    signal = parse_input(fi)
    fi.close()

    message = decode_message(signal)

    print "The message is {}".format(message)