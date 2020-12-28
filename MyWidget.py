import sys
import matplotlib
import os
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
matplotlib.use("Qt5Agg")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
# from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget,QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import seaborn as sns
from scipy.stats import poisson
# sns.set_style("whitegrid")

# sns.set_style("darkgrid", {"axes.facecolor": "0"})

from PyQt5.QtCore import *
from PyQt5 import QtWidgets

class Mydemo(FigureCanvas):
    def __init__(self, parent=None, width=100, height=50, dpi=100):

        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # self.fig = Figure(figsize=(width, height))
        self.fig = Figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MatplotWidget1(FigureCanvas):

    def __init__(self, parent=None, dpi=100, initial_message=None):
        # fig,ax = plt.subplots()
        self.fig = Figure( tight_layout=True)
        # self.fig = Figure(figsize=(100, 50), tight_layout=True)
        # self.fig = plt.figure()
        self.axes =self.fig.add_subplot(1, 1, 1)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.updateGeometry()
        palette = self.palette()
        self.setContentsMargins(0,0,0,0)
        # fig.set_facecolor(palette.background().color().getRgbF()[0:3])
        # self.axes = ax


    def make_plot(self, data,x_name="",z_name="",outcome="",labeltmp=""):
        # sns.set_style("darkgrid")
        # plt.sca(self.axes)
        # self.fig.clf()
        self.fig.canvas.draw_idle()
        self.axes.clear()
        # self.plt.grid()
        # self.axes = self.fig.add_subplot(1, 1, 1)
        # pg=sns.lmplot(x_name,outcome,data,hue=z_name)
        # print(np.max(data)-np.min(data))
        if int(max(data)-min(data))!=0:
           bins=int(max(data)-min(data))
        else:
            bins = 1
        pg=sns.distplot(data,ax=self.axes,bins=bins,label=labeltmp)
        # self.axes.grid()
        self.axes.legend()
        # self.fig.legend()
        # self.axes.title(labeltmp)
        # pg=sns.distplot(data,ax=self.axes,bins=int(max(data)-min(data)),fit=poisson)
        #ax = plt.gca()
        #ax.legend(numpoints=1, fancybox=True, fontsize="small", )
        #self.axes.get_legend().draggable(True, update="loc")
        # fig = pg.fig
        # pg.set_canvas(self)
        # self.figure = fig
        # fig = self.figure
        # palette = self.palette()
        # fig.set_facecolor(palette.background().color().getRgbF()[0:3])
        #
        # plt.show()
        # self.draw()
        self.resize_event()
        # self.draw()


class ComboCheckBox(QComboBox):
    sinOuttext = pyqtSignal(list)
    def __init__(self, items):  # items==[str,str...]
        super(ComboCheckBox, self).__init__()
        self.items = items
        self.Outputindexlist=[]
        self.items.insert(0, '全部')
        self.row_num = len(self.items)
        self.Selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()
        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.All)
        for i in range(1, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.show)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)
        self.qCheckBox[0].setChecked(True)

    def addQCheckBox(self, i):
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qCheckBox[i].setChecked(True)
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

    def Selectlist(self):
        Outputlist = []
        self.Outputindexlist=[]
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                Outputlist.append(self.qCheckBox[i].text())
                self.Outputindexlist.append(i-1)
        self.Selectedrow_num = len(Outputlist)
        return Outputlist,self.Outputindexlist

    def show(self):
        show = ''
        Outputlist, Outputindexlist= self.Selectlist()
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        for i in Outputlist:
            show += i + ';'
        if self.Selectedrow_num == 0:
            self.qCheckBox[0].setCheckState(0)
        elif self.Selectedrow_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
        else:
            self.qCheckBox[0].setCheckState(1)
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)
        print(Outputindexlist)
        print(Outputlist)
        self.sinOuttext.emit(self.Outputindexlist)

    def All(self, zhuangtai):
        if zhuangtai == 2:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif zhuangtai == 1:
            if self.Selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif zhuangtai == 0:
            self.clear()
        print()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)


class CheckableComboBox(QtWidgets.QComboBox):
    sinOuttext = pyqtSignal(list)
    def loadItems(self, items):
        self.items = items
        self.items.insert(0, '全部')
        self.row_num = len(self.items)
        self.Selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()
        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.All)
        for i in range(0, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.showMessage)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)
        self.qCheckBox[0].setChecked(True)
        # self.qLineEdit.textChanged.connect(self.printResults)

    def showPopup(self):
        #  重写showPopup方法，避免下拉框数据多而导致显示不全的问题
        select_list = self.Selectlist()  # 当前选择数据
        self.loadItems(items=self.items[1:])  # 重新添加组件
        for select in select_list:
            index = self.items[:].index(select)
            self.qCheckBox[index].setChecked(True)  # 选中组件
        return QComboBox.showPopup(self)

    def printResults(self):
        list = self.Selectlist()
        print(list)

    def addQCheckBox(self, i):
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

    def Selectlist(self):
        Outputlist = []
        Outputindexlist=[]
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                Outputlist.append(self.qCheckBox[i].text())
                Outputindexlist.append(i-1)
        self.Selectedrow_num = len(Outputlist)
        self.sinOuttext.emit(Outputindexlist)
        return Outputlist

    def showMessage(self):
        Outputlist = self.Selectlist()
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        show = ';'.join(Outputlist)

        if self.Selectedrow_num == 0:
            self.qCheckBox[0].setCheckState(0)
        elif self.Selectedrow_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
        else:
            self.qCheckBox[0].setCheckState(1)
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)

    def All(self, zhuangtai):
        if zhuangtai == 2:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif zhuangtai == 1:
            if self.Selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif zhuangtai == 0:
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)

    def currentText(self):
        text = QComboBox.currentText(self).split(';')
        if text.__len__() == 1:
            if not text[0]:
                return []
        return text

if __name__ == "__main__":
    widget = MatplotWidget1()
    widget.show()
    # create fake data
    n_subjects = 40
    d = {
        "Group1": np.random.randint(1, 4, n_subjects),
        "Group2": np.random.randint(1, 3, n_subjects),
        "Outcome": np.random.random(n_subjects)
    }
    data = pd.DataFrame(d)
    widget.make_plot(data, "Group1", "Group2", "Outcome")
    app = QApplication([])
    app.exec_()