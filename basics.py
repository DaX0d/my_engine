from vector import Vector
import time
import os
import math

def custom_round(num: float) -> int:
    '''Возвращает округленное число (математически, а не как это делает стандартный Python)'''
    sign = 1 if num >= 0 else -1
    abs_num = abs(num)
    integer_part = int(abs_num)
    fractional_part = abs_num - integer_part
    rounded_fractional_part = math.floor(fractional_part) if fractional_part < 0.5 else math.ceil(fractional_part)
    if rounded_fractional_part == 1:
        integer_part += 1
    return sign * (integer_part + rounded_fractional_part)


class Board:
    '''Доска, на которой отображаются объекты.'''
    field: list[list]
    fill: str = " "

    def __init__(self, size: tuple[int, int], objects: list) -> None:
        self.size = size
        self.field = self._get_empty_field()
        self.objects = objects
    
    def _generate(self) -> None:
        '''Вызывает метод render у объекта из списка объектов на доске.'''
        for object in self.objects:
            object.render(self)

    def _get_empty_field(self) -> list[list]:
        '''Возвращает пустую доску'''
        return [[self.fill for x in range(self.size[0])] for y in range(self.size[1])]
    
    def collisions_check(self) -> None:
        '''Проверяет наличие столкновений объектов на доске'''
        for i in range(len(self.objects) - 1):
            for j in range(i+1, len(self.objects)):
                self.objects[i].collision_check(self.objects[j])

    def render(self, time_seconds: int, *, tracer=False) -> None:
        '''Выводит в коммандную строку изображение доски с указанной длительностью'''
        os.system("cls")
        if not tracer:
            self.field = self._get_empty_field()
        self._generate()
        self.collisions_check()
        for l in reversed(self.field):
            print(*l)
        if time_seconds != 1:
            time.sleep(0.2)
            self.render(time_seconds-1, tracer=tracer)


class VisableObject:
    '''ИНТЕРФЕЙС видимого объекта'''
    symbol: str
    def render(self, b: Board) -> None:
        '''Размещает изображение объекта на доске'''


class Mobile(VisableObject):
    '''Способная перемещаться легкая материальная точка'''
    position: tuple[float, float]
    speed: Vector
    acceleration: Vector
    symbol = "•"

    def __init__(self,
                 position: tuple[float, float],
                 speed: Vector,
                 acceleration: Vector) -> None:
        self.position, self.speed, self.acceleration = position, speed, acceleration

    def is_in_field(self, board: Board) -> bool:
        '''Проверка нахождения объекта в зоне видимости доски'''
        return all(0 <= self.position[n] < board.size[n] for n in range(2))

    def render(self, board: Board) -> None:
        if self.is_in_field(board):
            board.field[round(self.position[1])][round(self.position[0])] = self.symbol
        self.move()

    def _get_speed(self) -> Vector:
        '''Возвращает новую скорось объекта'''
        return self.speed + self.acceleration

    def _get_position(self) -> tuple[int, int]:
        '''Возвращает новую позицию объекта'''
        return tuple(self.position[n] + self.speed[n] + self.acceleration[n]/2 for n in range(2))
    
    def collision_check(self, object) -> None:
        match object.__class__.__name__:
            case "Mobile":
                if self.position == object.position:
                    self.speed, object.speed = object.speed, self.speed
                    return
            case "Massive":
                if self.position == object.position:
                    self.speed = -self.speed
                    return
        object.collision_check(self)
            
    
    def move(self) -> None:
        '''Перемещает объект'''
        self.position = self._get_position()
        self.speed = self._get_speed()
    
    def __str__(self) -> str:
        return f'''{self.__class__.__name__}(
    position: {self.position},
    speed: {self.speed},
    acceleration: {self.acceleration})\n'''
    

class Massive(Mobile):
    '''Перемещаемая массивная точка'''
    mass: float
    symbol = "○"
    impuls: Vector

    def __init__(self,
                 position: tuple[float, float],
                 speed: Vector,
                 acceleration: Vector,
                 mass: int) -> None:
        super().__init__(position, speed, acceleration)
        self.mass = mass
        self.impuls = self._get_impuls()

    def _get_impuls(self) -> Vector:
        '''Возвращает импульс объекта'''
        return self.speed * self.mass

    def move(self) -> None:
        super().move()
        self.impuls = self._get_impuls()

    def __str__(self) -> str:
        return f'''{self.__class__.__name__}(
    position: {self.position},
    speed: {self.speed},
    acceleration: {self.acceleration},
    mass: {self.mass},
    impuls: {self.impuls})\n'''


class Square(VisableObject):
    '''Статичный квадрат'''
    corner: tuple[float, float]
    size: int
    area: list[tuple[int, int]]
    symbol = "◙"

    def __init__(self, corner: tuple[float, float], size: int) -> None:
        self.corner, self.size = corner, size
        self.area = self._get_area()

    def _get_area(self) -> list[tuple[int, int]]:
        '''Возвращает точки простанства, занимаемые квадратом'''
        return [(x, y) for x in range(custom_round(self.corner[0]), custom_round(self.corner[0]+self.size))
                       for y in range(custom_round(self.corner[1]), custom_round(self.corner[1]+self.size))]
        
    def render(self, board: Board) -> None:
        for x, y in self.area:
            if self._is_in_board((x, y), board):
                board.field[y][x] = self.symbol
        
    def __eq__(self, value) -> bool:
        return self.center[0]-self.size/2 <= value.position[0] <= self.center[0]+self.size/2\
                and self.center[1]-self.size/2 <= value.position[1] <= self.center[1]+self.size/2
    
    def collision_check(self, object) -> None:
        match object.__class__.__name__:
            case "Massive":
                if object.position in self.area:
                    object.speed = Vector((-object.speed[0], object.speed[1]))
    
    @staticmethod
    def _is_in_board(coords: tuple[int, int], board: Board) -> bool:
        '''Проверка нахождения точки в зоне видимости доски'''
        return all(0 <= coords[n] < board.size[n] for n in range(2))


if __name__ == "__main__":
    pass
