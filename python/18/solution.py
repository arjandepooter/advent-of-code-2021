import sys
from collections import *
from functools import *
from itertools import combinations, takewhile


class Node:
    def __init__(self, value, left=None, right=None):
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self) -> str:
        if self.value is not None:
            return f"{self.value}"
        return f"[{self.left},{self.right}]"

    def is_value_pair(self) -> bool:
        return (
            self.left is not None
            and self.right is not None
            and self.left.value is not None
            and self.right.value is not None
        )

    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __add__(self, other):
        return Node(None, self, other)


def parse_line(line):
    return eval(line)


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


def to_tree(data):
    if type(data) is int:
        return Node(data)

    node = Node(None)
    node.left = to_tree(data[0])
    node.right = to_tree(data[1])

    return node


def find_level_4_node(node, level=4):
    if level == 0:
        if node.is_value_pair():
            return [node]

        return None
    if node is None:
        return None
    if node.left and (next := find_level_4_node(node.left, level - 1)):
        return next + [node]
    if node.right and (next := find_level_4_node(node.right, level - 1)):
        return next + [node]


def find_node_with_value_greater_than_10(node):
    if node is None:
        return None
    if node.value and node.value >= 10:
        return node
    if node.left and (next := find_node_with_value_greater_than_10(node.left)):
        return next
    if node.right and (next := find_node_with_value_greater_than_10(node.right)):
        return next


def iter_tree(node):
    if node is None:
        return

    yield from iter_tree(node.left)
    yield from iter_tree(node.right)
    yield node


def reduce_step(data):
    if path := find_level_4_node(data, 4):
        node = path[0]
        left = node.left.value
        right = node.right.value

        node.left = None
        node.right = None
        node.value = 0

        left_nodes = list(
            reversed(list(takewhile(lambda n: n is not node, iter_tree(data))))
        )
        right_nodes = list(
            reversed(
                list(
                    takewhile(lambda n: n is not node, reversed(list(iter_tree(data))))
                )
            )
        )

        for node in left_nodes:
            if node.value is not None:
                node.value += left
                break
        for node in right_nodes:
            if node.value is not None:
                node.value += right
                break

        return True

    if node := find_node_with_value_greater_than_10(data):
        value, r = divmod(node.value, 2)
        node.value = None

        node.left = Node(value)
        node.right = Node(value + r)
        return True

    return False


def full_reduce(data):
    while reduce_step(data):
        pass
    return data


def part_1(data):
    numbers = [to_tree(line) for line in data]

    reduced = reduce(lambda a, b: full_reduce(a + b), numbers)

    return reduced.magnitude()


def part_2(data):
    acc = 0
    for a, b in combinations(data, 2):
        reduced = full_reduce(to_tree(a) + to_tree(b))
        acc = max(acc, reduced.magnitude())
    return acc


data = read_input()
print(part_1(data))
print(part_2(data))
