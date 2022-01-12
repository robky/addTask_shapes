from math import sqrt
from typing import Tuple


class Shapes:
    """General class for shapes."""

    def __init__(self, *coordinates_vertices: Tuple[float, float]) -> None:
        self.coordinates_vertices = coordinates_vertices

    def get_side(self) -> float:
        """Get the side size."""
        (x1, y1), (x2, y2) = self.coordinates_vertices[:2]
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def get_area(self) -> float:
        """Get the area of the shape."""
        pass

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        raise NotImplementedError(f'Define get_perimetr in '
                                  f'{self.__class__.__name__}')

    def compare(self) -> bool:
        """Compare shapes."""
        pass


class Triangle(Shapes):

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        side_triangle = 3
        return self.get_side() * side_triangle


class Pentagon(Shapes):

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        side_pentagon = 5
        return self.get_side() * side_pentagon


def main() -> None:
    s = Shapes((2, 1), (6, 4))
    print(s.get_side())


if __name__ == '__main__':
    main()
