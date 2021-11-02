from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import sys
from PyQt5 import uic
from random import randint
from reversi1 import Ui_MainWindow
import random
import time

class Choose_color(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("option.ui", self)
        self.pushButton.setStyleSheet("background-image : url(full.jpg);")
        self.pushButton_2.setStyleSheet("background-image : url(full2.jpg);")
        self.pushButton.clicked.connect(lambda x: self.clicked("1"))
        self.pushButton_2.clicked.connect(lambda x: self.clicked("2"))

    def clicked(self, checked):
        if checked == "1":
            self.w = AnotherWindow("O", "X")
        else:
            self.w = AnotherWindow("X", "O")
        self.w.show()
        self.close()
        

class AnotherWindow(QMainWindow):
    def __init__(self, chose, comp):
        super().__init__()
        uic.loadUi('reversi1.ui', self)
        self.setWindowTitle('Reversi')
        
        self.matrix = [[self.p11, self.p12, self.p13, self.p14, self.p15, self.p16, self.p17, self.p18],
                       [self.p21, self.p22, self.p23, self.p24, self.p25, self.p26, self.p27, self.p28],
                       [self.p31, self.p32, self.p33, self.p34, self.p35, self.p36, self.p37, self.p38],
                       [self.p41, self.p42, self.p43, self.p44, self.p45, self.p46, self.p47, self.p48],
                       [self.p51, self.p52, self.p53, self.p54, self.p55, self.p56, self.p57, self.p58],
                       [self.p61, self.p62, self.p63, self.p64, self.p65, self.p66, self.p67, self.p68],
                       [self.p71, self.p72, self.p73, self.p74, self.p75, self.p76, self.p77, self.p78],
                       [self.p81, self.p82, self.p83, self.p84, self.p85, self.p86, self.p87, self.p88]]

        self.p44.setStyleSheet("background-image : url(full2.jpg);")
        self.p55.setStyleSheet("background-image : url(full2.jpg);")
        self.p45.setStyleSheet("background-image : url(full.jpg);")
        self.p54.setStyleSheet("background-image : url(full.jpg);")

        self.mainBoard = self.getNewBoard()
        self.resetBoard(self.mainBoard)

        self.playerTile = chose
        self.computerTile = comp

        if chose == "O":
            self.play_color = "background-image : url(full.jpg);"
            self.comp_color = "background-image : url(full2.jpg);"
        else:
            self.play_color = "background-image : url(full2.jpg);"
            self.comp_color = "background-image : url(full.jpg);"
            
        turn = "player"

        for index_y, i in enumerate(self.matrix):
            for index_x, n in enumerate(i):
                try:
                    n.clicked.connect(lambda x: self.game(turn))
                except Exception as e:
                    print(e)

    def game(self, turn):
        sending_button = self.sender()
        sending_button = list(str(sending_button.objectName())[1:])
        self.player_move = sending_button
        if turn == 'player':
            #self.drawBoard(self.mainBoard)
            
            #self.showPoints(self.playerTile, self.computerTile)
            move = self.getPlayerMove(self.mainBoard, self.playerTile, "".join(sending_button[::-1]))
            self.makeMove(self.mainBoard, self.playerTile, move[0], move[1])

            if self.getValidMoves(self.mainBoard, self.computerTile) == []:
                turn = "player"
            else:
                turn = 'computer'
        try:
            self.game_comp(turn)
            
        except Exception as e:
            print(e)
            
    def game_comp(self, turn):
        if turn == "computer":
            #self.drawBoard(self.mainBoard)
            #self.showPoints(self.playerTile, self.computerTile)
            x, y = self.getComputerMove(self.mainBoard, self.computerTile)
            self.matrix[y][x].setStyleSheet(self.comp_color)
            self.makeMove_comp(self.mainBoard, self.computerTile, x, y)

            if self.getValidMoves(self.mainBoard, self.playerTile) == []:
                turn = 'computer'
            else:
                turn = 'player'

            #self.drawBoard(self.mainBoard)
            #scores = self.getScoreOfBoard(self.mainBoard)
            """print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
            if scores[playerTile] > scores[computerTile]:
                print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
            elif scores[playerTile] < scores[computerTile]:
                print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
            elif scores[playerTile] == scores[computerTile]:
                print('The game was a tie!')"""
        

    def drawBoard(self, board):
        HLINE = '  +---+---+---+---+---+---+---+---+'
        VLINE = '  |   |   |   |   |   |   |   |   |'
        print('    1   2   3   4   5   6   7   8')
        print(HLINE)
        for y in range(8):
            print(VLINE)
            print(y+1, end=' ')
            for x in range(8):
                print('| %s' % (board[x][y]), end=' ')
            print('|')
            print(VLINE)
            print(HLINE)

    def resetBoard(self, board):
        for x in range(8):
            for y in range(8):
                board[x][y] = ' '
        board[3][3] = 'X'
        board[3][4] = 'O'
        board[4][3] = 'O'
        board[4][4] = 'X'

    def getNewBoard(self):
        board = []
        for i in range(8):
            board.append([' '] * 8)
        return board

     
    def isValidMove(self, board, tile, xstart, ystart):
        if board[xstart][ystart] != ' ' or not self.isOnBoard(xstart, ystart):
            return False
        board[xstart][ystart] = tile # temporarily set the tile on the board.
        if tile == 'X':
            otherTile = 'O'
        else:
            otherTile = 'X'
        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection # first step in the direction
            y += ydirection # first step in the direction
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break

                if not self.isOnBoard(x, y):
                    continue
                if board[x][y] == tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        board[xstart][ystart] = ' ' # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    def isOnBoard(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <=7


    def getBoardWithValidMoves(self, board, tile):
        dupeBoard = self.getBoardCopy(board)

        for x, y in self.getValidMoves(dupeBoard, tile):
            dupeBoard[x][y] = '.'
        return dupeBoard

    def getValidMoves(self, board, tile):
        validMoves = []
        for x in range(8):
            for y in range(8):
                if self.isValidMove(board, tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves

    def getScoreOfBoard(self, board):
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'X':
                    xscore += 1
                if board[x][y] == 'O':
                    oscore += 1
        return {'X':xscore, 'O':oscore}


    def makeMove(self, board, tile, xstart, ystart):
        tilesToFlip = self.isValidMove(board, tile, xstart, ystart)

        if tilesToFlip == False:
            return False

        board[xstart][ystart] = tile
        self.matrix[ystart][xstart].setStyleSheet(self.play_color)
        for x, y in tilesToFlip:
            board[x][y] = tile
            self.matrix[y][x].setStyleSheet(self.play_color)
        return True

    def makeMove_comp(self, board, tile, xstart, ystart):
        tilesToFlip = self.isValidMove(board, tile, xstart, ystart)

        if tilesToFlip == False:
            return False

        board[xstart][ystart] = tile
        self.matrix[ystart][xstart].setStyleSheet(self.comp_color)
        for x, y in tilesToFlip:
            board[x][y] = tile
            self.matrix[y][x].setStyleSheet(self.comp_color)
        return True

    def getBoardCopy(self, board):
        dupeBoard = self.getNewBoard()

        for x in range(8):
            for y in range(8):
                dupeBoard[x][y] = board[x][y]
        return dupeBoard

    def isOnCorner(self, x, y):
        return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

    def getPlayerMove(self, board, playerTile, place):
        DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
        while True:
            move = place

            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if self.isValidMove(board, playerTile, x, y) == False:
                    continue
                else:
                    break
            else:
                print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
                print('For example, 81 will be the top-right corner.')

        return [x, y]

    def getComputerMove(self, board, computerTile):
        possibleMoves = self.getValidMoves(board, computerTile)
        random.shuffle(possibleMoves)
        for x, y in possibleMoves:
            if self.isOnCorner(x, y):
                return [x, y]

        bestScore = -1
        for x, y in possibleMoves:
            dupeBoard = self.getBoardCopy(board)
            self.makeMove_comp(dupeBoard, computerTile, x, y)
            score = self.getScoreOfBoard(dupeBoard)[computerTile]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
        return bestMove

    def showPoints(self, playerTile, computerTile):
        scores = self.getScoreOfBoard(self.mainBoard)
        print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))

        
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('first_page.ui', self)
        self.pixmap = QPixmap("start.png")
        self.label.setPixmap(self.pixmap)
        self.pixmap = QPixmap("Reversi.png")
        self.label_2.setPixmap(self.pixmap)
        self.w = None
        self.pushButton_2.clicked.connect(self.show_new_window)

    def show_new_window(self, checked):
        if self.w is None:
            try:
                self.w = Choose_color()
            except Exception as e:
                print(e)
            self.w.show()

        else:
            self.w.close()
            self.w = None
            



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
