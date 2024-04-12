from basics import *
import logging
logging.basicConfig(filename="debug.log", level=logging.DEBUG)

if __name__ == "__main__":
    a = Massive((20, 20), Vector((3, 0)), Vector((0, 0)), 1)
    a.symbol = "a"
    b = Mobile((28, 20), Vector((-5, 0)), Vector((0, 0)))
    b.symbol = "b"
    board = Board((52, 47), [a, b])
    board.render(10)
    logging.debug(f"\na = {a}\n{a.__class__.__name__}\n")
    logging.debug(f"\nb = {b}\n")
