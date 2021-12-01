import sys


def read_input():
    return [int(line) for line in sys.stdin.readlines() if line.strip()]


def part_1(data):
    current = data[0]
    acc = 0

    for n in data:
        if n > current:
            acc += 1
        current = n

    return acc


def part_2(data):
    current = sum(data[:3])
    acc = 0

    for (a, b, c) in zip(data, data[1:], data[2:]):
        if (a + b + c) > current:
            acc += 1

        current = a + b + c

    return acc


data = read_input()
print(part_1(data))
print(part_2(data))
