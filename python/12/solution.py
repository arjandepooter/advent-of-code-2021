import sys
from collections import defaultdict


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    edges = defaultdict(list)
    for line in lines:
        node1, node2 = line.split("-")
        edges[node1].append(node2)
        edges[node2].append(node1)
    return edges


def find_number_of_paths(
    data, current="start", visited=frozenset("start"), visited_small_twice=True
):
    if current == "end":
        return 1

    return sum(
        find_number_of_paths(
            data,
            n,
            visited | {current},
            visited_small_twice or n.islower() and n in visited,
        )
        for n in data.get(current, [])
        if n.isupper() or n not in visited or (not visited_small_twice and n != "start")
    )


def part_1(data):
    return find_number_of_paths(data)


def part_2(data):
    return find_number_of_paths(data, visited_small_twice=False)


data = read_input()
print(part_1(data))
print(part_2(data))
