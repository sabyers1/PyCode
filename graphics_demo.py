#graphics_demo.py
""" Simple program to experiment with graphic capbilities
    of the Tkinter package """

from graphics import *
import random

def main():
    win = GraphWin("Random Graphics Demo Window",500, 500)
    win.setBackground(color_rgb(255,255,255))
    for i in random.sample(range(50,450),10):
        pt = Point(i, random.randint(50,450))
        cir = Circle(pt, 20)
        cir.setFill(color='lightblue')
        cir.draw(win)
    t = Text(Point(100,350),"Important Information!")
    t.setSize(18)
    t.setFace('arial')
    t.setStyle('bold italic')
    t.setTextColor(color='red')
    t.draw(win)
    win.getMouse()
    win.close()

main()