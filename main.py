from basics import *

if __name__ == "__main__":
    bullet = Massive((3, 35), Vector((3, 4)), Vector((0, -1)), 3)
    sq = Square((5.6, 10.5), 5)
    b = Board((52, 47), [bullet, sq])
    b.render(13)
    #print(sq.area)