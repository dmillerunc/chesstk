import tkinter
from math import trunc
from copy import deepcopy
import time
from datetime import date
from typing import NewType
from PIL import (ImageTk, Image)
import re
import pandas as pd
import numpy as np

#from bitboard import piece
files = ["a","b","c","d","e","f","g","h"]
ranks = [8, 7, 6, 5, 4, 3, 2, 1]


#Create variables
FileLocation = NewType("FileLocation", str)
Pos = NewType("Pos", tuple)
AppTitle = "Chess Program"
cPath = "C:/Users/onlygoodderek/OneDrive/Pictures/chess program images/"
boardLoc = FileLocation(cPath+"chessboard.png")
piecesFile = FileLocation(cPath+"ChessPiecesArray.png")
yellowTileLoc = FileLocation(cPath+"YellowTile.png")
#print(type(boardLoc))
pieceCropDict = {"Q":[0,60,60,120],"K":[60,60,120,120], "R":[120,60,180,120], "N":[180,60,240,120],
    "B":[240,60,300,120], "P":[300,60,360,120], "q":[0,0,60,60],"k":[60,0,120,60],
    "r":[120,0,180,60], "n":[180,0,240,60], "b":[240,0,300,60], "p":[300,0,360,60]}
startPos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
box = (0,0,60,60)
pos = Pos((43,43))


gridBoundaries = [43,129,215,301,387,473,559,645]
maxBoundary = 688
midPoint = int(maxBoundary/2)
class chessFrame:
    def __init__(self):
        self.frame = pd.DataFrame(columns=files,index=[0,1,2,3,4,5,6,7])
        self.frame.fillna(0,inplace=True)
    def __str__(self):
        return str(self.frame)
    def add(self,_rank,_file,_input):
        self.frame.loc[_rank,_file] = _input
    def remove(self,_rank,_file):
        self.frame.loc[_rank,_file] = 0
    def to_csv(self,_title:FileLocation):
        self.frame.to_csv(_title)

class Fen:
    def __init__(self, _fen: str):
        self.fen = _fen
        self.createFrame()
        self.readFen()

    def __str__(self):
        return self.fen
    def createFrame(self):
        self.frame = chessFrame()
    def readFen(self):
        self.fenList = re.split("/", self.fen)
        if len(self.fenList) == 8:
            print("Successful Fen Upload")
        else:
            print("Fen has wrong number of ranks")
        r=0

        while r < len(self.fenList):
            f=0
            i=0
            while i < 8:
                if self.fenList[r][f].isdigit():
                    i+= int(self.fenList[r][f])-1
                    print(r,f)
                elif not self.fenList[r][f].isdigit():
                    print(self.fenList[r][f])
                    if re.match('[a-zA-Z]', self.fenList[r][f]):
                        self.frame.add(r,files[i], self.fenList[r][f])
                f+=1
                i+=1
            r+=1
    def createFen(self):
        pass

            
class ChessBoard:
    """
    Create Canvas and Board for Chess
    _app: tkinterApp
    _mbound: Size of board (Integer)
    """
    def __init__(self, _app):
        """
        _app: tKinter Application
        """
        self.moveNo = 1
        self.turn = "White"
        self.selected = False
        img = Image.open(boardLoc)
        self.pieceImg = Image.open(piecesFile)
        self.tkImg = ImageTk.PhotoImage(img)
        self.hLight = SquareHighlight()
        self.pHlight = SquareHighlight()
        self.app = _app
        self.size = 688 
        self.captPcList = []
        self.selectedPiece = object
    def createCanvas(self):
        """
        Establish Canvas for placing all future images
        """
        self.canvas = tkinter.Canvas(app_win, width = self.size, height = self.size)
        self.canvas.pack()
    def createBoard(self):
        """
        Draw ChessBoard
        """
        self.img = self.canvas.create_image(self.size/2,self.size/2, image = self.tkImg)   
    def getPieces(self, _fen:Fen):
        """
        Take _fen and create Piece List
        _fen: Fen 
        """
        self.fen = Fen(_fen)
        self.bFrame = self.fen.frame
        for r in range(8):
            for f in range(8):
                """Place piece into frame at correct location"""
                try:
                    if self.bFrame.frame[files[f]][r].upper() == "K":
                        self.bFrame.add(r,files[f], King(pieceCropDict[self.bFrame.frame[files[f]][r]],
                                                       self.pieceImg, (f,r), self.bFrame.frame[files[f]][r]))
                    elif self.bFrame.frame[files[f]][r].upper() == "Q":
                        self.bFrame.add(r,files[f], Queen(pieceCropDict[self.bFrame.frame[files[f]][r]],
                                                        self.pieceImg, (f,r), self.bFrame.frame[files[f]][r]))
                    elif self.bFrame.frame[files[f]][r].upper() == "N":
                        self.bFrame.add(r,files[f], Knight(pieceCropDict[self.bFrame.frame[files[f]][r]],
                                                         self.pieceImg, (f,r), self.bFrame.frame[files[f]][r]))
                    elif self.bFrame.frame[files[f]][r].upper() == "B":
                        self.bFrame.add(r,files[f], Bishop(pieceCropDict[self.bFrame.frame[files[f]][r]],
                                                         self.pieceImg, (f,r), self.bFrame.frame[files[f]][r]))
                    elif self.bFrame.frame[files[f]][r].upper() == "R":
                        self.bFrame.add(r,files[f], Rook(pieceCropDict[self.bFrame.frame[files[f]][r]],
                                                       self.pieceImg, (f,r), self.bFrame.frame[files[f]][r]))
                    elif self.bFrame.frame[files[f]][r].upper() == "P":
                        self.bFrame.add(r,files[f], Pawn(pieceCropDict[self.bFrame.frame[files[f]][r]],
                                                       self.pieceImg, (f,r), self.bFrame.frame[files[f]][r]))
                except:
                    pass
        print(self.bFrame)
        #print(self.pcList)
    def selectPiece(self, _piece: object):
        """
        Select _piece
        _piece: Piece Class Object
        """
        self.selectedPiece = _piece
        self.selected = True
        self.selectedPiece.selected = True
        #_piece.selected = True
    def deselectPiece(self):
        """
        Deselect Piece
        """
        self.selectedPiece
        self.selectedPiece = None
        self.selected = False
    def capturePiece(self, _piece: object):
        """
        _piece: Piece Class Object
        """
        print("Captured")
        _piece.deleteImg()
        self.pcList.remove(_piece)
        self.captPcList.append(_piece)
    def checkPieces(self, _mPos:Pos):
        """
        Return if Piece is on selected square
        _xpos: x position as integer
        _ypos: y position as integer
        """
        if self.selected == True:
            tmpObj = self.bFrame.frame[files[_mPos[0]]][_mPos[1]]
            print(self.selectedPiece.imgLoc)
            if self.selectedPiece.checkBlock(self.selectedPiece.imgLoc,_mPos,self):
                print("Move blocked by other piece")
            elif isinstance(tmpObj,Piece):
                if tmpObj.color == self.turn:
                    print("You cannot take your own piece, illegal move.")
                elif tmpObj.color != self.turn:
                    if self.selectedPiece.checkCapture(_mPos):
                        self.bFrame.add(_mPos[1],files[_mPos[0]], self.selectedPiece)
                        self.bFrame.remove(self.selectedPiece.imgLoc[1],files[self.selectedPiece.imgLoc[0]])
                        self.selectedPiece.move(_mPos)
                        #self.bFrame.to_csv(FileLocation('bframe.csv'))
            else:
                if self.selectedPiece.checklegal(_mPos):
                    rank = _mPos[1]
                    file = files[_mPos[0]]
                    oRank = self.selectedPiece.imgLoc[1]
                    oFile = files[self.selectedPiece.imgLoc[0]]
                    
                    tmp = self.selectedPiece
                    self.bFrame.add(rank,file,tmp)
                    self.bFrame.remove(oRank, oFile)
                    #self.bFrame.to_csv(FileLocation('bframe.csv'))
                    self.selectedPiece.move(_mPos)
                    self.selected = False
                    if not self.pHlight.status:
                        self.pHlight.draw(self.hLight.imgLoc)   #Turns True
                        print(_mPos)
                        self.hLight.move(_mPos)
        elif self.selected == False:
            print("Checking Legality of Selection...")
            tmpObj = self.bFrame.frame[files[_mPos[0]]][_mPos[1]]
            if isinstance(tmpObj,Piece):
                if self.turn == tmpObj.color:
                    print("Piece Selected")
                    self.selected = True
                    self.selectedPiece = tmpObj
                    if self.hLight.status and self.pHlight.status:
                        self.pHlight.delete()   #Turns False
                        self.hLight.move(_mPos)
                        self.canvas.update()
                    elif not self.hLight.status:
                        self.hLight.draw(_mPos) #turns True
                    elif self.hLight.status:
                        self.pHlight.draw(self.hLight.imgLoc)
                        self.hLight.move(_mPos) #No Change
                        self.canvas.update()
                    
                elif self.turn != tmpObj.color:
                    print("Wrong Color, Please Select Again")
    def changeTurn(self):
        """
        Change Turn
        """
        if self.turn == "White":
            self.turn = "Black"
        elif self.turn == "Black":
            self.turn = "White"     
            self.moveNo = self.moveNo + 1
    def on_mouse_click(self, _event):
        """
        gives location of center of square as determined by mouseclick
        _event: mouseclick event
        """
        x = trunc(_event.x/86)
        y = trunc(_event.y/86)
        print(x,y)
        xcenter = (trunc(_event.x/86)*86)+43
        ycenter = (trunc(_event.y/86)*86)+43
        mouse_pos = Pos((x,y))
        self.checkPieces(mouse_pos)

# class PGNLog:
#     def __init__(self):
#         self.date = str(date.today())
#         self.time = ' ' + str(time.localtime().tm_hour) + '-' + str(time.localtime().tm_min)
#         self.fileName = self.date +self.time + ".pgn"
#         with open(self.fileName, 'a') as pgnFile:
#             pgnFile.write("[Event \"?\"]\n")
#             pgnFile.write("[Site \"?\"]\n")
#             pgnFile.write("[Date \"" + self.date + "\"]\n")
#             pgnFile.write("[Round \"?\"]\n")
#             pgnFile.write("[White \"?\"]\n")
#             pgnFile.write("[Black \"?\"]\n")
#             pgnFile.write("[Result \"?\"]\n")
#             #pgnFile.write("[ECO \"*\"]\n\n")
#             pgnFile.close()
#         print("Create Log", self.fileName)
#     def writeMove(self, _str: str):
#         """
#         Write move to PGN file
#         """
#         with open(self.fileName, 'a') as pgnFile:
#             pgnFile.write(_str + ' ') 
            
class Piece:
    """
    Create Piece and draw on window.
    _box: list of integers
    _img: Image object
    _imgLoc: Set of coordinates as tuple
    _type: Piece type and color as character
    """
    def __init__(self, _box: list[int], _img: object, _imgLoc: Pos, _type):
        #print(_box,_img,_imgLoc,_type)
        self.hasMoved = False
        self.selected = False
        if _type.islower():
            self.color = "Black"
        elif _type.isupper():
            self.color = "White"
        self.type = _type
        self.box = _box
        cropImg = _img.crop(_box)
        cropImg = cropImg.resize((84,84),resample=3)
        self.tkImg = ImageTk.PhotoImage(cropImg)
        self.imgLoc = (_imgLoc[0],_imgLoc[1])
        print(self.imgLoc)
        self.draw()
        self.tmpMove = ""
    def __str__(self):
        return str((self.type,self.color))
    def deleteImg(self):
        Board.canvas.delete(self.img)
    def draw(self):
        self.img = Board.canvas.create_image((self.imgLoc[0]*86+43,self.imgLoc[1]*86+43),image = self.tkImg)
    def move(self,_newPos:Pos):
        print("Derek",_newPos)
        xmov = _newPos[0] - self.imgLoc[0]
        ymov = _newPos[1] - self.imgLoc[1]
        print(xmov,ymov)
        #rankIndex = gridBoundaries.index(_newPos[0])
        #fileIndex = gridBoundaries.index(_newPos[1])
        print("Legal Move")

        Board.canvas.move(self.img, xmov*86, ymov*86)
        Board.canvas.update()
        if Board.turn == "White":
            Board.turn = "Black"
            tmpSTR =self.getMovestr(ranks[_newPos[0]],str(files[_newPos[1]]))
            Board.tmpMove = tmpSTR
            print(Board.tmpMove)
        elif Board.turn == "Black":
            Board.turn = "White"
            tmpSTR = self.getMovestr(ranks[_newPos[0]], files[_newPos[1]])
            Board.tmpMove = Board.tmpMove + tmpSTR
            #logVar.writeMove(Board.tmpMove)
            Board.moveNo = Board.moveNo + 1
            print(Board.tmpMove)
        self.deselect
        Board.deselectPiece()
        self.imgLoc = _newPos
        self.hasMoved = True
    def checkBlock(self,_sPos:Pos,_dPos:Pos, _Board: object):
        if _sPos == _dPos:
            return False            # There is nothing blocking if the piece is not moving
        else:
            if _dPos[0] - _sPos[0] > 0 and _dPos[1] - _sPos[1] >0:
                _pDir = Pos((1,1))
            elif _dPos[0] - _sPos[0] < 0 and _dPos[1] - _sPos[1] < 0:
                _pDir = Pos((-1,-1))
            elif _dPos[0] - _sPos[0] == 0 and _dPos[1] - _sPos[1] > 0:
                _pDir = Pos((0,1))
            elif _dPos[0] - _sPos[0] > 0 and _dPos[1] - _sPos[1] == 0:
                _pDir = Pos((1,0))
            elif _dPos[0] - _sPos[0] == 0 and _dPos[1] - _sPos[1] < 0:
                _pDir = Pos((0,-1))
            elif _dPos[0] - _sPos[0] < 0 and _dPos[1] - _sPos[1] == 0:
                _pDir = Pos((-1,0))
            elif _dPos[0] - _sPos[0] > 0 and _dPos[1] - _sPos[1] < 0:
                _pDir = Pos((1,-1))
            elif _dPos[0] - _sPos[0] < 0 and _dPos[1] - _sPos[1] > 0:
                _pDir = Pos((-1,1))
            while _sPos[0] != _dPos[0] and _sPos[1] != _dPos[1]:
                _sPos =  Pos((_sPos[0] + _pDir[0], _sPos[1]+ _pDir[1]))
                if _sPos == _dPos:
                    break
                if isinstance(_Board.bFrame.frame[files[_sPos[0]]][_sPos[1]],Piece):
                    print(_Board.bFrame.frame[files[_sPos[0]]][_sPos[1]].imgLoc , "Piece Blocking intended move")
                    return True
                

            return False
    def getMovestr(self,_rank, _file):
        if self.color == "White":
            if self.type.upper() == 'P':
                tmpSTR = str(Board.moveNo) + '. ' + str(_file) + str(_rank) + ' '
            else:
                tmpSTR = str(Board.moveNo) + '. ' + self.type.upper() +str(_file) + str(_rank) + ' '
            return tmpSTR
        elif self.color == 'Black':
            if self.type.upper() == 'P':
                tmpSTR = str(_file) + str(_rank)
            else:
                tmpSTR = self.type.upper() + str(_file) + str(_rank)
            return tmpSTR
    def deselect(self):
        self.selected = False
    def select(self):
        self.selected = True
class King(Piece):    
    """
    Class for giving King rules for moving and attacking
    """

    def __init__(self, _box, _img, _imgLoc:Pos, _type):
        super().__init__(_box, _img, _imgLoc, _type) 
    
    def checklegal(self, _newPos: Pos):
        self.checkBlock(self.imgLoc,_newPos)
        xmov = abs(int(_newPos[0] - self.imgLoc[0]))
        ymov = abs(int(_newPos[1] - self.imgLoc[1]))
        #print(abs(xmov))
        #print(abs(ymov))
        if xmov == 0 and ymov == 1: #Vertical One Space
            return True
        elif xmov == 1 and ymov == 0: #Horizontal One Space
            return True
        elif xmov == 1 and ymov == 1: #Diagonal One Space
            return True
        else:
            return False    

    def checkCapture(self, _newPos: Pos):
        xmov = abs(int(_newPos[0] - self.imgLoc[0]))
        ymov = abs(int(_newPos[1] - self.imgLoc[1]))
        #print(abs(xmov))
        #print(abs(ymov))
        if xmov == 0 and ymov == 1: #Vertical One Space
            return True
        elif xmov == 1 and ymov == 0: #Horizontal One Space
            return True
        elif xmov == 1 and ymov == 1: #Diagonal One Space
            return True
        else:
            return False

class Queen(Piece):
    """
    Class for giving Queen rules for moving and attacking
    """
    def __init__(self, _box, _img, _imgLoc:Pos, _type):
        super().__init__(_box, _img, _imgLoc, _type)
    def checklegal(self, _newPos: Pos):
        xmov = abs(int(_newPos[0] - self.imgLoc[0]))
        ymov = abs(int(_newPos[1] - self.imgLoc[1]))
        if xmov == ymov: #Diaganal Movement
            return True
        elif xmov == 0 and ymov > 0: #Vertical Movement
            return True
        elif xmov > 0 and ymov ==0: #Horizontal Movement
            return True
        else:
            return False

    def checkCapture(self, _newPos: Pos):
        xmov = abs(int(_newPos[0]/86 - self.imgLoc[0]/86))
        ymov = abs(int(_newPos[1]/86 - self.imgLoc[1]/86))
        if xmov == ymov: #Diaganal Movement
            return True
        elif xmov == 0 and ymov > 0: #Vertical Movement
            return True
        elif xmov > 0 and ymov ==0: #Horizontal Movement
            return True
        else:
            return False
        #print(xmov, ymov)
class Knight(Piece):
    """
    Class for giving Knight rules for moving and attacking
    """
    def __init__(self, _box, _img, _imgLoc:Pos, _type):
        super().__init__(_box, _img, _imgLoc, _type)
    def checklegal(self, _newPos: Pos):
        xmov = abs(int(_newPos[0] - self.imgLoc[0]))
        ymov = abs(int(_newPos[1] - self.imgLoc[1]))
        if xmov == 2 and ymov == 1: #Horizontal L
            return True
        elif xmov == 1 and ymov == 2: #Vertical L
            return True
        else:
            return False
    def checkCapture(self, _newPos: Pos):
        xmov = abs(int(_newPos[0]/86 - self.imgLoc[0]/86))
        ymov = abs(int(_newPos[1]/86 - self.imgLoc[1]/86))
        if xmov == 2 and ymov == 1: #Horizontal L
            return True
        elif xmov == 1 and ymov == 2: #Vertical L
            return True
        else:
            return False

        #print(xmov, ymov)
    def checkBlock(self,_sPos,_dPos,_Board):
        return False
class Bishop(Piece):
    def __init__(self, _box, _img, _imgLoc:Pos, _type):
        super().__init__(_box, _img, _imgLoc, _type)
    def checklegal(self, _newPos: Pos):
        xmov = abs(int(_newPos[0] - self.imgLoc[0]))
        ymov = abs(int(_newPos[1] - self.imgLoc[1]))
        if xmov == ymov: #Diaganal Movement
            return True
        else:
            return False
        #print(xmov, ymov)
    def checkCapture(self, _newPos: Pos):
        xmov = abs(int(_newPos[0]/86 - self.imgLoc[0]/86))
        ymov = abs(int(_newPos[1]/86 - self.imgLoc[1]/86))
        if xmov == ymov: #Diaganal Movement
            return True
        else:
            return False
class Rook(Piece):
    def __init__(self, _box, _img, _imgLoc:Pos, _type):
        super().__init__(_box, _img, _imgLoc, _type)
    def checklegal(self, _newPos: Pos):
        xmov = abs(int(_newPos[0] - self.imgLoc[0]))
        ymov = abs(int(_newPos[1] - self.imgLoc[1]))
        if xmov == 0 and ymov > 0: #Vertical Movement
            return True
        elif xmov > 0 and ymov == 0: #Horizontal Movement
            return True
        else:
            return False
    def checkCapture(self, _newPos: Pos):
        xmov = abs(int(_newPos[0]/86 - self.imgLoc[0]/86))
        ymov = abs(int(_newPos[1]/86 - self.imgLoc[1]/86))
        if xmov == 0 and ymov > 0: #Vertical Movement
            return True
        elif xmov > 0 and ymov == 0: #Horizontal Movement
            return True
        else:
            return False
        #print(xmov, ymov)
class Pawn(Piece):
    def __init__(self, _box, _img, _imgLoc:Pos, _type):
        super().__init__(_box, _img, _imgLoc, _type)
    def checklegal(self, _newPos: Pos):
        if self.color == "White":
            yconstant = -1
        elif self.color == "Black":
            yconstant = 1
        xmov = abs(int(_newPos[0] - self.imgLoc[0]))
        ymov = int(_newPos[1] - self.imgLoc[1])
        #print(xmov,ymov,yconstant)
        if xmov == 0 and ymov == yconstant * 1: #Vertical Move One Space
            return True
        elif xmov == 0 and ymov == yconstant * 2 and not self.hasMoved: #Vertical Move Two Spaces
            return True
        else: 
            return False
        #print(xmov, ymov)
    def checkCapture(self,_newPos: Pos):
        print("Checking Capture")
        xmov = abs(int(_newPos[0] - self.imgLoc[0]))
        ymov = int(_newPos[1] - self.imgLoc[1])
        if self.color == "White":
            yconstant = -1
        elif self.color == "Black":
            yconstant = 1
        print(xmov,ymov,yconstant)
        if xmov == 1 and ymov == yconstant * 1:
            print("Capturing")
            return True
class SquareHighlight:
    """
    Creates a Square Highlight and moves it
    """
    def __init__(self):
        self.status = False
        callimage = Image.open(yellowTileLoc)
        self.img = ImageTk.PhotoImage(callimage)
    def draw(self,_mPos:Pos):
        self.imgLoc = _mPos
        self.highlight = Board.canvas.create_image(_mPos[0]*86+43,_mPos[1]*86+43,image = self.img)
        self.status=True
    def move(self,_mPos:Pos):
        xmov = _mPos[0]*86 - self.imgLoc[0]*86
        ymov = _mPos[1]*86 - self.imgLoc[1]*86
        #print(xmov,ymov)
        self.imgLoc = _mPos
        Board.canvas.move(self.highlight, xmov, ymov)
        Board.canvas.update()
    def delete(self):
        Board.canvas.delete(self.highlight)
        self.status = False


#logVar = PGNLog()          

"""
Create Window, Canvas and ChessBoard
"""
app_win = tkinter.Tk()
app_win.title(AppTitle)
app_win.geometry(str(maxBoundary)+'x'+str(maxBoundary))
Board = ChessBoard(app_win)
Board.createCanvas()
Board.createBoard()
Board.getPieces(startPos)


Board.canvas.bind("<1>", Board.on_mouse_click)





app_win.mainloop()