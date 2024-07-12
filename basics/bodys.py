import math

from .board import Board
from .vector import Vector

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

def cos(v, b) -> float:
    '''Возвращает коситус между двумя векторами'''
    if (math.sqrt(v[0]**2 + v[1]**2) == 0) or (math.sqrt(b[0]**2 + b[1]**2) == 0):
        return 1
    return (v[0]*b[0] + v[1]*b[1]) / (math.sqrt(v[0]**2 + v[1]**2) * math.sqrt(b[0]**2 + b[1]**2))

def rnd_tpl(tpl: tuple[float, float]) -> tuple[int, int]:
    '''Принимает кортеж с двумя float, возыращает его с округленными значениями'''
    return (round(tpl[0]), round(tpl[1]))


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
        return all(0 <= round(self.position[n]) < board.size[n] for n in range(2))

    def _get_speed(self, FPS) -> Vector:
        '''Возвращает новую скорось объекта'''
        return self.speed + self.acceleration/FPS

    def _get_position(self, FPS) -> tuple[int, int]:
        '''Возвращает новую позицию объекта'''
        return tuple(self.position[n] + self.speed[n]/FPS + self.acceleration[n]/(2*FPS) for n in range(2))

    def _get_area(self) -> list[tuple[int, int]]:
        '''Возвращает плащадь, занимаемую объектом на доске'''
        return [(custom_round(self.position[0]), custom_round(self.position[1]))]

    def collision_check(self, obj) -> None:
        '''Проверяет наличие коллизии двух объектов и вызывает нужный метод для ее разрешения'''
        slf_cls_nm = self.__class__.__name__
        obj_cls_nm = obj.__class__.__name__
        if self.collision(obj):
            try:
                method = getattr(self, f'_resolve_{obj_cls_nm}')
                method(obj)
            except:
                try:
                    method = getattr(obj, f'_resolve_{slf_cls_nm}')
                    method(self)
                except:
                    raise AttributeError(f'Unable to collide {slf_cls_nm} and {obj_cls_nm}')
    
    def collision(self, obj) -> bool:
        '''Проверяет надичие коллизии между двумя объектами'''
        return self._get_area()[0] in obj._get_area()

    def _resolve_Mobile(self, obj) -> None:
        '''Разрешает коллизию с мобильным телом'''
        self.speed, obj.speed = obj.speed, self.speed

    def _resolve_Massive(self, obj) -> None:
        '''Разрашает коллизию с массивным телом'''
        if cos(self.speed, obj.speed) < 0:
            self.speed = -self.speed + obj.speed
        else:
            self.speed = self.speed + obj.speed
    
    def _resolve_Square(self, obj) -> None:
        '''Разрашает коллизию с квадратом'''
        obj._resolve_Mobile(self)

    def _resolve_MobileSquare(self, obj) -> None:
        '''Разрашает коллизию с подвижным квадратом'''
        obj._resolve_Mobile(self)

    def render(self, board: Board) -> None:
        if self.is_in_field(board):
            board.field[round(self.position[1])][round(self.position[0])] = self.symbol
        self.move(FPS=board.FPS)

    def move(self, FPS) -> None:
        '''Перемещает объект'''
        self.position = self._get_position(FPS)
        self.speed = self._get_speed(FPS)

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

    def _resolve_Mobile(self, obj) -> None:
        return obj._resolve_Massive(self)

    def _resolve_Massive(self, obj) -> None:
        m1, m2 = self.mass, obj.mass
        v1i, v2i = self.speed, obj.speed
        # Новые скорости после столкновения
        v1f = ((m1 - m2) * v1i + 2 * m2 * v2i) / (m1 + m2)
        v2f = ((m2 - m1) * v2i + 2 * m1 * v1i) / (m1 + m2)
        self.speed = v1f
        obj.speed = v2f

    def move(self, FPS) -> None:
        super().move(FPS)
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
    perimetr: dict[str, list[tuple[int, int]]]

    def __init__(self, corner: tuple[float, float], size: int) -> None:
        self.corner, self.size = corner, size
        self.area = self._get_area()
        self.perimetr = self._get_perimetr()

    def _get_area(self) -> list[tuple[int, int]]:
        '''Возвращает точки простанства, занимаемые квадратом'''
        return [(x, y) for x in range(custom_round(self.corner[0]), custom_round(self.corner[0]+self.size))
                       for y in range(custom_round(self.corner[1]), custom_round(self.corner[1]+self.size))]

    def _get_perimetr(self) -> dict[str, list[tuple[int, int]]]:
        '''Возвращает точки, находящиеся по периметру квадрата'''
        perimetr = {
            'corners': [rnd_tpl(self.corner), rnd_tpl((self.corner[0] + self.size-1, self.corner[1])),
                        rnd_tpl((self.corner[0], self.corner[1] + self.size-1)),
                        rnd_tpl((self.corner[0] + self.size-1, self.corner[1] + self.size-1))],
            'horizontal': ([rnd_tpl((self.corner[0] + n, self.corner[1] + self.size-1)) for n in range(self.size)] +
                            [rnd_tpl(((self.corner[0] + n, self.corner[1]))) for n in range(self.size)]),
            'verticals': ([rnd_tpl((self.corner[0] + self.size, self.corner[1] + n)) for n in range(self.size)] +
                                     [rnd_tpl((self.corner[0], self.corner[1] + n)) for n in range(self.size)])
        }
        return perimetr

    def collision_check(self, obj) -> None:
        '''Проверяет наличие коллизии двух объектов и вызывает нужный метод для ее разрешения'''
        slf_cls_nm = self.__class__.__name__
        obj_cls_nm = obj.__class__.__name__
        if self.collision(obj):
            try:
                method = getattr(self, f'_resolve_{obj_cls_nm}')
                method(obj)
            except:
                try:
                    method = getattr(obj, f'_resolve_{slf_cls_nm}')
                    method(self)
                except:
                    raise AttributeError(f'Unable to collide {slf_cls_nm} and {obj_cls_nm}')    
    
    def collision(self, obj) -> bool:
        return any([c in self.area for c in obj._get_area()])

    def _resolve_Mobile(self, obj) -> None:
        if obj.area[0] in self.perimetr['corners']:
            obj.speed = -obj.speed
        elif obj.area[0] in self.perimetr['horizontal']:
            obj.speed = Vector((obj.speed[0], -obj.speed[1]))
        elif obj.area[0] in self.perimetr['verticals']:
            obj.speed = Vector((-obj.speed[0], obj.speed[1]))

    def _resolve_Massive(self, obj) -> None:
        self._resolve_Mobile(obj)

    def render(self, board: Board) -> None:
        for x, y in self.area:
            if self._is_in_board((x, y), board):
                board.field[y][x] = self.symbol

    @staticmethod
    def _is_in_board(coords: tuple[int, int], board: Board) -> bool:
        '''Проверка нахождения точки в зоне видимости доски'''
        return all(0 <= coords[n] < board.size[n] for n in range(2))


class MobileSquare(Square, Mobile):
    '''Подвижный крадрат'''
    symbol = '#'

    def __init__(self, corner: tuple[float, float], size: int, speed: Vector, acceleration: Vector) -> None:
        self.corner, self.size = corner, size
        self.speed = speed
        self.acceleration = acceleration
        self.area = self._get_area()
        self.position = self.corner

    def _get_area(self) -> list[tuple[int, int]]:
        '''Возвращает точки простанства, занимаемые квадратом'''
        return [(x, y) for x in range(round(self.corner[0]), round(self.corner[0]+self.size))
                       for y in range(round(self.corner[1]), round(self.corner[1]+self.size))]

    def _resolve_Mobile(self, obj) -> None:
        return obj._resolve_MobileSquare(self)

    def render(self, board: Board) -> None:
        super().render(board)
        self.move(board.FPS)

    def move(self, FPS):
        super().move(FPS)
        self.corner = self.position
        self.area = self._get_area()
        self.perimetr = self._get_perimetr()


if __name__ == "__main__":
    pass
