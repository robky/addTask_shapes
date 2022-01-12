from dataclasses import dataclass
from math import sqrt, sin, pi
from typing import Tuple

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


class Shapes:
    """General class for shapes."""

    def __init__(self, *vertices: Tuple[Vertices]) -> None:
        self.vertices = vertices

    def get_side(self) -> float:
        """Get the side size."""
        return self.vertices[0].get_distance(self.vertices[1])

    def get_area(self) -> float:
        """Get the area of the shape."""
        raise NotImplementedError(f'Define get_area in '
                                  f'{self.__class__.__name__}')

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        raise NotImplementedError(f'Define get_perimetr in '
                                  f'{self.__class__.__name__}')

    def __eq__(self, other) -> bool:
        """Compare shapes."""
        return set(self.vertices) == set(other.vertices)

    def get_info(self) -> str:
        """Return all values of shape"""
        return (f'Figure: {self.__class__.__name__},\n'
                f'Side: {self.get_side()},\n'
                f'Area: {self.get_area()},\n'
                f'Perimetr: {self.get_perimetr()}')


class Triangle(Shapes):

    NUM_SIDES = 3

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        return self.get_side() * self.NUM_SIDES

    def get_area(self) -> float:
        """Get the area of the shape."""
        coefficient_area = sqrt(3) / 4
        return coefficient_area * self.get_side() ** 2


class Pentagon(Shapes):

    NUM_SIDES = 5

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        return self.get_side() * self.NUM_SIDES

    def get_area(self) -> float:
        """Get the area of the shape."""
        side = self.get_side()
        triangle_hip = side / (2 * sin(pi / 5))
        triangle_area = 1/2 * side * sqrt(triangle_hip ** 2 - side ** 2 / 4)
        return triangle_area * self.NUM_SIDES


def main() -> None:
    '''t = Triangle((2, 1), (6, 4), (4, 2))
    print(t.get_info())

    p = Pentagon((2, 1), (6, 4), (2, 1))
    print(p.get_info())

    t2 = Triangle((6, 4), (2, 1), (4, 2))
    print(t == t2)'''

    vt1 = Vertices(6, 4)
    vt2 = Vertices(2, 1)
    vt3 = Vertices(4, 2)
    t = Triangle(vt1, vt2, vt3)
    t2 = Triangle(vt2, vt1, vt3)
    print(t.get_info())
    #print(t == t2)


if __name__ == '__main__':
    main()
