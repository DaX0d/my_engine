from basics import *
import logging
logging.basicConfig(filename="debug.log", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    a = Massive((20, 20), Vector((1, 1)), Vector((0, 0)), 1)
    a.symbol = "a"
    b = Square((28, 20), 10)
    board = Board((52, 47), [a, b])
    board.render(15)
    #logging.debug(f"\na = {a}\n{a.__class__.__name__}\n")
    #logging.debug(f"\nb = {b}\n")
