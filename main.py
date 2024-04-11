from basics import *

if __name__ == "__main__":
    p = Mobile((2, 25), Vector((-3, 1)), Vector((2, -1)))
    mp = Massive((20, 29), Vector((-1, 0)), Vector((0, -1)), 10)
    sq = Square((25, 23), 5)
    b = Board((52, 47), [mp, p, sq])
    b.render(8)
    print(type(mp.impuls))