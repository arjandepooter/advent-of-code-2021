import sys
from itertools import tee


def parse_line(line):
    return int(line.strip(), 2)


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return (
        [parse_line(line) for line in lines],
        len(lines[0]),
    )


def bits_per_position(numbers, position):
    ones = sum((n >> position) & 1 for n in numbers)

    return len(numbers) - ones, ones


def part_1(numbers, width):
    gamma = 0

    for offset in range(width):
        zeroes, ones = bits_per_position(numbers, width - offset - 1)
        gamma <<= 1
        gamma |= ones > zeroes

    # epsilon rate is the bitwise inverse of the gamma rate
    eps = gamma ^ (1 << width) - 1

    return gamma * eps


def reduce_numbers_by_bit_occurence(numbers, width, most):
    offset = 0

    while len(numbers) > 1:
        position = width - offset - 1
        zeroes, ones = bits_per_position(numbers, position)
        numbers = [n for n in numbers if (n >> position) & 1 ^ (ones >= zeroes) ^ most]
        offset += 1

    return numbers[0]


def part_2(numbers, width):
    oxygen = reduce_numbers_by_bit_occurence(numbers[::], width, True)
    co2 = reduce_numbers_by_bit_occurence(numbers[::], width, False)

    return oxygen * co2


data = read_input()
print(part_1(*data))
print(part_2(*data))
