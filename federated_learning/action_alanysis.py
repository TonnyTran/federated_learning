import matplotlib.pyplot as plt
from xlrd import open_workbook
import numpy as np
from matplotlib import cm
import xlsxwriter
from mpl_toolkits.mplot3d import axes3d

class ActionAnalysis():
    def __init__(self):
        book = open_workbook('../results/result_v6.0.xls')
        self.sheet = book.sheet_by_index(1)
        self.frequency = np.zeros((11, 6), dtype=int)
        self.actionsum = np.zeros((11, 6), dtype=int)
        self.actresult = np.zeros((11, 6), dtype=float)
        self.filename = '../result_draw/harvest_action3.xlsx'
        self.update()
        self.storeFile()
        self.draw3D()

    def update(self):
        for index in range(1, self.sheet.nrows):
            q = int(self.sheet.cell_value(index, 11))
            e = int(self.sheet.cell_value(index, 12))
            time = int(self.sheet.cell_value(index, 13))
            self.frequency[q][e] = self.frequency[q][e] + 1
            self.actionsum[q][e] = self.actionsum[q][e] + time

        for r in range(0, 11):
            for c in range(0, 6):
                if (self.frequency[r][c] > 0):
                    self.actresult[r][c] = self.actionsum[r][c] * 1.0 / self.frequency[r][c]
        print (self.actresult)

    def draw3D(self):
        X = np.arange(0, 10, 1)
        xlen = len(X)
        Y = np.arange(0, 5, 1)
        ylen = len(Y)

        fig = plt.figure()
        ax = fig.add_subplot(121, projection='3d')

        X, Y = np.meshgrid(X, Y)
        Z = self.actresult[X, Y]

        bottom = np.zeros(xlen * ylen)
        width = depth = 10
        XX = X.flatten()
        YY = Y.flatten()
        dz = Z.flatten()

        values = np.linspace(0, 10, XX.ravel().shape[0])
        colors = cm.rainbow(values)

        # cs = ['r', 'g', 'b', 'y', 'c'] * XX.ravel().shape[0]

        ax.bar3d(XX.ravel(), YY.ravel(), dz * 0, width, depth, dz, color=colors)

        ax.set_xlabel('State (Number of stakes)')
        ax.set_ylabel('Action')
        ax.set_zlabel('Probability of action selected')
        plt.show()

    def storeFile(self):
        workbook = xlsxwriter.Workbook(self.filename)
        worksheet = workbook.add_worksheet()
        for rowIndex in range(11):
            for colIndex in range(6):
                worksheet.write(rowIndex + 1, colIndex, str(self.actresult[rowIndex, colIndex]))
        workbook.close()


actionAnalysis = ActionAnalysis()

