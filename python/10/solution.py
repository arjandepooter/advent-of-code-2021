import sys
from functools import reduce


def parse_line(line):
    return line


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


CHUNKS = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}


def check_syntax(line):
    stack = []

    for c in line:
        if c in CHUNKS.values():
            stack.append(c)
        else:
            s = stack.pop()
            if s != CHUNKS[c]:
                return (stack, c)

    return (stack, None)


def part_1(data):
    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    acc = 0

    for line in data:
        _, mismatch = check_syntax(line)
        acc += scores.get(mismatch, 0)

    return acc


def part_2(data):
    scores = []
    order = ["(", "[", "{", "<"]

    for line in data:
        stack, mismatch = check_syntax(line)
        if mismatch is not None:
            continue

        score = reduce(
            lambda acc, c: (acc * 5) + order.index(c) + 1,
            reversed(stack),
            0,
        )
        scores.append(score)

    scores.sort()
    return scores[len(scores) // 2]


data = read_input()
print(part_1(data))
print(part_2(data))
