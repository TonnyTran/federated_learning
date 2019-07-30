import matplotlib.pyplot as plt
from xlrd import open_workbook
import xlsxwriter

interval = 10
book = open_workbook('../results/result_v2.0_800k.xls')
book2 = open_workbook('../results/result_v9.513_2.xls')
book3 = open_workbook('../results/result_v9.531_2.xls')

column = 3

sheet = book.sheet_by_index(0)
sheet2 = book2.sheet_by_index(0)
sheet3 = book3.sheet_by_index(0)

file_name = '../result_draw/result_v9.0_time.xlsx'
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet()


X, Y1, Y2, Y3, Y4, Y1_average, Y2_average, Y3_average, Y4_average = [], [], [], [], [], [], [], [], []
for row_index in xrange(1, min(sheet.nrows, sheet2.nrows, sheet3.nrows)):
    y1 = sheet.cell_value(row_index, column)
    y2 = sheet2.cell_value(row_index, column)
    y3 = sheet3.cell_value(row_index, column)
    Y1.append(float(y1))
    Y2.append(float(y2))
    Y3.append(float(y3))

for ave_index in range(0, len(Y1)/interval-1):
    Y1_ave = sum(Y1[ave_index*interval:((ave_index+1)*interval)]) / interval
    Y1_average.append(Y1_ave)
    Y2_ave = sum(Y2[ave_index * interval:((ave_index + 1) * interval)]) / interval
    Y2_average.append(Y2_ave)
    Y3_ave = sum(Y3[ave_index * interval:((ave_index + 1) * interval)]) / interval
    Y3_average.append(Y3_ave)
    X.append(ave_index)
    worksheet.write(ave_index + 1, 0, str(ave_index))
    worksheet.write(ave_index + 1, 1, str(Y1_ave))
    worksheet.write(ave_index + 1, 2, str(Y2_ave))
    worksheet.write(ave_index + 1, 3, str(Y3_ave))

workbook.close()
# print(X)
# print(Y)
# print(Y2)
# print(Y3)
plt.xlabel('x' + str(interval) + ' Number of episodes')
plt.ylabel('Energy consumption (J)')
plt.plot(X, Y1_average, 'r', label="DQN", zorder=10)
plt.plot(X, Y2_average, 'b', label="Greedy", zorder=10)
plt.plot(X, Y3_average, 'g', label="Random", zorder=10)
plt.legend()
plt.show()