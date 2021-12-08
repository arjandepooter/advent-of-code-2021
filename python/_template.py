import sys


def parse_line(line):
    return line


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


def part_1(data):
    pass


def part_2(data):
    pass


data = read_input()
print(part_1(data))
print(part_2(data))
