from basics.board import Board
from basics.bodys import Mobile, Square, Massive, MobileSquare
from basics.vector import Vector

if __name__ == "__main__":
    a = MobileSquare((15, 20), 8, Vector((1, 0)), Vector((0, 0)))
    b = Massive((25, 40), Vector((0, -2)), Vector((0, 0)), 1)

    board = Board((114, 64), [a, b])

    try:
        board.simulate(10, FPS=10, tracer=False)
    except KeyboardInterrupt:
        print('Exiting...')
