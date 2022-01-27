from abc import ABC
from dataclasses import dataclass
from math import radians, sqrt, tan
from typing import List, Tuple


class WrongFigureTypeError(Exception):
    def __str__(self) -> str:
        return 'Wrong the number of vertices to create a shape'


class WrongFigureVerticesError(Exception):
    def __str__(self) -> str:
        return 'Not possible to create a shape on the specified vertices'


@dataclass
class Vertices:
    """Class vertices of shapes"""

    x: float
    y: float

    def get_distance(self, other_vertices: 'Vertices') -> float:
        x1, y1 = self.x, self.y
        x2, y2 = other_vertices.x, other_vertices.y
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def __eq__(self, other) -> bool:
        """Compare vertices."""
        return self.x == other.x and self.y == other.y


class Shapes(ABC):
    """General abstract class for shapes."""

    def __init__(self, num_sides, side_length, *vertices: Vertices) -> None:
        self.num_sides = num_sides
        self.side_length = side_length
        self.vertices = vertices

    def get_area(self) -> float:
        """Get the area of the shape."""
        return ((((self.num_sides * (self.side_length ** 2)) / 4)
                * (1 / (tan(radians(180 / self.num_sides))))))

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        return self.side_length * self.num_sides

    def __str__(self) -> str:
        return self.NAME

    def get_info(self) -> str:
        """Return all values of shape"""

        return (f'Figure: {self.NAME},\n'
                f'Number of side: {self.num_sides},\n'
                f'Side length: {self.side_length},\n'
                f'Area: {self.get_area()},\n'
                f'Perimetr: {self.get_perimetr()}')

    def __eq__(self, other) -> bool:
        """Compare shapes."""
        if self.num_sides != other.num_sides:
            return False
        for vert in self.vertices:
            if vert not in other.vertices:
                return False
        return True


class Triangle(Shapes):
    """According to the assignment, Triangle should be the class."""

    NAME = 'Triangle'


class Pentagon(Shapes):
    """According to the assignment, Pentagon should be the class"""

    NAME = 'Pentagon'


class Creator():
    """Data validation and object creation"""

    NUM_ROUND = 1
    side_of_shape = {
        3: Triangle,
        5: Pentagon
    }
    vertices: Tuple[Vertices]
    num_sides: int
    side_length: float
    correct_order: list

    def get_object_or_error(self, *vertices: Tuple[Vertices]) -> Shapes:
        self.num_sides = len(vertices)

        if self.num_sides not in self.side_of_shape:
            raise WrongFigureTypeError()

        self.vertices = vertices
        self.side_length = self.get_side_length()

        if not self.is_possible_build_figure():
            raise WrongFigureVerticesError()

        return (self.side_of_shape[self.num_sides](self.num_sides,
                                                   self.side_length,
                                                   *self.vertices))

    def get_side_length(self) -> float:
        result = []
        vert_start = self.vertices[0]
        for vert_end in self.vertices[1:]:
            result.append(vert_start.get_distance(vert_end))
        return round(min(result), self.NUM_ROUND)

    def is_possible_build_figure(self) -> bool:
        if (self.is_vert_different()
                and self.is_vert_same()
                and self.is_distance_between_adjacent_equal()):
            return True
        return False

    def is_vert_different(self) -> bool:
        unique = []
        for vert in self.vertices:
            if vert not in unique:
                unique.append(vert)
        return len(unique) == len(self.vertices)

    def is_vert_same(self) -> bool:
        temp = list(range(1, self.num_sides))
        correct_order = [0]
        while len(temp):
            for i in temp.copy():
                if (round(self.vertices[correct_order[-1]].
                          get_distance(self.vertices[i]),
                          self.NUM_ROUND) == self.side_length):
                    correct_order.append(temp.pop(temp.index(i)))
                    break
            else:
                return False
        self.correct_order = correct_order
        return True

    def is_distance_between_adjacent_equal(self) -> bool:
        # The distance between adjacent vertices through one must be equal
        distance = []
        if self.num_sides % 2 == 0:
            distance = self.get_between_distance(self.correct_order[::2]
                                                 + [self.correct_order[0]])
            distance += self.get_between_distance(self.correct_order[1::2]
                                                  + [self.correct_order[1]])
        else:
            distance = self.get_between_distance(self.correct_order[::2]
                                                 + self.correct_order[1::2]
                                                 + [self.correct_order[0]])
        return len(set(distance)) == 1

    def get_between_distance(self, indexes_correct_order) -> list:
        result = []
        pre_i = indexes_correct_order[0]
        for i in indexes_correct_order[1:]:
            (result.append(round(
                self.vertices[pre_i].get_distance(self.vertices[i]),
                self.NUM_ROUND)))
            pre_i = i
        return result


def get_vertices(coordinates: List[tuple]):
    return map(lambda x: Vertices(*x), coordinates)


def action(*vertices: Vertices) -> Shapes:
    return Creator().get_object_or_error(*vertices)


def main() -> None:
    # Correct coordinates
    triangle = [(18, 2.01), (19.74, -1.01), (16.26, -1.01)]
    pentagon = [(31.18, -1.63), (31.91, 0.62), (28.82, -1.63), (30, 2.01),
                (28.09, 0.62)]

    t1 = action(*get_vertices(triangle))
    p1 = action(*get_vertices(pentagon))

    print(t1.get_info())
    print()
    print(p1.get_info())

    print(f'Compare t1 == p1: {t1 == p1}')
    pentagon = [(31.91, 0.62), (31.18, -1.63), (28.82, -1.63), (28.09, 0.62),
                (30, 2.01)]
    p2 = action(*get_vertices(pentagon))
    print(f'Compare p1 == p2: {p1 == p2}')


if __name__ == '__main__':
    main()
