from basics import *
import math
# import logging
# logging.basicConfig(filename="debug.log", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    a = Massive((5, 20), Vector((5, 0)), Vector((0, 0)), 5)
    a.symbol = 'a'
    b = Massive((15, 20), Vector((2, 0)), Vector((0, 0)), 5)
    b.symbol = 'b'
    board = Board((52, 47), [a, b])
    try: 
        board.simulate(10, FPS=7)
    except KeyboardInterrupt:
        print('Exiting...')
    # logging.debug(f"\na = {a}\n{a.__class__.__name__}\n")
    # logging.debug(f"\nb = {b}\n")

    # v = Vector((10, 0))
    # b = Vector((-10, 0))

    # print(cos(v, b))