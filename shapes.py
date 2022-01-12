from dataclasses import dataclass
from math import radians, sqrt, tan


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

    def get_tuple(self) -> tuple:
        return (self.x, self.y)


class Shapes:
    """General class for shapes."""

    NUM_SIDES = 0

    def __init__(self, *vertices: Vertices) -> None:
        self.vertices = vertices

    def get_side(self) -> float:
        """Get the side size by the first two vertices."""
        return self.vertices[0].get_distance(self.vertices[1])

    def get_area(self) -> float:
        """Get the area of the shape."""
        if self.NUM_SIDES == 0:
            raise NotImplementedError(f'Define NUM_SIDES in '
                                      f'{self.__class__.__name__}')
        return (((self.NUM_SIDES * (self.get_side() ** 2)) / 4)
                * (1 / (tan(radians(180 / self.NUM_SIDES)))))

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        if self.NUM_SIDES == 0:
            raise NotImplementedError(f'Define NUM_SIDES in '
                                      f'{self.__class__.__name__}')
        return self.get_side() * self.NUM_SIDES

    def __eq__(self, other) -> bool:
        """Compare shapes."""
        return (set(vert.get_tuple() for vert in self.vertices)
                == set(vert.get_tuple() for vert in other.vertices))

    def get_info(self) -> str:
        """Return all values of shape"""
        return (f'Figure: {self.__class__.__name__},\n'
                f'Side: {self.get_side()},\n'
                f'Area: {self.get_area()},\n'
                f'Perimetr: {self.get_perimetr()}')


class Triangle(Shapes):

    NUM_SIDES = 3


class Pentagon(Shapes):

    NUM_SIDES = 5


def main() -> None:

    vt1 = Vertices(6, 4)
    vt2 = Vertices(2, 1)
    vt3 = Vertices(4, 2)
    t = Triangle(vt1, vt2, vt3)
    t2 = Triangle(vt2, vt1, vt3)
    p = Pentagon(vt1, vt2)
    print(t.get_info())
    print(t == t2)
    print(vt1)
    print(p.get_info())


if __name__ == '__main__':
    main()
