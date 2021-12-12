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


def find_paths(data, current="start", visited=None, visited_small_twice=False):
    if visited is None:
        visited = {current}

    if current == "end":
        return 1

    acc = 0
    for n in data.get(current, []):
        new_visits = visited.copy()
        new_visits.add(n)

        if (
            n.isupper()
            or n not in visited
            or (not visited_small_twice and n != "start")
        ):
            acc += find_paths(
                data,
                n,
                new_visits,
                visited_small_twice or n.islower() and n in visited,
            )
    return acc


def part_1(data):
    return find_paths(data, visited_small_twice=True)


def part_2(data):
    return find_paths(data)


data = read_input()
print(part_1(data))
print(part_2(data))
