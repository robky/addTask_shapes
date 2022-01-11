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
        pass

    def compare(self) -> bool:
        """Compare shapes."""
        pass


def main() -> None:
    s = Shapes((2, 1), (6, 4))
    print(s.get_side())


if __name__ == '__main__':
    main()
