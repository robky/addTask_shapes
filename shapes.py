from math import sqrt, sin, pi
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
        raise NotImplementedError(f'Define get_area in '
                                  f'{self.__class__.__name__}')

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        raise NotImplementedError(f'Define get_perimetr in '
                                  f'{self.__class__.__name__}')

    def compare(self) -> bool:
        """Compare shapes."""
        pass

    def get_info(self) -> str:
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
        triangle_hip = self.get_side() / (2 * sin(pi / 5))
        triangle_area = (1/2 * self.get_side() * sqrt(triangle_hip ** 2
                         - self.get_side() ** 2 / 4))
        return triangle_area * self.NUM_SIDES


def main() -> None:
    t = Triangle((2, 1), (6, 4), (4, 2))
    print(t.get_info())

    p = Pentagon((2, 1), (6, 4), (2, 1))
    print(p.get_info())


if __name__ == '__main__':
    main()
