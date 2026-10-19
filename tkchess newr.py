import tkinter
from math import trunc
from copy import deepcopy
import time
from datetime import date
from typing import NewType
from PIL import (ImageTk, Image)
import re
import pandas as pd
from fenreader import GameManager, GameLogger

FileLocation = NewType("FileLocation", str)
Pos = NewType("Pos", tuple)
AppTitle = "Chess Program"
cPath = "C:/Users/onlygoodderek/OneDrive/Pictures/chess program images/"
boardLoc = FileLocation(cPath+"chessboard.png")
piecesFile = FileLocation(cPath+"ChessPiecesArray.png")
yellowTileLoc = FileLocation(cPath+"YellowTile.png")
gridBoundaries = [43,129,215,301,387,473,559,645]
maxBoundary = 688
class ChessBoard:
    def __init__(self, _fen:str):
        self.app = tkinter.Tk()
        self.app.title(AppTitle)
        self.size = maxBoundary
        self.gm = GameManager(_fen)
        self.gl = GameLogger()
        self.pieceList = [0]*64
        img = Image.open(boardLoc)
        self.pieceImg = Image.open(piecesFile)
        self.tkImg = ImageTk.PhotoImage(img)
        self.hLight = SquareHighLight()
        self.pHlight = SquareHighLight()
        self.createCanvas()
        self.createBoard()
        self.startApp()
    @property
    def midPoint(self)->int:
        return int(self.size/2)
    def createCanvas(self):
        """
        Establish Canvas for placing all future images
        """
        self.canvas = tkinter.Canvas(self.app, width = self.size, height = self.size)
        self.canvas.pack()
    def createBoard(self):
        """
        Draw ChessBoard
        """
        self.img = self.canvas.create_image(self.size/2,self.size/2, image = self.tkImg)  
    def startApp(self):
        self.app.mainloop()
    def getPieces(self, _fen:):
        """
        Take _fen and create Piece List
        _fen: Fen 
        """

        self.pieces = []
        for i in range(64):
            print(trunc(i/8), i%8)
            print(self.gm.gameboards.all.get_square(i))
            r = trunc(i / 8)
            f = i % 8
            tmp_sq = self.gm.gameboards.all.get_square(i)
            tmp_piece = self.gm.gameboards.get_piece(tmp_sq)
            if str(tmp_piece).upper() == 'K':
                self.pieceList[i] = King(pieceCropDict[self.bFrame.frame[files[f]][r]], self.pieceImg, (f,r), self.bFrame.frame[files[f]][r])
            elif str(tmp_piece).upper() == "Q":
                self.pieceList[i] =  Queen(pieceCropDict[self.bFrame.frame[files[f]][r]], self.pieceImg, (f,r), self.bFrame.frame[files[f]][r])
            elif str(tmp_piece).upper() == "R":
                self.pieceList[i] = Rook(pieceCropDict[self.bFrame.frame[files[f]][r]], self.pieceImg, (f,r), self.bFrame.frame[files[f]][r])
            elif str(tmp_piece).upper() == "B":
                self.pieceList[i] = Bishop(pieceCropDict[self.bFrame.frame[files[f]][r]], self.pieceImg, (f,r), self.bFrame.frame[files[f]][r])
            elif str(tmp_piece).upper() == "N":
                self.pieceList[i] = Knight(pieceCropDict[self.bFrame.frame[files[f]][r]], self.pieceImg, (f,r), self.bFrame.frame[files[f]][r])
            elif str(tmp_piece).upper() == "P":
                self.pieceList[i] = Pawn(pieceCropDict[self.bFrame.frame[files[f]][r]], self.pieceImg, (f,r), self.bFrame.frame[files[f]][r])
class SquareHighLight:
    def __init__(self):
        self.status = False
        callimage = Image.open(yellowTileLoc)
        self.img = ImageTk.PhotoImage(callimage)
        self._pos = [0,0]
    @property
    def x(self):
        return self._pos[0]
    @x.setter
    def x(self, _val):
        self._pos[0] = _val
    @property
    def y(self):
        return self._pos[1]
    @y.setter
    def y(self, _val):
        self._pos[1] = _val
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, _val: tuple):
        self._pos[0] = _val[0]
        self._pos[1] = _val[1]
class Piece:
    def __init__(self):
        pass
class King(Piece):
    def __init__(self):
        pass
class Queen(Piece):
    def __init__(self):
        pass
class Rook(Piece):
    def __init__(self):
        pass
class Bishop(Piece):
    def __init__(self):
        pass
class Knight(Piece):
    def __init__(self):
        pass
class Pawn(Piece):
    def __init__(self):
        pass
if __name__ == "__main__":
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    cb = ChessBoard(fen)