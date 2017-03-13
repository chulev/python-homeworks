import itertools


def largest_powers_of_two(number):
    """ Calculates the largest powers of two for a given number. """
    return [2 ** index for index, digit in
            enumerate(str(bin(number)[:1:-1])) if int(digit) > 0
            ]


def powers_of_two_remain(numbers):
    """ Checks if at least one frequency of occurence is an odd number. """
    all_powers_of_two = list(itertools.chain.from_iterable(
                             [largest_powers_of_two(number)
                              for number in numbers]))
    occurence_frequency = [all_powers_of_two.count(occurences)
                           for occurences in all_powers_of_two]

    return all(occurences % 2 == 0
               for occurences in occurence_frequency) is False
