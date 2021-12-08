import sys


def parse_line(line):
    parts = line.split(" | ")
    return list(parts[0].split(" ")), list(parts[1].split(" "))


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


# unique mapping between (number_of_segments, overlap with 1, overlap with 4, overlap with 7)
OVERLAPS = {
    (6, 2, 3, 3): 0,
    (5, 1, 2, 2): 2,
    (5, 2, 3, 3): 3,
    (5, 1, 3, 2): 5,
    (6, 1, 3, 2): 6,
    (6, 2, 4, 3): 9,
}

KNOWN_LENGTHS = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}


def decode_line(signals, outs):
    known = {
        KNOWN_LENGTHS[len(signal)]: signal
        for signal in signals
        if len(signal) in KNOWN_LENGTHS
    }

    for signal in signals:
        if len(signal) not in (2, 3, 4, 7):
            overlaps = (len(signal),) + tuple(
                len(set(known[n]) & set(signal)) for n in (1, 4, 7)
            )
            known[OVERLAPS[overlaps]] = signal

    acc = 0
    for out in outs:
        for d, signal in known.items():
            if set(signal) == set(out):
                acc *= 10
                acc += d
    return acc


def part_1(data):
    acc = 0
    for _, out in data:
        for n in out:
            if len(n) in KNOWN_LENGTHS:
                acc += 1
    return acc


def part_2(data):
    return sum(decode_line(signal, out) for (signal, out) in data)


data = read_input()
print(f"Part 1: {part_1(data)}")
print(f"Part 2: {part_2(data)}")
