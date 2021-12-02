import sys


def parse_line(line):
    a, b = line.strip().split(" ")
    return (a, int(b))


def read_input():
    return [parse_line(line) for line in sys.stdin.readlines() if line.strip()]


def part_1(data):
    v, h = 0, 0
    
    for (d, n) in data:
        match d:
            case "forward":
                h += n
            case "down":
                v += n
            case "up":
                v -= n

    return h * v


def part_2(data):
    aim = 0
    v, h = 0, 0

    for (d, n) in data:
        match d:
            case "forward":
                h += n
                v += aim * n
            case "down":
                aim += n
            case "up":
                aim -= n

    return h * v


data = read_input()
print(part_1(data))
print(part_2(data))
