import time

from basics.board import Board
from basics.bodys import Mobile, Square, Massive, MobileSquare, Rectangle
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


ALL_TESTS = [square_test, mobile_test]


if __name__ == '__main__':
    try:
        print('Выберите тест:')
        for i in range(len(ALL_TESTS)):
            print(f'\t{i}: {ALL_TESTS[i].__name__}')
        running_test = ALL_TESTS[int(input('\n'))]
        running_test()
    except KeyboardInterrupt:
        print('Exiting...')
