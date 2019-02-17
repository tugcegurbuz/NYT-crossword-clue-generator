from dataExtractor import DataExtractor
from PyQt5 import uic, QtWidgets
import sys
import pandas as pd
from operator import itemgetter
import ast


def get_puzzle(crossword_num):
    across = []
    down = []
    d = pd.read_csv('./data/%d.csv'%crossword_num, sep="&", encoding='utf-8', header=None)

    sol = [[[], [], [], [], [], ], [[], [], [], [], [], ], [[], [], [], [], [], ], [[], [], [], [], [], ],
              [[], [], [], [], [], ]]
    grid = [[{}, {}, {}, {}, {}], [{}, {}, {}, {}, {}], [{}, {}, {}, {}, {}], [{}, {}, {}, {}, {}], [{}, {}, {}, {}, {}]]
    for i in range(0, 5):
        for j in range(0, 5):
            x = ast.literal_eval(d[j][i])
            d[j][i] = x
            grid[i][j]['letter'] = x['letter']
            sol[i][j] = x['letter']
            if 'number' in x:
                grid[i][j]['number'] = x['number']
                if 'across' in x:
                    across.append({'number': x['number'], 'clue': x['across'], })
                if 'down' in x:
                    down.append({'number': x['number'], 'clue': x['down'], })

    down = sorted(down, key=itemgetter('number'))
    across = sorted(across, key=itemgetter('number'))

    return across, down, sol, grid


class Ui(QtWidgets.QDialog):
    def __init__(self):
        self.de = DataExtractor()
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)
        self.crossword_num = 0

        self.todayButton.clicked.connect(self.todayPuzzle)
        self.stored1Button.clicked.connect(self.storedPuzzle1)
        self.stored2Button.clicked.connect(self.storedPuzzle2)
        self.stored3Button.clicked.connect(self.storedPuzzle3)
        self.stored4Button.clicked.connect(self.storedPuzzle4)
        self.stored5Button.clicked.connect(self.storedPuzzle5)
        self.stored6Button.clicked.connect(self.storedPuzzle6)
        self.stored7Button.clicked.connect(self.storedPuzzle7)
        self.stored8Button.clicked.connect(self.storedPuzzle8)
        self.stored9Button.clicked.connect(self.storedPuzzle9)
        self.stored10Button.clicked.connect(self.storedPuzzle10)
        self.show()

    def todayPuzzle(self):
        self.de.extractData('Firefox')
        path = 'stored_crosswords/' + self.de.date + '_' + self.de.full_date + '.csv'
        self.de.loadCSV(path)
        self.showNewPuzzle()
        self.crossword_num = 11

    def storedPuzzle1(self):
        self.de.loadCSV('./stored_crosswords/1.csv')
        self.showNewPuzzle()
        self.crossword_num = 1
        # print(self.de.grid)

    def storedPuzzle2(self):
        self.de.loadCSV('./stored_crosswords/2.csv')
        self.showNewPuzzle()
        self.crossword_num = 2

    def storedPuzzle3(self):
        self.de.loadCSV('./stored_crosswords/3.csv')
        self.showNewPuzzle()
        self.crossword_num = 3

    def storedPuzzle4(self):
        self.de.loadCSV('./stored_crosswords/4.csv')
        self.showNewPuzzle()
        self.crossword_num = 4

    def storedPuzzle5(self):
        self.de.loadCSV('./stored_crosswords/5.csv')
        self.showNewPuzzle()
        self.crossword_num = 5

    def storedPuzzle6(self):
        self.de.loadCSV('./stored_crosswords/6.csv')
        self.showNewPuzzle()
        self.crossword_num = 6

    def storedPuzzle7(self):
        self.de.loadCSV('./stored_crosswords/7.csv')
        self.showNewPuzzle()
        self.crossword_num = 7

    def storedPuzzle8(self):
        self.de.loadCSV('./stored_crosswords/8.csv')
        self.showNewPuzzle()
        self.crossword_num = 8

    def storedPuzzle9(self):
        self.de.loadCSV('./stored_crosswords/9.csv')
        self.showNewPuzzle()
        self.crossword_num = 9

    def storedPuzzle10(self):
        self.de.loadCSV('./stored_crosswords/10.csv')
        self.showNewPuzzle()
        self.crossword_num = 10


    def showNewPuzzle(self):
        self.showAcross()
        self.showDown()
        self.showSol()
        self.showClueNum()
        self.clearGrid()
        self.clearColor()
        self.showBlock()

    def showAcross(self):
        self.AcrossList.clear()
        for line in self.de.across:
            self.AcrossList.addItem(str(line['number']) + ' - ' + line['clue'])

    def showDown(self):
        self.DownList.clear()
        for line in self.de.down:
            self.DownList.addItem(str(line['number']) + ' - ' + line['clue'])

    def showSol(self):
        for i in range(5):
            for j in range(5):
                exec('self.s%d%dText.setPlainText("  "+str(self.de.matrix[i][j]))'%(i+1,j+1))

    def showClueNum(self):
        for i in range(5):
            for j in range(5):
                clue = self.de.grid[i][j]
                if 'number' in clue:
                    number = self.de.grid[i][j]['number']
                    exec('self.num%d%dLabel.setText(str(number))' % (i + 1, j + 1))
                else:
                    exec('self.num%d%dLabel.setText("")' % (i + 1, j + 1))

    def showBlock(self):
        for i in range(5):
            for j in range(5):
                clue = self.de.grid[i][j]
                if clue['letter'] == '-':
                    exec('self.g%d%dText.setStyleSheet("background-color: black;")' % (i + 1, j + 1))
                    exec('self.g%d%dText.setStyleSheet("background-color: black;")'% (i + 1, j + 1))
                    exec('self.g%d%dText.setPlainText("  -")' % (i + 1, j + 1))
                    exec('self.g%d%dText.setReadOnly(True)' % (i + 1, j + 1))

    def showCrossword(self, crossword):
        for i in range(5):
            for j in range(5):
                exec('self.g%d%dText.setPlainText("  "+str(crossword[i+5*j]["char"]))' % (j + 1, i + 1))
                exec('self.g%d%dText.setReadOnly(True)' % (i + 1, j + 1))

    def clearGrid(self):
        for i in range(5):
            for j in range(5):
                exec('self.g%d%dText.setPlainText("  ")' % (i + 1, j + 1))
                exec('self.g%d%dText.setReadOnly(False)' % (i + 1, j + 1))

    def clearColor(self):
        for i in range(5):
            for j in range(5):
                exec('self.g%d%dText.setStyleSheet("background-color: white;")' % (i + 1, j + 1))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())