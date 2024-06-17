from basics.board import Board
from basics.bodys import Mobile, Square, Massive, MobileSquare
from basics.vector import Vector
import math
# import logging
# logging.basicConfig(filename="debug.log", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    a = MobileSquare((20, 20), 5, Vector((1, 1)), Vector((0, 0)))
    # a.symbol = 'a'
    # b = Square((50, 30), 3)
    # b.symbol = 'b'
    board = Board((114, 64), [a])
    # board.fill = '-'
    try: 
        board.simulate(10, FPS=7, traser=False)
    except KeyboardInterrupt:
        print('Exiting...')

    # for i in range(3):
    #     print(b.area)
    #     print([b.area[c] for c in range(len(b.area)-1, 0, -b.size)] + [(b.corner[0] + n, b.corner[1]) for n in range(b.size)])
    #     print()
        # if b.collision(a):
        #     print('Есть контакт!!!')
        # else:
        #     print('(')

    # logging.debug(f"\na = {a}\n{a.__class__.__name__}\n")
    # logging.debug(f"\nb = {b}\n")

    # v = Vector((10, 0))
    # b = Vector((-10, 0))

    # print(cos(v, b))
