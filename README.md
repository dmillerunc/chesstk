# chesstk

### Classes

1. [chessFrame](#chessFrame)
2. [ChessBoard](#ChessBoard)
3. [PGNLog](#pgnlog)
4. [Piece](#piece)
    1. [King](#king)
    2. [Queen](#queen)
    3. [Knight](#knight)
    4. [Bishop](#bishop)
    5. [Rook](#rook)
    6. [Pawn](#pawn)
5. [SquareHighlight](#squarehightlight)

# chessFrame
A class necessary for controlling multiple dataframes. It streamlines some of the initial code allowing for fewer key strokes.<br>
```
__init__(self):
    Starts the dataframe and cleans the data.
```
```
__str__(self):
    Returns the dataframe in a string form.
```
```
add(self, _rank, _file, _input):
    Add item to dataframe
    _rank = int
    _file = char
    _input = Piece
```
```
remove(self):
    Remove item from the dataframe
    _rank = int
    _file = char
```
```
to_csv(self, _title):
    Export dataframe to csv file
    _title = FileLocation
```
# ChessBoard
This class creates a chessboard and tracks board states.
```
__init__(self, _app):
    Initialize the board: Create basic board state.
    _app = tKinter app
```
# PGNLog
# Piece
### King
### Queen
### Knight
### Bishop
### Rook
### Pawn
# SquareHightLight

