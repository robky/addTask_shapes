from dataclasses import dataclass
from math import radians, sqrt, tan


class WrongFigureTypeError(Exception):

    def __init__(self, shape_type) -> None:
        self.shape_type = shape_type

    def __str__(self) -> str:
        return (f'Wrong the number of vertices to create the'
                f' {self.shape_type}')


class WrongFigureVerticesError(Exception):

    def __init__(self, shape_type) -> None:
        self.shape_type = shape_type

    def __str__(self) -> str:
        return (f'Not possible to create a {self.shape_type} on the '
                f'specified vertices')


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
        return self.x, self.y


class Shapes:
    """General class for shapes."""

    NUM_SIDES = 0
    side: float

    def __init__(self, *vertices: Vertices) -> None:
        self.vertices = vertices

        if self.NUM_SIDES != len(self.vertices):
            raise WrongFigureTypeError(self.__class__.__name__)
        self.check_correct()

    def get_side(self) -> float:
        """Get the size of the side by the minimum distance between the
        vertices."""
        vert_start = self.vertices[0]
        result = []
        for vert_stop in self.vertices[1:]:
            result.append(vert_start.get_distance(vert_stop))
        return min(result)

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

    def check_correct(self) -> bool:
        """The vertices must be different.
        All sides should be the same.
        All vertices must lie on the same circle."""        
        vert_list = [vert.get_tuple() for vert in self.vertices]
        if len(set(vert_list)) != len(self.vertices):            
            return False
        
        vert_start = self.vertices[0]
        result = []
        for vert_stop in self.vertices[1:]:
            result.append(vert_start.get_distance(vert_stop))
        min_side = min(result)
        temp_list = list(range(len(self.vertices)))
        work_list = []
        while len(temp_list) > 1:
            for i in temp_list[1:].copy():
                if (self.vertices[temp_list[0]].get_distance(self.vertices[i])
                    == min_side):
                    work_list.append(temp_list.pop(0))
                    break
            else:
                print('$$$$$$$$$$$$$$$$$$$')
                print(temp_list)
                print(work_list)
                return False
            
        print(temp_list)
        print(work_list)        
        

        
        # (x1, y1), (x2, y2), (x3, y3) = 
        # print('-----', x1, x2)
        return True


class Triangle(Shapes):

    NUM_SIDES = 3


class Pentagon(Shapes):

    NUM_SIDES = 5


def main() -> None:
    # Correct coordinates
    vt1 = Vertices(18, 2.01)
    vt2 = Vertices(16.26, -1.01)
    vt3 = Vertices(19.74, -1.01)
    t = Triangle(vt1, vt2, vt3)
    t2 = Triangle(vt2, vt1, vt3)
    print(t.get_info())
    print(t == t2)
    print(vt1)

    vp1 = Vertices(30, 2.01)
    vp2 = Vertices(31.91, 0.62)
    vp3 = Vertices(31.18, -1.63)
    vp4 = Vertices(28.82, -1.63)
    vp5 = Vertices(28.09, 0.62)
    p = Pentagon(vp1, vp2, vp3, vp4, vp5)
    p2 = Pentagon(vp3, vp3, vp1, vp4, vp2)
    print(p.get_info())
    print(p == p2)


if __name__ == '__main__':
    main()
