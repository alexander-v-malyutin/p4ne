from matplotlib import pyplot
from openpyxl import load_workbook


wb = load_workbook('data_analysis_lab.xlsx')
sheet = wb['Data']


def getvalue(x):
    return x.value


X = list(map(getvalue, sheet['A'][1:]))
Y1 = list(map(getvalue, sheet['B'][1:]))
Y2 = list(map(getvalue, sheet['C'][1:]))
Y3 = list(map(getvalue, sheet['D'][1:]))

pyplot.plot(X, Y1, label='Температура')
pyplot.plot(X, Y2, label='Отн. температура')
pyplot.plot(X, Y3, label='Активность')
#pyplot.plot(X, Y1, 'r--', X, Y2, X, Y3)

pyplot.show()
