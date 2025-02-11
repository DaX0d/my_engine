import time
import os


class Board:
    '''Доска, на которой отображаются объекты.'''
    field: list[list]
    fill: str = " "
    FPS = 5
    tracer = False
    debug = False

    def __init__(self, size: tuple[int, int], objects: list, *, debug = False) -> None:
        self.size = size
        self.field = self._get_empty_field()
        self.objects = objects
        self.debug = debug
    
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

    def render(self) -> None:
        '''Выводит в коммандную строку изображение доски'''
        if not self.debug:
            os.system('cls' if os.name == 'nt' else 'clear')
        if not self.tracer:
            self.field = self._get_empty_field()
        self.collisions_check()
        self._generate()
        if self.debug:
            for obj in self.objects:
                print(obj)
        else:
            for l in reversed(self.field):
                print(*l)
        time.sleep(1/self.FPS)

    def simulate(self, time_seconds: int, *, tracer: bool = False, FPS: int = 5) -> None:
        '''Симуляция доски в реальном времени'''
        self.FPS, self.tracer = FPS, tracer
        start_time = time.time()
        for i in range(time_seconds * self.FPS):
            self.render()
        end_time = time.time()
        if self.debug:
            print(end_time - start_time)


if __name__ == '__main__':
    pass
