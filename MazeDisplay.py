'''
File: MazeDisplay.py
File Create: 24 Jun 2020
Author: Stephen Byers
-----
Graphically displaying maze and seeker movements

No Copyright 2020
'''

from array import *

#import tkinter as tk
from tkinter import * 
#from tk import Entry, Button, OptionMenu
from PIL import Image, ImageTk 
#import random
#import tkFileDialog
import tkinter.filedialog
#import os
import csv  #allow .csv file open/close and reading


class Square:
    ''' Individual tile/square within maze.  It is either open or part of wall.
        It tracks the row, column position within the matrix with a position
        tuple. '''
    def __init__(self, pos):
        self.mpos=pos
        self.mwall=1
        self.mvisited=False
        #print("{},{} ".format(pos[0],pos[1]),end="")
    def setWall(self,setting):
        self.mwall = setting
    def getWall(self):
        return self.mwall
    def visit(self):
        self.mvisited=True
    def getVisit(self):
        return self.mvisited

class Maze:
    def __init__(self,row,col):
        self.mrow = row
        self.mcol = col
        self.m = [[Square((r,c)) for c in range(col)] for r in range(row)]
    def getRows(self):
        return self.mrow 
    def getCols(self):
        return self.mcol
    def update(self,rows,cols):
        ''' Change the size of the maze matrix if needed.
            wipes the data from the array.'''
        if rows!=self.mrow or cols!=self.mcol:
            self.m.remove  # delete old array
            self.m = [[Square((r,c)) for c in range(cols)] for r in range(rows)]
            self.mrow = rows
            self.mcol = cols
            return True
        return False

    def read(self, fname):
        '''Read .csv file with matrix information.'''
        try:
            with open(fname) as csv_file:
                csv_reader = csv.reader(csv_file)
                # Determine size of new maze from num rows and elements in a line
                newRows =  sum(1 for line in csv_reader)
                csv_file.seek(0)
                line = csv_file.readline()
                tokens = line.split(",")
                newCols = len(tokens)
                # print("File: {} {},{} ".format(fname,newRows,newCols))
                # Adjust the maze according to new size if needed.
                self.update(newRows,newCols)
                
                csv_file.seek(0)    #reset the file reading point to beginning.
                r = 0  #row count
                for row in csv_reader:
                    c = 0  #column count
                    for s in row:
                        self.m[r][c].setWall(int(s))
                        # print("{}-{} ".format(s,self.m[r][c].getWall()),end="")
                        c += 1
                    r += 1
                    # print()

        except Exception as inst:
            print(inst)
        except:
            print("Couldn't open file: {}".format(fname))

    def write(self, fname):
        '''Write .csv file with matrix information.'''
        try:
            with open(fname, mode='w') as csv_file:  #end of with will close file.
                maze_writer = csv.writer(csv_file)
                row = [0 for i in range(self.mcol)]
                for r in range(self.mrow):      # loop through maze rows/cols
                    for c in range(self.mcol):
                        #print("{},{}-{} ".format(r,c,self.m[r][c].getWall()),end="")
                        row[c] = int(self.m[r][c].getWall())
                    #print(row)
                    maze_writer.writerow(row)
        except Exception as inst:
            print(inst)

class Seeker:  
    def __init__(self,maze):
        self.maze = maze
        self.seekMaze()

    def seekMaze(self):
        #find maze top opening to start
        for i in range(self.maze.getCols()):
            if not self.maze.m[0][i].getWall():
                cCol = i
                self.maze.m[0][i].visit()
        #self.maze.m[0][cCol]

        #loop until out of maze bottom
        h = self.maze.getRows()
        cRow = 0
        pr,pc = cRow, cCol
        while(cRow+1<h):
            cRow,cCol = self.calcNextMove(cRow,cCol)
            if pr==cRow and pc==cCol:
                cRow = h #exit loop
            pr,pc = cRow,cCol

    def calcNextMove(self,r,c):
        if r+1 < self.maze.getRows():
            if self.maze.m[r+1][c].getWall()==0 and self.maze.m[r+1][c].getWall()==0:  #Down, open down next row
                self.maze.m[r][c].visit()
                r += 1
                return r,c
        if c-1 > -1:
            if self.maze.m[r][c-1].getWall()==0 and self.maze.m[r][c-1].getVisit()==0:  # Left, not on left wall
                self.maze.m[r][c].visit()
                c -= 1
                return r,c
        if r-1 > -1:
            if self.maze.m[r-1][c].getWall()==0 and self.maze.m[r][c+1].getWall()!=0: # Up, not right avail, not on top edge
                self.maze.m[r][c].visit()
                return r,c
        if c+1 < self.maze.getCols():
            if self.maze.m[r][c+1].getWall() == 0: # Right, not on right edge
                self.maze.m[r][c].visit()
                c += 1
                return r,c
        return r,c 

class Tiles():
    def __init__(self,row,col):
        self.tiles = []
        self.row = row
        self.col = col

    def add(self,tile):
        self.tiles.append(tile)

    def show(self):
        for tile in self.tiles:
            tile.show()

class Tile(Label):
    def __init__(self,parent,pos,size,emptyimage,sq):
        Label.__init__(self,parent,width=size,height=size,bg='Black',image=emptyimage,relief='solid',compound='center')
        ''' Use empty image so labels are square and sized by pixels, whereas label widget is 
            normally sized to font character width and line height, if image present, then sized
            according to pixels.'''
        self.pos = pos
        self.sq = sq  # maze square
        self.i = emptyimage  # need to keep empty image from garbage collector, so can change config later.

        if sq.getWall()== 0:
            self.config(bg='White')
        self.bind('<Button-1>',self.mouseClick)

    def show(self):
        self.grid(row=self.pos[0],column = self.pos[1])

    def mouseClick(self,event):
        ''' Toggles whether square is part of wall or not '''
        if self.sq.getWall()==0:
            self.sq.setWall(1)
            self.config(bg='Black')
        else:
            self.sq.setWall(0)
            self.config(bg='White')

    def visited(self):
        #self.sq.getVisit():
        self.sq.visit()
        dotImg = PhotoImage(file="dot.png")  # dot image
        self.i = dotImg
        self.config(image=self.i)

class MazeFrame(Frame):
    MAX_DISPLAY_SIZE = 500
    def __init__(self, parent, maze, mainf, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        
        self.parent = parent
        self.mainf = mainf  # main object frame for callback of functions
        self.maze = maze
        self.tileSize = self.MAX_DISPLAY_SIZE/max(maze.getRows(),maze.getCols())
        self.mazeFrame = Frame(self)
        self.tiles = self.createTiles()
        self.tiles.show()
        self.mazeFrame.pack()
        # osx uses highlightbackground for button rather than bg option!
        #self.but=Button(self, text='Solve',command=self.mainf.restart,bd=10,highlightbackground='SlateGray3',width=20).pack(side='right',pady=5,padx=5) # place button below maze matrix
        self.but=Button(self, text='Solve',command=self.solve,bd=10,highlightbackground='SlateGray3',width=20) # place button below maze matrix
        self.but.pack(side='right',pady=5,padx=5)
        #self.bindKeys()

    def solve(self):
        self.seekr = Seeker(self.maze)
        self.tiles.show()
        self.but.configure(text='Restart', command=self.mainf.restart)

    def createTiles(self):
        rows = self.maze.getRows()
        cols = self.maze.getCols()
        tiles = Tiles(rows,cols)
        emptyimage= PhotoImage()  # empty image
        for row in range(rows):
            for col in range(cols):
                # x0 = col * self.tileSize
                # y0 = row * self.tileSize
                # x1 = x0 + self.tileSize
                # y1 = y0 + self.tileSize
                tile = Tile(self.mazeFrame,(row,col),self.tileSize,emptyimage,self.maze.m[row][col])
                # print("C{}".format(self.maze.m[row][col].getWall()),end=" ")
                tiles.add(tile)
            # print()
        return tiles

    def bindKeys(self):
        self.bind_all('<Key-Up>',self.flip)
        self.bind_all('<Key-Down>',self.flip)
        self.bind_all('<Key-Right>',self.flip)
        self.bind_all('<Key-Left>',self.flip)

    def flip(self):
        #self.tiles.flip(event.keysym)
        pass

class Main:
    def __init__(self,parent):
        self.parent = parent
        self.gridHt = IntVar()
        self.gridWt = IntVar()
        self.gridHt.set(10)     # default maze is 10x10 squares
        self.gridWt.set(10)
        self.mazeFile = StringVar()
        self.mazeFile.set("tmpmaze.csv")  #default maze informatino
        self.maze = Maze(self.gridHt.get(),self.gridWt.get())

        self.createWidgets()

    def createWidgets(self):
        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame,text='Select maze dimensions:', font=('',18)).pack(padx=10,pady=10)
        frame = Frame(self.mainFrame)
        Label(frame,text='Maze Height').grid(sticky = tkinter.W)
        Label(frame,text='Maze Width').grid(sticky = tkinter.W)
        OptionList = range(6,21,1)  # arbitary range for matrix
        OptionMenu(frame,self.gridHt,*OptionList).grid(row=0,column=1,padx=10,pady=10,sticky=tkinter.W)
        OptionMenu(frame,self.gridWt,*OptionList).grid(row=1,column=1,padx=10,pady=10,sticky=tkinter.W)
        Label(frame,text='Maze Data').grid(row=3,sticky = tkinter.W)        
        Entry(frame,textvariable=self.mazeFile,width=50).grid(row=3,column=1,padx=10,pady=2)
        Button(frame,text='Browse',command=self.browse).grid(row=3,column=2,padx=10,pady=2)
        frame.pack(padx=10,pady=10)

        Button(self.mainFrame, text='Write',command=self.writeMaze).pack(side=RIGHT,padx=10,pady=10)
        Button(self.mainFrame, text='Read',command=self.readMaze).pack(side=RIGHT,padx=10,pady=10)
        self.mainFrame.pack()       # show dialog


    def browse(self):
        self.mazeFile.set(tkinter.filedialog.askopenfilename(title="Maze Data File",filetypes=(("csv","*.csv"),("text File","*.txt"))))

    def restart(self):
        self.guiMaze.pack_forget()  # hid maze matrix
        self.mainFrame.pack()       # restart dialog

    def writeMaze(self):
        self.maze.update(self.gridHt.get(),self.gridWt.get())  # if dimensions changed, all maze data wiped out.
        self.maze.write(self.mazeFile.get())
        self.guiMaze = MazeFrame(self.parent,self.maze,self,background='SlateGray3')
        self.mainFrame.pack_forget()  # close dialog box
        self.guiMaze.pack()           # display tiles
    
    def readMaze(self):
        self.maze.read(self.mazeFile.get())
        self.gridHt.set(self.maze.getRows())
        self.gridWt.set(self.maze.getCols())
        self.guiMaze = MazeFrame(self.parent, self.maze,self,background='SlateGray3')
        self.mainFrame.pack_forget()  # close dialog box
        self.guiMaze.pack()           # display maze tiles


if __name__ == "__main__":
    root = Tk()
    root.title("Maze Display")
    Main(root)
    root.mainloop()

