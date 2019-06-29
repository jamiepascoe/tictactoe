"""2-Player game of Tic Tac Toe"""

import sys
import numpy as np
from PyQt5 import QtWidgets as QtW


class Widget(QtW.QWidget):
    
    def __init__(self):
        super().__init__()    #Initialise QWidget
        self.analysis = Analysing()
        self.setWindowTitle('Tic Tac Toe')
        self.init_gui() #Initialise GUI
        self.show()
    
    def init_gui(self):
        """Initialise 3x3 button grid
        0   1   2
        3   4   5
        6   7   8"""
        self.con={1:'O', -1:'X'}    #Dictionary to convert to output format
        grid = QtW.QGridLayout()
        for i in range(9):  #Create 9 buttons
            button = QtW.QPushButton(' ', self)
            button.setObjectName('pButton'+str(i))
            button.clicked.connect(self.btn_clk)    #Add slot
            row, col = divmod(i, 3)
            grid.addWidget(button, row, col)    #Add button to 3x3 grid
        self.setLayout(grid)

    def btn_clk(self):
        """Checks move is valid, calls game complete check"""
        button = self.sender()
        if button.text() != ' ':
            QtW.QMessageBox.about(self, 'Error', 'Invalid Move')
        else:
            button.setText(self.con[self.analysis.go]) #Change button to X or O
            button_num = int(button.objectName()[-1])  #Strip index from button
            winner = self.analysis.valid_move(button_num)
            if winner is not 0: #If game complete
                self.game_over(winner)
    
    def game_over(self, winner):
        """Displays message box with game outcome, calls restart"""
        if winner in [1,-1]:    #If someone has won
            QtW.QMessageBox.about(self,' ', 'Player '+self.con[winner]+' won!')
        elif winner == 2:   #If it's a Draw
            QtW.QMessageBox.about(self,' ', "It's a Draw")
        self.restart()
    
    def restart(self):
        """Resets grid"""
        self.analysis.__init__()    #Reinitialise analysis variables
        for i in range(9):  #Reset button text
            button = self.findChild(QtW.QPushButton, 'pButton'+str(i))
            button.setText(' ')

   

class Analysing():
    """Methods that analyse whether the game is won/drawn"""
    def __init__(self):
        self.moves_grid=np.zeros(9, dtype = np.int64)   #Create  zero array
        self.go=-1   #Start with X's go
        self.goes=0  #Count number of goes carried out

    def valid_move(self, position):
        """Returns -1 if X has won, 1 if O has, 
        2 if it's a Draw, 0 to continue play"""
        self.goes+=1 #Increment total number of goes
        self.moves_grid[position]=self.go #Store new go in array
        
        if 3 in self.row_col_sums(self.moves_grid):
            return self.go     
        elif self.goes==9:    #Check if it's a draw
            return 2
        else:   #If game not over
            self.go*=-1 #Change goes
            return 0

    def row_col_sums(self, ar):
        """Returns array with absolute sum of all rows/cols/diagonals"""
        #Sum down and up diagonals
        sums=np.array([sum(ar[0::4]), sum(ar[2:8:2])])
        for i in range(3):  #Sum columns and rows
            sums = np.append(sums, [sum(ar[i::3]), sum(ar[i*3:i*3+3])])
        return np.abs(sums)


if __name__ == "__main__":
    app = QtW.QApplication([])
    widget = Widget()
    sys.exit(app.exec_())
