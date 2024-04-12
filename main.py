from basics import *

if __name__ == "__main__":
    bullet = Massive((3, 35), Vector((3, 4)), Vector((0, -1)), 3)
    a = Mobile((6.6, 7.3), Vector((3, 10.5)), Vector((-0.3, -1.5)))
    sq = Square((50, 43), 5)
    b = Board((52, 47), [bullet, sq, a])
    b.render(17, tracer=True)
    #print(sq.area)
