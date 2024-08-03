from basics.board import Board
from basics.bodys import Mobile, Square, Massive, MobileSquare
from basics.vector import Vector

def main():
    a = MobileSquare((15, 20), 5, Vector((3, 0)), Vector((0, 0)))
    b = Massive((30, 23), Vector((1, 0)), Vector((0, 0)), 1)

    board = Board((115, 60), [a, b])
    # board.fill = '-'

    try:
        board.simulate(10, FPS=10, tracer=False)
    except KeyboardInterrupt:
        print('Exiting...')

if __name__ == "__main__":
    main()
