import sys

from functools import reduce
from itertools import combinations, takewhile, tee
from typing import Callable, Iterator, List, Optional, Tuple, Union

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

    def magnitude(self) -> int:
        if self.value is not None:
            return self.value
        assert self.left is not None and self.right is not None
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def reduce(self) -> "Node":
        reduced = True
        while reduced:
            reduced = False

            if node := self.find_node(
                lambda node, level: level == 4 and node.value is None
            ):
                self.explode(node)
                reduced = True
            elif node := self.find_node(
                lambda n, _: (n.value is not None) and n.value >= 10
            ):
                node.split()
                reduced = True

        return self

    def explode(self, node: "Node"):
        assert node.left and node.left.value is not None
        assert node.right and node.right.value is not None

        left, right = node.left.value, node.right.value
        node.left = node.right = None
        node.value = 0

        if left_node := next(self.left_value_nodes(node), None):
            assert left_node.value is not None
            left_node.value += left
        if right_node := next(self.right_value_nodes(node), None):
            assert right_node.value is not None
            right_node.value += right

    def split(self):
        assert self.value is not None
        value, r = divmod(self.value, 2)
        self.value = None

        self.left = Node(value)
        self.right = Node(value + r)

    def find_node(
        self, predicate: Callable[["Node", int], bool], level=0
    ) -> Optional["Node"]:
        if predicate(self, level):
            return self

        return (
            self.left
            and self.left.find_node(predicate, level + 1)
            or self.right
            and self.right.find_node(predicate, level + 1)
        )

    def left_value_nodes(self, node: "Node") -> Iterator["Node"]:
        return reversed(
            list(
                value_node
                for value_node in takewhile(lambda n: n is not node, self)
                if value_node.value is not None
            )
        )

    def right_value_nodes(self, node: "Node") -> Iterator["Node"]:

        return reversed(
            list(
                value_node
                for value_node in takewhile(
                    lambda n: n is not node, reversed(list(self))
                )
                if value_node.value is not None
            )
        )

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


def part_1(data: List[Data]) -> int:
    numbers = [to_tree(line) for line in data]

    return reduce(lambda a, b: (a + b).reduce(), numbers).magnitude()


def part_2(data: List[Data]) -> int:
    return max(
        (to_tree(number1) + to_tree(number2)).reduce().magnitude()
        for number1, number2 in combinations(data, 2)
    )


if __name__ == "__main__":
    data = read_input()
    print(part_1(data))
    print(part_2(data))
