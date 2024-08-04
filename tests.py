import time

from basics.board import Board
from basics.bodys import Mobile, Square, Massive, MobileRectangle, Rectangle, MobileSquare
from basics.vector import Vector


def square_test():
    a = Square((30, 14), 5)
    b = Massive((32, 5), 3, (0, 2))
    board = Board((115, 60), [a, b])
    board.simulate(10)

def mobile_test():
    a = Mobile((30, 50), (3, 0))
    board = Board((115, 60), [a])
    board.simulate(10, tracer=True, FPS=10)

def mobilerectangle_test():
    a = MobileRectangle((39, 30), (10, 7), (1, 5), (0, -1))
    board = Board((115, 60), [a])
    board.simulate(10)

def mobilerectangle_collisions_test():
    a = MobileRectangle((20, 10), (10, 5), (4, 3))
    b = Mobile((55, 50), (-2, -1), (0, -1))
    board = Board((115, 60), [a, b])
    board.simulate(10, FPS=10)

def mobilesquare_test():
    a = MobileSquare((20, 20), 5, (2, 3), (1, -1))
    board = Board((115, 60), [a])
    board.simulate(10)

#==========================================================================================================
ALL_TESTS = [
    square_test,
    mobile_test,
    mobilerectangle_test,
    mobilerectangle_collisions_test,
    mobilesquare_test
]
#==========================================================================================================

if __name__ == '__main__':
    try:
        print('Выберите тест:')
        for i in range(len(ALL_TESTS)):
            print(f'\t{i}: {ALL_TESTS[i].__name__}')
        running_test = ALL_TESTS[int(input('\n'))]
        running_test()
    except KeyboardInterrupt:
        print('Exiting...')
