import argparse
import re

"""
--- Day 9: Explosives in Cyberspace ---

Wandering around a secure area, you come across a datalink port to a new part
of the network. After briefly scanning it for interesting files, you find one
file in particular that catches your attention. It's compressed with an
experimental format, but fortunately, the documentation for the format is
nearby.

The format compresses a sequence of characters. Whitespace is ignored. To
indicate that some sequence should be repeated, a marker is added to the
file, like (10x2). To decompress this marker, take the subsequent 10 characters
and repeat them 2 times. Then, continue reading the file after the repeated
data. The marker itself is not included in the decompressed output.

If parentheses or other characters appear within the data referenced by a
marker, that's okay - treat it like normal data, not a marker, and then
resume looking for markers after the decompressed section.

For example:

    ADVENT contains no markers and decompresses to itself with no changes,
    resulting in a decompressed length of 6.

    A(1x5)BC repeats only the B a total of 5 times, becoming ABBBBBC for a
    decompressed length of 7.

    (3x3)XYZ becomes XYZXYZXYZ for a decompressed length of 9.

    A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a
    decompressed length of 11.

    (6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but
    because it's within a data section of another marker, it is not treated
    any differently from the A that comes after it. It has a decompressed
    length of 6.

    X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of
    18), because the decompressed data from the (8x2) marker (the (3x3)ABC)
    is skipped and not processed further.

What is the decompressed length of the file (your puzzle input)? Don't count
whitespace.

----
Part two:

Apparently, the file actually uses version two of the format.

In version two, the only difference is that markers within decompressed data
are decompressed. This, the documentation explains, provides much more
substantial compression capabilities, allowing many-gigabyte files to be stored
in only a few kilobytes.

For example:

    (3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains
        no markers.
    X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY, because the decompressed
        data from the (8x2) marker is then further decompressed, thus triggering
        the (3x3) marker twice for a total of six ABC sequences.

    (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated
    241920 times.

    (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445
    characters long.

Unfortunately, the computer you brought probably doesn't have enough memory to
actually decompress the file; you'll have to come up with another way to get
its decompressed length.

What is the decompressed length of the file using this improved format?

"""


def parse_input(fi):
    return fi.readline().rstrip()


def decompress_v2(line):
    i = 0
    size = 0

    while i < len(line):
        marker = marker_ahead(line, i)
        if marker:
            i = skip_marker(line, i)
            new_substring = line[i:i+marker[0]]
            size += marker[1] * decompress_v2(new_substring)
            i += len(new_substring)
        else:
            size +=1
            i += 1

    return size


def decompress(line):
    decompressed_line = ''
    i = 0
    while i < len(line):
        marker = marker_ahead(line, i)
        if marker:
            length = marker[0]
            repeats = marker[1]
            i = skip_marker(line, i)

            decompressed_substring = line[i:i+length]*repeats
            decompressed_line += decompressed_substring
            i += length
        else:
            decompressed_line += line[i]
            i += 1

    return decompressed_line


def skip_marker(line, index):
    if line[index] != '(':
        msg = "Error: No marker at this position: {}, instead of (, found {}".format(
            index, line[index])
        raise ValueError(msg)

    new_index = index
    while line[new_index] != ')':
        new_index += 1

    new_index += 1

    return new_index


def marker_ahead(line, index):
    remainder = line[index:]
    if remainder[0] == '(':
        remainder = remainder[0: remainder.find(')')+1]
        values = re.findall('\((.*?)x(.*?)\)', remainder)[0]
        if values:
            return [int(v) for v in values]

    return None


def compute_compression_percentage_reduction(size_compressed, size_decompressed):
    return (size_decompressed - size_compressed)*100/float(size_decompressed)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 09: Explosives in cyberspace')

    parser.add_argument('in_file', help='Input data')

    args = parser.parse_args()

    fi = open(args.in_file)
    compressed_line = parse_input(fi)
    fi.close()

    decompressed_line = decompress(compressed_line)
    decompressed_size_v2 = decompress_v2(compressed_line)

    compression_percentage = compute_compression_percentage_reduction(
        len(compressed_line),
        len(decompressed_line))

    compression_percentage_v2 = compute_compression_percentage_reduction(
        len(compressed_line),
        decompressed_size_v2)


    print "Decompressed line has length {} (from {} compressed).".format(
        len(decompressed_line), len(compressed_line))

    print "Decompressed line v2 has length {} (from {} compressed).".format(
        decompressed_size_v2, len(compressed_line))

    print "\nExperimental algorithm reduced the string on a {:.5f} %".format(
        compression_percentage)

    print "Experimental algorithm v2 reduced the string on a {:.5f} %".format(
        compression_percentage_v2)