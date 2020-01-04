import sys
import matplotlib
import os
import pandas as pd
matplotlib.use("Qt5Agg")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget,QPushButton
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


    def make_plot(self, data,x_name="",z_name="",outcome=""):
        # sns.set_style("darkgrid")
        # plt.sca(self.axes)
        # self.fig.clf()
        self.fig.canvas.draw_idle()
        self.axes.clear()
        # self.axes = self.fig.add_subplot(1, 1, 1)
        # pg=sns.lmplot(x_name,outcome,data,hue=z_name)
        pg=sns.distplot(data,ax=self.axes)
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