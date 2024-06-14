from basics import *
# import logging
# logging.basicConfig(filename="debug.log", format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    a = Massive((20, 20), Vector((2, 0)), Vector((0, 0)), 1)
    a.symbol = 'a'
    b = Massive((34, 20), Vector((-1, 0)), Vector((0, 0)), 3)
    b.symbol = 'b'
    board = Board((52, 47), [a, b])
    try: 
        board.simulate(10)
    except KeyboardInterrupt:
        print('Exiting...')
    # logging.debug(f"\na = {a}\n{a.__class__.__name__}\n")
    # logging.debug(f"\nb = {b}\n")
