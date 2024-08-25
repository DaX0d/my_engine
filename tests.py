import time

from basics.board import Board
from basics.bodys import Mobile, Square, Massive, MobileRectangle, Rectangle, MobileSquare
from basics.vector import Vector

all_tests = []

def test(func):
    all_tests.append(func)
    return func


@test
def mobile_test():
    a = Mobile((30, 50), (3, 0))
    board = Board((115, 60), [a])
    board.simulate(10, tracer=True, FPS=10)

@test
def mobile_collision_test():
    a = Mobile((10, 10), (2, 0), (1, 0))
    b = Mobile((20, 10), (1, 0), (-1, 0))
    a.symbol = 'a'
    b.symbol = 'b'
    board = Board((115, 60), [a, b])
    board.simulate(10)

@test
def massive_test():
    a = Massive((10, 10), 3, (1, 5), (1, -1))
    board = Board((115, 60), [a])
    board.simulate(10)

@test
def massive_collisions_test():
    bodys = [
        Massive((10, 10), 5, (1, 0)),
        Massive((25, 10), 2, (-2, 0))
    ]
    bodys[0].symbol = 'a'
    bodys[1].symbol = 'b'
    board = Board((115, 60), bodys, debug=True)
    board.simulate(10)

@test
def square_test():
    a = Square((30, 14), 5)
    b = Massive((32, 5), 3, (0, 2))
    board = Board((115, 60), [a, b])
    board.simulate(10)

@test
def mobilerectangle_test():
    a = MobileRectangle((39, 30), (10, 7), (1, 5), (0, -1))
    board = Board((115, 60), [a])
    board.simulate(10)

@test
def mobilerectangle_collisions_test():
    a = MobileRectangle((20, 10), (10, 5), (4, 3))
    b = Mobile((55, 50), (-2, -1), (0, -1))
    board = Board((115, 60), [a, b])
    board.simulate(10, FPS=10)

@test
def mobilesquare_test():
    a = MobileSquare((20, 20), 5, (2, 3), (1, -1))
    board = Board((115, 60), [a])
    board.simulate(10)

@test
def print_time_test():
    text = 'aboba'
    start = time.time()
    print(text)
    end = time.time()
    print(end - start)

if __name__ == '__main__':
    try:
        print('Выберите тест:')
        for i in range(len(all_tests)):
            print(f'\t{i}: {all_tests[i].__name__}')
        running_test = all_tests[int(input('\n'))]
        running_test()
    except KeyboardInterrupt:
        print('Exiting...')
