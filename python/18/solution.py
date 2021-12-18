import sys

from functools import reduce
from itertools import combinations, takewhile
from typing import Iterator, List, Optional, Union

Data = Union[int, List["Data"]]


def parse_line(line) -> Data:
    return eval(line)


def read_input() -> List[Data]:
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


class Node:
    def __init__(
        self,
        value: Optional[int] = None,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
    ):
        self.left = left
        self.right = right
        self.value = value

    def is_value_pair(self) -> bool:
        return (
            self.left is not None
            and self.right is not None
            and self.left.value is not None
            and self.right.value is not None
        )

    def magnitude(self) -> int:
        if self.value is not None:
            return self.value
        assert self.left is not None and self.right is not None
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __repr__(self) -> str:
        if self.value is not None:
            return f"{self.value}"
        return f"[{self.left},{self.right}]"

    def __add__(self, other: "Node") -> "Node":
        return Node(None, self, other)

    def __iter__(self) -> Iterator["Node"]:
        if self.left:
            yield from self.left
        if self.right:
            yield from self.right
        yield self


def to_tree(data: Data) -> Node:
    if type(data) is int:
        return Node(data)
    assert type(data) is list
    node = Node(None)
    node.left = to_tree(data[0])
    node.right = to_tree(data[1])

    return node


def find_level_4_node(node: Node, level=4) -> Optional[List[Node]]:
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


def find_node_with_value_greater_than_10(node: Node) -> Optional[Node]:
    if node is None:
        return None
    if node.value and node.value >= 10:
        return node
    if node.left and (next := find_node_with_value_greater_than_10(node.left)):
        return next
    if node.right and (next := find_node_with_value_greater_than_10(node.right)):
        return next


def reduce_tree(root: Node) -> Node:
    reduced = True
    while reduced:
        reduced = False
        if path := find_level_4_node(root, 4):
            node = path[0]
            assert (
                node.left
                and node.right
                and node.left.value is not None
                and node.right.value is not None
            )
            left = node.left.value
            right = node.right.value

            node.left = None
            node.right = None
            node.value = 0

            left_nodes = list(reversed(list(takewhile(lambda n: n is not node, root))))
            right_nodes = list(
                reversed(list(takewhile(lambda n: n is not node, reversed(list(root)))))
            )

            for node in left_nodes:
                if node.value is not None:
                    node.value += left
                    break
            for node in right_nodes:
                if node.value is not None:
                    node.value += right
                    break

            reduced = True
        elif node := find_node_with_value_greater_than_10(root):
            assert node.value is not None
            value, r = divmod(node.value, 2)
            node.value = None

            node.left = Node(value)
            node.right = Node(value + r)
            reduced = True

    return root


def part_1(data: List[Data]) -> int:
    numbers = [to_tree(line) for line in data]

    return reduce(lambda a, b: reduce_tree(a + b), numbers).magnitude()


def part_2(data: List[Data]) -> int:
    return max(
        reduce_tree(to_tree(a) + to_tree(b)).magnitude()
        for a, b in combinations(data, 2)
    )


data = read_input()
print(part_1(data))
print(part_2(data))
