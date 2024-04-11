from vector import Vector
import time
import os


class Board:
    field: list[list]
    fill: str = " "

    def __init__(self, size: tuple[int, int], objects: list) -> None:
        self.size = size
        self.field = [[self.fill for x in range(size[0])] for y in range(size[1])]
        self.objects = objects
    
    def _generate(self) -> None:
        for object in self.objects:
            object.render(self)

    def render(self, time_seconds: int, *, tracer=False) -> None:
        os.system("cls")
        if not tracer:
            self.field = [[self.fill for x in range(self.size[0])] for y in range(self.size[1])]
        self._generate()
        for l in reversed(self.field): print(*l)
        if time_seconds != 1:
            time.sleep(1)
            self.render(time_seconds-1, tracer=tracer)


class VisableObject:
    symbol: str
    def render(self, b: Board) -> None:
        pass


class Mobile(VisableObject):
    position: tuple[int, int]
    speed: Vector
    acceleration: Vector
    symbol = "•"

    def __init__(self,
                 position: tuple[int, int],
                 speed: Vector,
                 acceleration: Vector) -> None:
        self.position, self.speed, self.acceleration = position, speed, acceleration

    def render(self, b: Board):
        b.field[int(self.position[1])][int(self.position[0])] = self.symbol
        self.move()

    def _get_speed(self) -> Vector:
        return self.speed + self.acceleration

    def _get_position(self) -> tuple[int, int]:
        return tuple(self.position[n] + self.speed[n] + self.acceleration[n]//2 for n in range(2))
    
    def move(self) -> None:
        self.position = self._get_position()
        self.speed = self._get_speed()

    def __str__(self) -> str:
        return f'''Mobile(
    position: {self.position},
    speed: {self.speed},
    acceleration: {self.acceleration})'''
    

class Massive(Mobile):
    mass: float
    symbol = "○"

    def __init__(self,
                 position: tuple[int, int],
                 speed: Vector,
                 acceleration: Vector,
                 mass: int) -> None:
        super().__init__(position, speed, acceleration)
        self.mass = mass

    def __str__(self) -> str:
        return f'''Massive(
    position: {self.position},
    speed: {self.speed},
    acceleration: {self.acceleration},
    mass: {self.mass})'''


class Square(VisableObject):
    center: tuple[int, int]
    size: int
    area: list[tuple[int, int]]
    symbol = "◙"

    def __init__(self, center: tuple[int, int], size: int) -> None:
        self.center, self.size = center, size
        self._get_area()

    def _get_area(self) -> None:
        self.area = [(x, y) for x in range(self.center[0]-self.size//2, self.center[0]+self.size//2)
                            for y in range(self.center[1]-self.size//2, self.center[1]+self.size//2)]
        
    def render(self, b: Board):
        for x, y in self.area:
            b.field[y][x] = self.symbol

    def move(self):
        pass
        
    def __eq__(self, value) -> bool:
        return self.center[0]-self.size/2 <= value.position[0] <= self.center[0]+self.size/2\
                and self.center[1]-self.size/2 <= value.position[1] <= self.center[1]+self.size/2


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
