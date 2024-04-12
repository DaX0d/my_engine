from basics import *

if __name__ == "__main__":
    bullet = Massive((3, 35), Vector((3, 4)), Vector((0, -1)), 3)
    b = Board((52, 47), [bullet])
    b.render(13, tracer=True)
    #print(sq.area)