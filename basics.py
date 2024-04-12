from vector import Vector
import time
import os
import math

def custom_round(num):
    sign = 1 if num >= 0 else -1
    abs_num = abs(num)
    integer_part = int(abs_num)
    fractional_part = abs_num - integer_part
    rounded_fractional_part = math.floor(fractional_part) if fractional_part < 0.5 else math.ceil(fractional_part)
    if rounded_fractional_part == 1:
        integer_part += 1
    return sign * (integer_part + rounded_fractional_part)


class Board:
    field: list[list]
    fill: str = " "

    def __init__(self, size: tuple[int, int], objects: list) -> None:
        self.size = size
        self.field = self._get_empty_field()
        self.objects = objects
    
    def _generate(self) -> None:
        for object in self.objects:
            object.render(self)

    def _get_empty_field(self) -> list[list]:
        return [[self.fill for x in range(self.size[0])] for y in range(self.size[1])]

    def render(self, time_seconds: int, *, tracer=False) -> None:
        os.system("cls")
        if not tracer:
            self.field = self._get_empty_field()
        self._generate()
        for l in reversed(self.field):
            print(*l)
        if time_seconds != 1:
            time.sleep(0.2)
            self.render(time_seconds-1, tracer=tracer)


class VisableObject:
    symbol: str
    def render(self, b: Board) -> None:
        pass


class Mobile(VisableObject):
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
        return all(0 <= self.position[n] < board.size[n] for n in range(2))

    def render(self, board: Board) -> None:
        if self.is_in_field(board):
            board.field[round(self.position[1])][round(self.position[0])] = self.symbol
        self.move()

    def _get_speed(self) -> Vector:
        return self.speed + self.acceleration

    def _get_position(self) -> tuple[int, int]:
        return tuple(self.position[n] + self.speed[n] + self.acceleration[n]/2 for n in range(2))
    
    def move(self) -> None:
        self.position = self._get_position()
        self.speed = self._get_speed()
    
    def __str__(self) -> str:
        return f'''{self.__class__.__name__}(
    position: {self.position},
    speed: {self.speed},
    acceleration: {self.acceleration})'''
    

class Massive(Mobile):
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
    impuls: {self.impuls})'''


class Square(VisableObject):
    corner: tuple[float, float]
    size: int
    area: list[tuple[int, int]]
    symbol = "◙"

    def __init__(self, corner: tuple[float, float], size: int) -> None:
        self.corner, self.size = corner, size
        self._get_area()

    def _get_area(self) -> None:
        self.area = [(x, y) for x in range(custom_round(self.corner[0]), custom_round(self.corner[0]+self.size))
                            for y in range(custom_round(self.corner[1]), custom_round(self.corner[1]+self.size))]
        
    def render(self, board: Board) -> None:
        for x, y in self.area:
            if self._is_in_board((x, y), board):
                board.field[y][x] = self.symbol
        
    def __eq__(self, value) -> bool:
        return self.center[0]-self.size/2 <= value.position[0] <= self.center[0]+self.size/2\
                and self.center[1]-self.size/2 <= value.position[1] <= self.center[1]+self.size/2
    
    @staticmethod
    def _is_in_board(coords: tuple[int, int], board: Board) -> bool:
        return all(0 <= coords[n] < board.size[n] for n in range(2))


if __name__ == "__main__":
    l = {
        "speed": Vector((1, 2)),
        "position": (0, 0),
        "acceleration": Vector((0, -1)),
        "mass": 10
    }
    a = Massive(**l)
    print(a)
    for i in range(4):
        a.move()
        print(a)
