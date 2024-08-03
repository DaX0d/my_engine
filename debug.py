from basics.board import Board
from basics.bodys import Mobile, Square, Massive, MobileSquare
from basics.vector import Vector

if __name__ == "__main__":
    a = MobileSquare((15, 20), 5, Vector((1, 0)), Vector((0, -1)))
    b = Massive((25, 35), Vector((0, -1)), Vector((0, 0)), 1)

    board = Board((114, 64), [a, b])
    board.FPS = 1

    for i in range(10):
        print(a.perimetr)
        a.move(1)

