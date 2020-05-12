'''
File: slideGUI.py
File Create: 29th Sep 2017
Author:Sahal Mohamed motiQ
-----
 Excerise to make graphical respresentation of slider game
 taken from: https://www.youtube.com/watch?v=vzzEP_YI424
 
-----
Last Modified: 8th May 2020 9:57:28 pm
Modified By: Stephen Byers
-----
No Copyright 2020
'''
#import tkinter as tk
from tkinter import * 
#from tk import Entry, Button, OptionMen
from PIL import Image, ImageTk 
import random
#import tkFileDialog
import tkinter.filedialog
import os

class Tiles():
    def __init__(self,grid):
        self.tiles = []
        self.grid = grid
        self.gap = None
        self.moves = 0

    def add(self,tile):
        self.tiles.append(tile)

    def getTile(self,pos):          #*pos or pos? video uses pointer *!!! has to do with passing (()) or ()
        #print("Tiles::getTile {} {}".format(pos[0],pos[1]))
        for tile in self.tiles:
            if tile.pos == pos:
                return tile
        return None                 #didn't find tile, added not sure if needed

    def getTileAroundGap(self):
        gRow,gCol = self.gap.pos
        return self.getTile((gRow,gCol-1)),self.getTile((gRow-1,gCol)),self.getTile((gRow,gCol+1)),self.getTile((gRow+1,gCol))

    def changeGap(self,tile):
        try:
            gPos = self.gap.pos
            self.gap.pos = tile.pos
            tile.pos = gPos
            self.moves += 1
            #print("ChangeGap position from: {},{} to {},{} Moves: {}"
            #    .format(self.gap.pos[0],self.gap.pos[1],tile.pos[0],tile.pos[1],self.moves))
        except:
            pass

    def slide(self,key):
        left,top,right,down = self.getTileAroundGap()
        print("Tiles::slide w key: {}".format(key))
        if key == 'Up':
            self.changeGap(down)
        if key == 'Down':
            self.changeGap(top)
        if key == 'Right':
            self.changeGap(left)
        if key == 'Left':
            self.changeGap(right)
        self.show()

    def shuffle(self):
        random.shuffle(self.tiles)
        i = 0
        for row in range(self.grid):
            for col in range(self.grid):
                self.tiles[i].pos = (row,col)
                i+=1
        
    def show(self):
        for tile in self.tiles:
            if self.gap != tile:
                tile.show()
        
    def setGap(self,index):
        self.gap = self.tiles[index]

    def isCorrect(self):
        for tile in self.tiles:
            if not tile.isCorrectPos():
                return False
        return True

class Tile(Label):
    def __init__(self,parent,image,pos):
        Label.__init__(self,parent,image=image) 

        self.image = image
        self.pos = pos
        self.curPos = pos

    def show(self):
        self.grid(row=self.pos[0],column = self.pos[1])

    def isCorrectPos(self):
        return self.pos == self.curPos

class Board(Frame):
    MAX_BOARD_SIZE = 500
    def __init__(self,parent,image,grid,win,*args,**kwargs):
        Frame.__init__(self,parent,*args,**kwargs)

        self.parent = parent
        self.grid = grid
        self.win = win
        self.image = self.openImage(image)
        self.tileSize = self.image.size[0]/self.grid 
        self.tiles = self.createTiles()
        self.tiles.shuffle()
        self.tiles.show()
        self.bindKeys()
        self.moves = 0

   
    def openImage(self,image):
        #image = Image.open(image)
        #sImageName = image.get()        #TkImage requires string not StrVar???
        #print("openImage file: {}".format(sImageName))
        image = Image.open(image)
        #print("image size: {} x {}".format(image.size[0],image.size[1]))
        if min(image.size) > self.MAX_BOARD_SIZE:
            image = image.resize((self.MAX_BOARD_SIZE,self.MAX_BOARD_SIZE),Image.ANTIALIAS)
        if image.size[0] != image.size[1]:
            image = image.crop((0,0,image.size[0],image.size[0])) #square up tile image
        return image

    def bindKeys(self):
        self.bind_all('<Key-Up>',self.slide)
        self.bind_all('<Key-Down>',self.slide)
        self.bind_all('<Key-Right>',self.slide)
        self.bind_all('<Key-Left>',self.slide)
        self.bind_all('<Button-1>',self.slide)

    def slide(self,event):
        self.tiles.slide(event.keysym)
        #print("Board::slide event captured")
        if self.tiles.isCorrect():         #video shows self.tile.isCorrect
            self.win(self.tiles.moves)

    def createTiles(self):
        tiles = Tiles(self.grid)
        for row in range(self.grid):
            for col in range(self.grid):
                x0 = col * self.tileSize
                y0 = row * self.tileSize
                x1 = x0 + self.tileSize
                y1 = y0 + self.tileSize
                tileImage = ImageTk.PhotoImage(self.image.crop((x0,y0,x1,y1)))
                tile = Tile(self,tileImage,(row,col))
                tiles.add(tile)
        tiles.setGap(-1)  # gap is last tile in tile list
        return tiles

class Main():
    def __init__(self,parent):
        self.parent = parent

        self.image = StringVar()
        self.winText = StringVar()
        self.grid = IntVar()
        self.grid.set(3)            #default grid set to 4x4
        #self.image.set("GridPanel.png")  #default image for now.
        self.image.set("dice.jpg")  #default image for now.

        self.createWidgets()

    def createWidgets(self):
        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame,text='Select Sliding Puzzle Image:', font = ('',18)).pack(padx=10,pady=10)
        frame = Frame(self.mainFrame)
        Label(frame,text='Image').grid(sticky = tkinter.W)
        Entry(frame,textvariable = self.image,width=50).grid(row=0,column=1,padx=10,pady=2)
        Button(frame,text='Browse',command=self.browse).grid(row=0,column=2,padx=10,pady=2)
        Label(frame,text='Grid').grid(sticky = tkinter.W)
        OptionMenu(frame,self.grid,*[3,4,5,6,7,8,9,10]).grid(row=1,column=1,padx=10,pady=10,sticky = tkinter.W)
        frame.pack(padx=10,pady=10)
        Button(self.mainFrame,text='Start',command=self.start).pack(padx=10,pady=10)
        self.mainFrame.pack()
        self.board = Frame(self.parent)
        self.winFrame = Frame(self.parent)
        Label(self.winFrame,textvariable=self.winText,font=('',50)).pack(padx=10,pady=10)
        Button(self.winFrame,text='Play Again',command = self.playAgain).pack(padx=10,pady=10)

    def start(self):
        image = self.image.get()
        grid = self.grid.get()  #grid is just integer in this point
        if os.path.exists(image):
            self.board = Board(self.parent,image,grid,self.win)
            self.mainFrame.pack_forget()
            self.board.pack()

    def browse(self):
        self.image.set(tkinter.filedialog.askopenfilename(title="Select Image",filetypes=(("png File","*.png"),("jpg File","*.jpg"))))

    def win(self, moves):
        self.board.pack_forget()
        self.winText.set('You are winner (with {0} moves)'.format(moves))
        self.winFrame.pack()

    def playAgain(self):
        self.winFrame.pack_forget()
        self.mainFrame.pack()


# back = tk.Frame(master=root, bg='grey')
# back.pack_propagate(0)  #Don't allow widgets to determine frames width/height
# back.pack(fill=tk.BOTH, expand=1)  #Expand the frame to fill the root window
# order = {3, 1, 6, 2, 5, 7, 15, 13, 4, 11, 8, 9, 14, 10, 12}
# go = tk.Button(master=back, text='Start Display', command=startDisplay)
# go.pack()
# close = tk.Button(master=back, text='Quit', command=root.destroy)
# close.pack()
# info = tk.Label(master=back, text="Made by me!", bg='blue', fg='white')
# info.pack()

if __name__ == "__main__":
    root = Tk()
    root.title("Slide Game")
    #root.geometry("500x500")
    Main(root)
    root.mainloop()