from abc import ABC
from math import sqrt
from dataclasses import dataclass
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
    """Общий клас для фигур"""

    def __init__(self, *vertices: Vertices) -> None:
        self.vertices = vertices


class Triangle(Shapes):
    NUM_SIDES = 3


class Pentagon(Shapes):
    NUM_SIDES = 5


class Creator():
    """Валидация данных и создание объекта"""

    NUM_ROUND = 1
    side_of_shape = {
        3: Triangle,
        5: Pentagon
    }
    vertices: Vertices
    num_sides: int
    side_length: float
    correct_order: list

    def get_object_or_error(self, *vertices: Tuple[Vertices]) -> Shapes:
        self.num_sides = len(vertices)

        # Количество вершин должно соответствовать создаваемым фигурам
        if self.num_sides not in self.side_of_shape:
            raise WrongFigureTypeError()

        self.vertices = vertices
        self.side_length = self.get_side_length()
        
        # По заданным вершинам можно построить фигуру?
        if not self.is_possible_build_figure():
            raise WrongFigureVerticesError()

        return self.side_of_shape[self.num_sides](self.vertices)

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
        # Расстояние между соседними вершинами через одну должны быть равны
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
            #print(self.vertices[pre_i], self.vertices[i])
            #print(f'start: {pre_i}, stop{i} - {result}')

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


    #t = Triangle(vt1, vt2, vt3)
    #t2 = Triangle(vt2, vt1, vt3)
    #print(t1.get_info())
    print(t1)
    print(p1)
    #print(t == t2)
    #print()

    vp1 = Vertices(30, 2.01)
    vp2 = Vertices(31.91, 0.62)
    vp3 = Vertices(31.18, -1.63)
    vp4 = Vertices(28.82, -1.63)
    vp5 = Vertices(28.09, 0.62)
    #p = Pentagon(vp1, vp2, vp3, vp4, vp5)
    #p2 = Pentagon(vp5, vp3, vp1, vp4, vp2)
    #print(p.get_info())
    #print()
    #print(p == p2)
    #print(t == p)

    

if __name__ == '__main__':
    main()













'''from dataclasses import dataclass
from math import radians, sqrt, tan





class Shapes:
    """General class for shapes."""

    NUM_SIDES = 0
    NUM_ROUND = 1
    side: float

    def __init__(self, *vertices: Vertices) -> None:
        # Мне, честно признаться, не очень нравится идея валидировать данные в конструкторе
        # конструктор должен собрать объект из валидных данных. Но как в такой системе классов сделать красиво, сказать
        # пока не готов.
        # Пока видиться только превратить в абстрактный класс. См. модуль abc. И то, логику тогда придется поменять. Но
        # это поможеть избавить от NotImplementdError в этом классе и явно не даст создать объект с типом Shapes.
        self.vertices = vertices

        if self.NUM_SIDES != len(self.vertices):
            raise WrongFigureTypeError(self.__class__.__name__)

        if not self.check_correct():
            raise WrongFigureVerticesError(self.__class__.__name__)

    def get_side(self) -> float:
        """Get the size of the side by the minimum distance between the
        vertices."""

        # может быть стоит это превратить в property?
        return self.side

    def get_area(self) -> float:
        """Get the area of the shape."""
        # Данный метод занимается рассчетом площади. А расчет площади не занимается валидацией количества вершин.
        # Тут явно стоит изменить логику работы.
        if self.NUM_SIDES == 0:
            raise NotImplementedError(f'Define NUM_SIDES in '
                                      f'{self.__class__.__name__}')
        return (round((((self.NUM_SIDES * (self.get_side() ** 2)) / 4)
                * (1 / (tan(radians(180 / self.NUM_SIDES))))), self.NUM_ROUND))

    def get_perimetr(self) -> float:
        """Get the perimeter of the shape."""
        # См. предыдущий метод.
        if self.NUM_SIDES == 0:
            raise NotImplementedError(f'Define NUM_SIDES in '
                                      f'{self.__class__.__name__}')
        return self.get_side() * self.NUM_SIDES

    def __eq__(self, other) -> bool:
        """Compare shapes."""
        # В классе Vertices реализован ментод __eq__, но тут почему-то используем не его. Зачем он нужен тогда?
        # См. функцию zip, она поможет сделать все красиво
        return (set(vert.get_tuple() for vert in self.vertices)
                == set(vert.get_tuple() for vert in other.vertices))

    def get_info(self) -> str:
        """Return all values of shape"""
        # Тут все ок, но ИМХО type(self).__name__ более читаемо. Но применимы оба варианта, зависит от команды и
        # применяемого стиля кода в ней
        return (f'Figure: {self.__class__.__name__},\n'
                f'Side: {self.get_side()},\n'
                f'Area: {self.get_area()},\n'
                f'Perimetr: {self.get_perimetr()}')

    def check_correct(self) -> bool:
        """The vertices must be different.
        All sides should be the same.
        All vertices must lie on the same circle."""

        # Тут подвешу вопрос. Что вернет type(self.vertices) в классе Vertices? :)
        # Может можно избавиться от этих конверсий туда-сюда?
        vert_list = [vert.get_tuple() for vert in self.vertices]
        if len(set(vert_list)) != len(self.vertices):
            return False


        # Чисто математически, многоугольник правильный, если его стороны равны и углы между сторонами равны.
        # Сорри, глубоко не вникаю, что тут происходит.
        # В будущих проектах стоит давать более осмысленные имена переменным и изолировать логику в методах/функциях.
        # Причем, это могут быть вложенные функции.
        vert_start = self.vertices[0]
        result = []
        for vert_stop in self.vertices[1:]:
            result.append(round(vert_start.get_distance(vert_stop),
                          self.NUM_ROUND))
        min_side = min(result)
        temp_list = list(range(1, len(self.vertices)))
        work_list = [0]
        while len(temp_list):
            for i in temp_list.copy():
                if (round(self.vertices[work_list[-1]].
                          get_distance(self.vertices[i]), self.NUM_ROUND)
                        == min_side):
                    work_list.append(temp_list.pop(temp_list.index(i)))
                    break
            else:
                return False

        dist_list = []
        for gd in work_list:
            (dist_list.append(
             round(self.vertices[gd].get_distance(self.vertices[
                (gd + 2) % len(work_list)]), self.NUM_ROUND)))
        if len(set(dist_list)) > 1:
            return False

        self.side = min_side
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
    print()
    print(t == t2)
    print()

    vp1 = Vertices(30, 2.01)
    vp2 = Vertices(31.91, 0.62)
    vp3 = Vertices(31.18, -1.63)
    vp4 = Vertices(28.82, -1.63)
    vp5 = Vertices(28.09, 0.62)
    p = Pentagon(vp1, vp2, vp3, vp4, vp5)
    p2 = Pentagon(vp5, vp3, vp1, vp4, vp2)
    print(p.get_info())
    print()
    print(p == p2)
    print(t == p)


if __name__ == '__main__':
    main()
'''