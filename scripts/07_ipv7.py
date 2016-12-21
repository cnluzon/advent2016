import argparse
import time
import hashlib
import re

"""
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP
addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to
figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA.
An ABBA is any four-character sequence which consists of a pair of two
different characters followed by the reverse of that pair, such as xyyx or
abba. However, the IP also must not have an ABBA within any hypernet sequences,
which are contained by square brackets.

For example:

    abba[mnop]qrst supports TLS (abba outside square brackets).
    abcd[bddb]xyyx does not support TLS (bddb is within square brackets,
        even though xyyx is outside square brackets).
    aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior
        characters must be different).
    ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even
        though it's within a larger string).

How many IPs in your puzzle input support TLS?


"""


def parse_input(fi):
    result = [line.rstrip() for line in fi.readlines()]
    return result


def is_tls_supported(address):
    tls_supported = False
    abba_within_brackets = contains_abba_within_brackets(address)
    if not abba_within_brackets:
        abba_outside_brackets = contains_abba_outside_brackets(address)
        if abba_outside_brackets:
            tls_supported = True

    return tls_supported


def is_ssl_supported(address):

    outside_brackets_list = extract_outside_brackets_strings(address)
    within_brackets_list = extract_within_brackets_strings(address)

    aba_accessor_list = extract_abas(outside_brackets_list)
    bab_accessor_list = extract_abas(within_brackets_list)

    for aba in aba_accessor_list:
        if matching_bab(aba) in bab_accessor_list:
            return True

    return False


def matching_bab(s):
    result = s[1] + s[0] + s[1]
    return result


def extract_abas(string_list):
    result = []
    for s in string_list:
        for i in range(len(s)-2):
            if is_aba(s[i:i+3]):
                result.append(s[i:i+3])

    return result


def is_aba(s):
    if (s[0] != s[1]) and (s[0] == s[2]):
        return True

    return False


def extract_within_brackets_strings(address):
    result = re.findall('\[(.*?)\]', address)
    return result


def extract_outside_brackets_strings(address):
    result = re.sub('\[(.*?)\]', '-', address)
    result = result.split('-')

    return result


def contains_abba_within_brackets(address):
    within_brackets_list = extract_within_brackets_strings(address)
    for s in within_brackets_list:
        if contains_abba(s):
            return True


def contains_abba_outside_brackets(address):
    outside_brackets_list = extract_outside_brackets_strings(address)
    for s in outside_brackets_list:
        if contains_abba(s):
            return True


def contains_abba(string):
    for i in range(len(string)-3):
        if is_abba(string[i:i+4]):
            return True

    return False


def is_abba(string):
    result = False
    if string[0] == string[-1]:
        if (string[1] == string[2]) and (string[0] != string[1]):
            result = True

    return result


def count_ips_with_property(ip_list, property_function):
    count = 0

    for address in ip_addresses:
        if property_function(address):
            count += 1

    return count

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Solve Advent of Code 2016 problem 07: IPv7')

    parser.add_argument('-f', '--file', help='Input codes')
    parser.add_argument('-c', '--code', help='Single input code')

    args = parser.parse_args()

    ip_addresses = None
    if args.file:
        fi = open(args.file)
        ip_addresses = parse_input(fi)
        fi.close()

    if args.code:
        ip_addresses = [args.code]

    if ip_addresses:

        ipv7_with_tls_count = count_ips_with_property(ip_addresses,
                                                      is_tls_supported)

        ipv7_with_ssl_count = count_ips_with_property(ip_addresses,
                                                      is_ssl_supported)

        print "There are {} addresses that support TLS out of {}".format(
            ipv7_with_tls_count, len(ip_addresses))


        print "There are {} addresses that support SSL out of {}".format(
            ipv7_with_ssl_count, len(ip_addresses))

    else:
        print "Please, provide either a code or a code file"