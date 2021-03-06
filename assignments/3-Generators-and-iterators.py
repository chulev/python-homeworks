from itertools import count


def primes():
    prime_multiples = {}
    yield 2

    for number in count(3, 2):
        composite = prime_multiples.pop(number, None)
        if composite:
            next_odd_multiple = number + 2 * composite
            while next_odd_multiple in prime_multiples:
                next_odd_multiple += 2 * composite
            prime_multiples[next_odd_multiple] = composite
        else:
            prime_multiples[number ** 2] = number
            yield number


def fibonacci():
    first, second = 1, 1

    while True:
        yield first
        first, second = second, first + second


def alphabet(*, code='', letters=''):
    if code == 'lat' and not letters:
        letters = 'abcdefghijklmnopqrstuvwxyz'
    elif code == 'bg' and not letters:
        letters = 'абвгдежзийклмнопрстуфхцчшщъьюя'

    return (letter for letter in letters)


def intertwined_sequences(generators, *, generator_definitions={}):
    already_seen = {}
    for generator in generators:
        length = generator.pop('length', None)
        if generator['sequence'] in already_seen:
            for _ in range(length):
                yield next(already_seen[generator['sequence']])
        else:
            method = generator_definitions.get(generator['sequence'],
                                               generator.get('sequence', None)
                                               )
            sequence = generator.pop('sequence', None)
            if type(method) is str:
                generator_object = iter(globals()[sequence](**generator))
            else:
                generator_object = iter(method(**generator))

            already_seen[sequence] = generator_object

            for _ in range(length):
                yield next(already_seen[sequence])