from basics.board import Board
from basics.bodys import Mobile, Square
from basics.vector import Vector
import math
# import logging
# logging.basicConfig(filename="debug.log", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    a = Square((50, 30), 10)
    a.symbol = 'a'
    b = Mobile((30, 50), Vector((5, 0)), Vector((0, -1)))
    b.symbol = 'b'
    board = Board((114, 64), [b, a])
    # board.fill = '-'
    try: 
        board.simulate(10, FPS=7, traser=False)
    except KeyboardInterrupt:
        print('Exiting...')
    # for i in range(70):
    #     b.move(7)
    #     if b.collision(a):
    #         print('Есть контакт!!!')
    #     else:
    #         print('(')

    # logging.debug(f"\na = {a}\n{a.__class__.__name__}\n")
    # logging.debug(f"\nb = {b}\n")

    # v = Vector((10, 0))
    # b = Vector((-10, 0))

    # print(cos(v, b))
