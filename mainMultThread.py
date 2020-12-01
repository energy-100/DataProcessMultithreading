import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import time
import pickle
import traceback
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from MyWidget import Mydemo,MatplotWidget1
from Thread import *
from dataread import *
# import qdarkstyle

# plt.grid()
# sns.set_style("whitegrid")
# sns.set_style("darkgrid", {"axes.facecolor": "0"})
from PyQt5 import QtCore

class main(QMainWindow):
    def __init__(self, parent=None):
        self.data=datastruct()
        self.historydata=[]
        self.inpath = ""
        self.outpath = ""
        self.imagen1Name = ''
        self.imagen2Name = ''
        self.imagen6Name = ''
        self.imagen7Name = ''
        self.Table2V = ""
        self.Table2H = ""
        self.showcut = 0
        self.featurex = 0
        self.fitweightindex=0
        self.b1low = [0.8, 0.1, 0, 0]
        self.b1top = [1.2, 1000, 1000, 1000000]
        self.b2low = [0.8, 0.1, 0]
        self.b2top = [1.2, 1000, 1000000]

        super(main, self).__init__(parent)
        self.setWindowTitle('人体延迟发光数据处理软件 V4.2(多线程版本)')
        self.setWindowIcon(QIcon('xyjk.png'))
        self.setFont(QFont("Microsoft YaHei", 12))
        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        self.statusBar().addPermanentWidget(self.progressBar)
        self.setAcceptDrops(True)

        self.resize(900, 600)
        self.grid = QGridLayout(self)

        self.buttontab = QTabWidget()
        self.buttontab.setMaximumHeight(450)

        self.buttontabgrid = QGridLayout(self)
        self.savetabgrid = QGridLayout(self)
        self.settingtabgrid = QGridLayout(self)
        self.historydatatabgrid = QGridLayout(self)

        self.widget2 = QWidget()
        self.widget2.setLayout(self.buttontabgrid)
        self.widget3 = QWidget()
        self.widget3.setLayout(self.savetabgrid)
        self.widget4 = QWidget()
        self.widget4.setLayout(self.settingtabgrid)
        self.widget5 = QWidget()
        self.widget5.setLayout(self.historydatatabgrid)

        self.buttontab.addTab(self.widget2, "操作面板")
        self.buttontab.addTab(self.widget3, "保存到文件")
        self.buttontab.addTab(self.widget4, "高级设置")
        self.buttontab.addTab(self.widget5, "最近添加")
        self.grid.addWidget(self.buttontab, 2, 0, 2, 3)


        # todo： 定义Figure
        self.figure = Mydemo(width=10, height=2, dpi=100)
        self.figure2 = Mydemo(width=10, height=2, dpi=100)
        self.figure6 = Mydemo(width=10, height=2, dpi=100)
        self.figure7 = Mydemo(width=10, height=2, dpi=100)
        self.figure3 = Mydemo(width=10, height=2, dpi=100)
        self.figure4 = MatplotWidget1()
        self.figure5 = Mydemo(width=10, height=2, dpi=100)
        # n_subjects = 40
        # d = {
        #     "Group1": np.random.randint(1, 4, n_subjects),
        #     "Group2": np.random.randint(1, 3, n_subjects),
        #     "Outcome": np.random.random(n_subjects)
        # }
        # data = pd.DataFrame(d)
        # self.figure4.make_plot([0,1,5,4,8,5,4,8,7,5,9,4,4,8,2,5], "Group1", "Group2", "Outcome")
        # self.figure4.make_plot(data, "Group1", "Group2", "Outcome")

        # self.figurecopy = self.figure
        # self.figure2copy =self.figure2
        # self.figure3copy = self.figure3

        self.FigtabWidget = QTabWidget()
        self.FigtabWidget.addTab(self.figure, "双曲线拟合")
        self.FigtabWidget.addTab(self.figure2, "指数拟合")
        self.FigtabWidget.addTab(self.figure6, "双曲线积分拟合")
        self.FigtabWidget.addTab(self.figure7, "指数积分拟合")
        self.FigtabWidget.addTab(self.figure3, "参数分析")
        self.FigtabWidget.addTab(self.figure4, "概率分布分析")
        self.FigtabWidget.addTab(self.figure5, "多曲线对比图")

        self.FigtabWidget.setMaximumHeight(450)
        self.grid.addWidget(self.FigtabWidget, 0, 3, 4, 12)

        # todo：高级设置
        self.labelshowcut = QLabel("图像显示模式：")
        self.showcutComboBox = QComboBox()
        self.showcutComboBox.addItems(["被裁剪的数据点+拟合数据点", "只显示拟合数据点"])
        self.showcutComboBox.setCurrentIndex(0)
        self.showcutComboBox.currentIndexChanged.connect(self.cutshowchange)
        self.settingtabgrid.addWidget(self.labelshowcut, 0, 0, 1, 1)
        self.settingtabgrid.addWidget(self.showcutComboBox, 0, 1, 1, 2)

        self.labelfeaturex = QLabel("参数变化曲线X轴：")
        self.featurexComboBox = QComboBox()
        self.featurexComboBox.addItems(["数据文件采集时间", "数据文件选择顺序"])
        self.featurexComboBox.setCurrentIndex(0)
        self.featurexComboBox.currentIndexChanged.connect(self.featurexchange)
        self.settingtabgrid.addWidget(self.labelfeaturex, 1, 0, 1, 1)
        self.settingtabgrid.addWidget(self.featurexComboBox, 1, 1, 1, 2)

        self.labelb11 = QLabel("(双曲)I0(Max比例):")
        self.settingtabgrid.addWidget(self.labelb11, 2, 0, 1, 1)
        self.labelb12 = QLabel("(双曲)τ:")
        self.settingtabgrid.addWidget(self.labelb12, 3, 0, 1, 1)
        self.labelb13 = QLabel("(双曲)Γ:")
        self.settingtabgrid.addWidget(self.labelb13, 4, 0, 1, 1)
        self.labelb14 = QLabel("(双曲)D:")
        self.settingtabgrid.addWidget(self.labelb14, 5, 0, 1, 1)
        self.labelb21 = QLabel("(指数)I0(Max比例):")
        self.settingtabgrid.addWidget(self.labelb21, 6, 0, 1, 1)
        self.labelb22 = QLabel("(指数)τ:")
        self.settingtabgrid.addWidget(self.labelb22, 7, 0, 1, 1)
        self.labelb23 = QLabel("(指数)D:")
        self.settingtabgrid.addWidget(self.labelb23, 8, 0, 1, 1)

        LineEditb11low = QLineEdit("0.8")
        # LineEditb11low.textChanged.connect(self.b11lowchange)
        LineEditb11low.setValidator(QDoubleValidator(0.0, 1.0, 6))
        LineEditb11top = QLineEdit("1.2")
        # LineEditb11top.textChanged.connect(self.b11topchange)
        LineEditb11top.setValidator(QDoubleValidator(1.0, 20.0, 6))
        LineEditb12low = QLineEdit("0.1")
        # LineEditb12low.textChanged.connect(self.b12lowchange)
        LineEditb12low.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb12top = QLineEdit("1000")
        # LineEditb12top.textChanged.connect(self.b12topchange)
        LineEditb12top.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb13low = QLineEdit("0")
        # LineEditb13low.textChanged.connect(self.b13lowchange)
        LineEditb13low.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb13top = QLineEdit("1000")
        # LineEditb13top.textChanged.connect(self.b13topchange)
        LineEditb13top.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb14low = QLineEdit("0")
        # LineEditb14low.textChanged.connect(self.b14lowchange)
        LineEditb14low.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb14top = QLineEdit("10000")
        # LineEditb14top.textChanged.connect(self.b14topchange)
        LineEditb14top.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb21low = QLineEdit("0.8")
        # LineEditb21low.textChanged.connect(self.b21lowchange)
        LineEditb21low.setValidator(QDoubleValidator(0.0, 1.0, 6))
        LineEditb21top = QLineEdit("1.2")
        # LineEditb21top.textChanged.connect(self.b21topchange)
        LineEditb21top.setValidator(QDoubleValidator(1.0, 20.0, 6))
        LineEditb22low = QLineEdit("0.1")
        # LineEditb22low.textChanged.connect(self.b22lowchange)
        LineEditb22low.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb22top = QLineEdit("1000")
        # LineEditb22top.textChanged.connect(self.b22topchange)
        LineEditb22top.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb23low = QLineEdit("0")
        # LineEditb23low.textChanged.connect(self.b23lowchange)
        LineEditb23low.setValidator(QDoubleValidator(0.01, 999999999.0, 6))
        LineEditb23top = QLineEdit("10000")
        # LineEditb23top.textChanged.connect(self.b23topchange)
        LineEditb23top.setValidator(QDoubleValidator(0.01, 999999999.0, 6))

        self.b11ComboBoxlow = QComboBox()
        self.b11ComboBoxlow.setLineEdit(LineEditb11low)
        self.b11ComboBoxlow.currentTextChanged.connect(self.b11lowchange)
        self.settingtabgrid.addWidget(self.b11ComboBoxlow, 2, 1, 1, 1)
        self.b11ComboBoxlow.addItems([str(round(i * 0.1, 1)) for i in range(10, -1, -1)])
        self.b11ComboBoxlow.setCurrentIndex(2)
        self.b11ComboBoxtop = QComboBox()
        self.b11ComboBoxtop.setLineEdit(LineEditb11top)
        self.b11ComboBoxtop.currentTextChanged.connect(self.b11topchange)
        self.settingtabgrid.addWidget(self.b11ComboBoxtop, 2, 2, 1, 1)
        self.b11ComboBoxtop.addItems([str(round(i * 0.1, 2)) for i in range(10, 21)])
        self.b11ComboBoxtop.setCurrentIndex(2)
        self.b12ComboBoxlow = QComboBox()
        self.b12ComboBoxlow.setLineEdit(LineEditb12low)
        self.b12ComboBoxlow.currentTextChanged.connect(self.b12lowchange)
        self.settingtabgrid.addWidget(self.b12ComboBoxlow, 3, 1, 1, 1)
        self.b12ComboBoxlow.addItems(
            ["0", "0.01", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
        self.b12ComboBoxlow.setCurrentIndex(2)
        self.b12ComboBoxtop = QComboBox()
        self.b12ComboBoxtop.setLineEdit(LineEditb12top)
        self.b12ComboBoxtop.currentTextChanged.connect(self.b12topchange)
        self.settingtabgrid.addWidget(self.b12ComboBoxtop, 3, 2, 1, 1)
        self.b12ComboBoxtop.addItems(
            ["1000", "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "10000", "20000", "30000", "40000",
             "50000", "60000", ])
        self.b12ComboBoxtop.setCurrentIndex(0)
        self.b13ComboBoxlow = QComboBox()
        self.b13ComboBoxlow.setLineEdit(LineEditb13low)
        self.b13ComboBoxlow.currentTextChanged.connect(self.b13lowchange)
        self.settingtabgrid.addWidget(self.b13ComboBoxlow, 4, 1, 1, 1)
        self.b13ComboBoxlow.addItems(
            ["0", "0.01", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
        self.b13ComboBoxlow.setCurrentIndex(0)
        self.b13ComboBoxtop = QComboBox()
        self.b13ComboBoxtop.setLineEdit(LineEditb13top)
        self.b13ComboBoxtop.currentTextChanged.connect(self.b13topchange)
        self.settingtabgrid.addWidget(self.b13ComboBoxtop, 4, 2, 1, 1)
        self.b13ComboBoxtop.addItems(
            ["1000", "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "10000", "20000", "30000", "40000",
             "50000", "60000", ])
        self.b13ComboBoxtop.setCurrentIndex(0)
        self.b14ComboBoxlow = QComboBox()
        self.b14ComboBoxlow.setLineEdit(LineEditb14low)
        self.b14ComboBoxlow.currentTextChanged.connect(self.b14lowchange)
        self.settingtabgrid.addWidget(self.b14ComboBoxlow, 5, 1, 1, 1)
        self.b14ComboBoxlow.addItems(
            ["0", "0.01", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
        self.b14ComboBoxlow.setCurrentIndex(0)
        self.b14ComboBoxtop = QComboBox()
        self.b14ComboBoxtop.setLineEdit(LineEditb14top)
        self.b14ComboBoxtop.currentTextChanged.connect(self.b14topchange)
        self.settingtabgrid.addWidget(self.b14ComboBoxtop, 5, 2, 1, 1)
        self.b14ComboBoxtop.addItems(
            ["1000", "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "10000", "20000", "30000", "40000",
             "50000", "60000", "1000000"])
        self.b14ComboBoxtop.setCurrentIndex(15)
        self.b21ComboBoxlow = QComboBox()
        self.b21ComboBoxlow.setLineEdit(LineEditb21low)
        self.b21ComboBoxlow.currentTextChanged.connect(self.b21lowchange)
        self.settingtabgrid.addWidget(self.b21ComboBoxlow, 6, 1, 1, 1)
        self.b21ComboBoxlow.addItems([str(round(i * 0.1, 1)) for i in range(10, -1, -1)])
        self.b21ComboBoxlow.setCurrentIndex(2)
        self.b21ComboBoxtop = QComboBox()
        self.b21ComboBoxtop.setLineEdit(LineEditb21top)
        self.b21ComboBoxtop.currentTextChanged.connect(self.b21topchange)
        self.settingtabgrid.addWidget(self.b21ComboBoxtop, 6, 2, 1, 1)
        self.b21ComboBoxtop.addItems([str(round(i * 0.1, 2)) for i in range(10, 21)])
        self.b21ComboBoxtop.setCurrentIndex(2)
        self.b22ComboBoxlow = QComboBox()
        self.b22ComboBoxlow.setLineEdit(LineEditb22low)
        self.b22ComboBoxlow.currentTextChanged.connect(self.b22lowchange)
        self.settingtabgrid.addWidget(self.b22ComboBoxlow, 7, 1, 1, 1)
        self.b22ComboBoxlow.addItems(
            ["0", "0.01", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
        self.b22ComboBoxlow.setCurrentIndex(2)
        self.b22ComboBoxtop = QComboBox()
        self.b22ComboBoxtop.setLineEdit(LineEditb22top)
        self.b22ComboBoxtop.currentTextChanged.connect(self.b22topchange)
        self.settingtabgrid.addWidget(self.b22ComboBoxtop, 7, 2, 1, 1)
        self.b22ComboBoxtop.addItems(
            ["1000", "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "10000", "20000", "30000", "40000",
             "50000", "60000", ])
        self.b22ComboBoxtop.setCurrentIndex(0)
        self.b23ComboBoxlow = QComboBox()
        self.b23ComboBoxlow.setLineEdit(LineEditb23low)
        self.b23ComboBoxlow.currentTextChanged.connect(self.b23lowchange)
        self.settingtabgrid.addWidget(self.b23ComboBoxlow, 8, 1, 1, 1)
        self.b23ComboBoxlow.addItems(
            ["0", "0.01", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
        self.b23ComboBoxlow.setCurrentIndex(0)
        self.b23ComboBoxtop = QComboBox()
        self.b23ComboBoxtop.setLineEdit(LineEditb23top)
        self.b23ComboBoxtop.currentTextChanged.connect(self.b23topchange)
        self.settingtabgrid.addWidget(self.b23ComboBoxtop, 8, 2, 1, 1)
        self.b23ComboBoxtop.addItems(
            ["1000", "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "10000", "20000", "30000", "40000",
             "50000", "60000", "1000000"])
        self.b23ComboBoxtop.setCurrentIndex(15)

        # self.label1=QLabel("文件列表：")
        # self.grid.addWidget(self.label1, 2, 0, 1, 3)

        self.label2 = QLabel("转换后的列表(按住ctrl选择多列或多行，右键选择复制类型)：")
        self.grid.addWidget(self.label2, 4, 0, 1, 10)

        self.deletedataButton=QPushButton("移除选中数据")
        self.deletedataButton.clicked.connect(self.deletedataButtonclicked)
        self.grid.addWidget(self.deletedataButton, 4, 9, 1, 1)

        self.getMeandataButton = QPushButton("求数据整体均值")
        self.getMeandataButton.clicked.connect(self.getMeandataclicked)
        self.grid.addWidget(self.getMeandataButton, 4, 7, 1, 1)

        self.backdataButton = QPushButton("重置当前数据")
        self.backdataButton.clicked.connect(self.backdataclicked)
        self.grid.addWidget(self.backdataButton, 4, 8, 1, 1)


        self.label3 = QLabel("数据子矩阵：")
        # self.grid.addWidget(self.label3, 4, 10, 1, 5)

        # todo：列表定义
        self.Table1 = QListWidget()

        self.Table2 = QTableWidget()
        self.Table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table2.horizontalHeader().sectionClicked.connect(self.Table2HorizontalHeaderClick)
        self.Table2.verticalScrollBar().valueChanged.connect(self.Table2verticalScrollbarvaluechanged)

        # self.Table2.setSelectionMode(QAbstractItemView.MultiSelection)
        self.Table2.verticalHeader().sectionClicked.connect(self.Table2VerticalHeaderClick)
        self.Table2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Table2.customContextMenuRequested.connect(self.generateMenu2)
        self.grid.addWidget(self.Table2, 5, 0, 1, 10)

        self.Table3 = QTableWidget()
        self.Table3.horizontalHeader().sectionClicked.connect(self.Table3HorizontalHeaderClick)
        self.Table3.verticalHeader().sectionClicked.connect(self.Table3VerticalHeaderClick)
        self.Table3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.grid.addWidget(self.Table3, 5, 10, 1, 5)

        #拟合历史
        self.Table4 = QTableWidget()
        self.Table4.verticalHeader().sectionClicked.connect(self.Table4VerticalHeaderClick)
        self.Table5 = QTableWidget()
        self.Table5.verticalHeader().sectionClicked.connect(self.Table5VerticalHeaderClick)
        # self.Table4.horizontalHeader().sectionClicked.connect(self.Table4HorizontalHeaderClick)
        # self.Table4.verticalHeader().sectionClicked.connect(self.Table4VerticalHeaderClick)
        self.Table4.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table4.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Table5.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table5.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        #积分拟合历史
        self.Table8 = QTableWidget()
        self.Table8.verticalHeader().sectionClicked.connect(self.Table8VerticalHeaderClick)
        self.Table9 = QTableWidget()
        self.Table9.verticalHeader().sectionClicked.connect(self.Table9VerticalHeaderClick)
        # self.Table8.horizontalHeader().sectionClicked.connect(self.Table8HorizontalHeaderClick)
        # self.Table8.verticalHeader().sectionClicked.connect(self.Table8VerticalHeaderClick)
        self.Table8.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table8.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Table9.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table9.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


        self.Table6 = QTableWidget()
        self.Table6.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table6.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Table6.setSelectionBehavior(QAbstractItemView.SelectRows)


        self.Table7 = QListWidget()
        self.Table7.setFont(QFont("Microsoft YaHei", 12))
        self.Table7.clicked.connect(self.table7clicked)
        self.historydatatabgrid.addWidget(self.Table7)
        # self.Table7.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.Table7.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.Table7.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.Table4, "单文件双曲线拟合历史")
        self.tabWidget.addTab(self.Table5, "单文件指数拟合历史")
        self.tabWidget.addTab(self.Table8, "单文件双曲线积分拟合历史")
        self.tabWidget.addTab(self.Table9, "单文件指数积分拟合历史")
        self.tabWidget.addTab(self.Table3, "数据子矩阵")
        self.tabWidget.addTab(self.Table6, "文件详细信息")

        self.grid.addWidget(self.tabWidget, 4, 10, 2, 5)

        self.readfileButton = QPushButton("读取并转换")
        self.grid.addWidget(self.readfileButton, 0, 0, 1, 1)
        self.readfileButton.clicked.connect(lambda: self.readfileButtonclicked())

        self.inLineEdit = dragLineEdit(self.statusBar)
        self.inLineEdit.setPlaceholderText('可拖拽数据文件夹至此')
        self.inLineEdit.returnPressed.connect(lambda: self.inLineEditfinished())
        self.inLineEdit.textChanged.connect(lambda: self.inLineEditfinished())
        self.grid.addWidget(self.inLineEdit, 0, 1, 1, 2)

        self.outfileButton = QPushButton("输出文件夹")
        self.grid.addWidget(self.outfileButton, 1, 0, 1, 1)
        self.outfileButton.clicked.connect(lambda: self.outfileButtonclicked())

        self.outLineEdit = QLineEdit(self)
        # self.inLineEdit.setPlaceholderText('可拖拽输出目录至此')
        self.outLineEdit.returnPressed.connect(lambda: self.outLineEditfinished())
        self.grid.addWidget(self.outLineEdit, 1, 1, 1, 2)

        # self.cutButton = QPushButton("数据裁剪")
        # self.grid.addWidget(self.cutButton, 6, 7, 1, 1)
        # self.cutButton.clicked.connect(lambda: self.cutButtonlicked())

        self.fitButton = QPushButton("数据拟合")
        self.buttontabgrid.addWidget(self.fitButton, 8, 0, 1, 3)
        self.fitButton.clicked.connect(lambda: self.fitButtonlicked())

        self.saveImageButton1 = QPushButton("保存双曲线图片")
        self.savetabgrid.addWidget(self.saveImageButton1, 0, 0, 1, 1)
        self.saveImageButton1.clicked.connect(lambda: self.saveImage1Buttonlicked())

        self.saveImageButton2 = QPushButton("保存指数图片")
        self.savetabgrid.addWidget(self.saveImageButton2, 1, 0, 1, 1)
        self.saveImageButton2.clicked.connect(lambda: self.saveImage2Buttonlicked())

        self.saveImageButton3 = QPushButton("保存参数变化图片")
        self.savetabgrid.addWidget(self.saveImageButton3, 2, 0, 1, 1)
        self.saveImageButton3.clicked.connect(lambda: self.saveImage3Buttonlicked())

        self.saveImageButton4 = QPushButton("保存概率分布图片")
        self.savetabgrid.addWidget(self.saveImageButton4, 3, 0, 1, 1)
        # self.saveImageButton4.clicked.connect(lambda: self.saveImage4Buttonlicked())

        self.saveImageButton5 = QPushButton("保存双曲-指数对比图")
        self.savetabgrid.addWidget(self.saveImageButton5, 4, 0, 1, 1)
        self.saveImageButton5.clicked.connect(lambda: self.saveImage5Buttonlicked())

        self.savefileButton = QPushButton("保存数据")
        self.savetabgrid.addWidget(self.savefileButton, 0, 1, 1, 1)
        self.savefileButton.clicked.connect(lambda: self.savefileButtonclicked())

        self.savefilesonButton = QPushButton("保存子矩阵(全部)")
        self.savetabgrid.addWidget(self.savefilesonButton, 1, 1, 1, 1)
        self.savefilesonButton.clicked.connect(lambda: self.savefilesonButtonclicked())

        self.savesinglefilesonButton = QPushButton("保存单文件裁剪数据")
        self.savetabgrid.addWidget(self.savesinglefilesonButton, 2, 1, 1, 1)
        self.savesinglefilesonButton.clicked.connect(lambda: self.savesinglefilesonButtonclicked())

        self.savedatafileButton = QPushButton("保存当前状态")
        self.savetabgrid.addWidget(self.savedatafileButton, 3, 1, 1, 1)
        self.savedatafileButton.clicked.connect(lambda: self.savedatafileButtonclicked())

        self.savefilesontxtButton = QPushButton("保存预处理后的TXT")
        self.savetabgrid.addWidget(self.savefilesontxtButton, 4, 1, 1, 1)
        self.savefilesontxtButton.clicked.connect(lambda: self.savefilesontxtButtonclicked())

        self.cutstartlabel = QLabel("删除数据个数(前):")
        self.cutstartlabel.setAlignment(Qt.AlignRight)
        self.buttontabgrid.addWidget(self.cutstartlabel, 0, 0, 1, 1)

        self.cutendlabel = QLabel("删除数据个数(后):")
        self.cutendlabel.setAlignment(Qt.AlignRight)
        self.buttontabgrid.addWidget(self.cutendlabel, 1, 0, 1, 1)

        # self.cutlabel = QLabel("裁剪模式:")
        # self.cutlabel.setAlignment(Qt.AlignRight)
        # self.grid.addWidget(self.cutlabel, 6, 4, 1, 1)

        # self.cuttypeComboBox = QComboBox()
        # self.cuttypeComboBox.addItems(
        #     ["批量裁剪"])
        # # self.cuttypeComboBox.setCurrentIndex(0)
        # # self.cuttypeComboBox.currentIndexChanged.connect(lambda: self.ChangedcuttypeComboBox())
        # self.grid.addWidget(self.cuttypeComboBox, 6, 5, 1, 2)

        self.fitlabel = QLabel("拟合模式:")
        # self.fitlabel.setAlignment(Qt.AlignRight)
        self.buttontabgrid.addWidget(self.fitlabel, 6, 0, 1, 1)

        self.fitComboBox = QComboBox()
        self.fitComboBox.addItems(
            ["批量拟合"])
        # self.fitComboBox.setCurrentIndex(0)
        # self.fitComboBox.currentIndexChanged.connect(lambda: self.ChangedfitComboBox())
        self.buttontabgrid.addWidget(self.fitComboBox, 6, 1, 1, 2)


        self.fitweightlabel = QLabel("拟合权重参数:")
        # self.fitlabel.setAlignment(Qt.AlignRight)
        self.buttontabgrid.addWidget(self.fitweightlabel, 7, 0, 1, 1)

        self.fitweightComboBox = QComboBox()
        self.fitweightComboBox.addItems(
            ["权重全部为1","权重为1/y","权重为子矩阵方差"])
        self.fitweightComboBox.currentIndexChanged.connect(self.fitweightComboBoxindexchanged)
        # self.fitComboBox.setCurrentIndex(0)
        # self.fitComboBox.currentIndexChanged.connect(lambda: self.ChangedfitComboBox())
        self.buttontabgrid.addWidget(self.fitweightComboBox, 7, 1, 1, 2)

        ComBoxlist = [str(i) for i in range(0, 101)]
        # ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
        #  "20"]
        LineEditcutstrat = QLineEdit("0")
        LineEditcutstrat.setValidator(QIntValidator(0, 999999999))
        LineEditcutend = QLineEdit("0")
        LineEditcutend.setValidator(QIntValidator(0, 999999999))

        self.cutComboBoxstart = QComboBox()
        self.cutComboBoxstart.addItems(ComBoxlist)
        self.cutComboBoxstart.setCurrentIndex(0)
        self.cutComboBoxstart.setLineEdit(LineEditcutstrat)
        # self.cutComboBoxstart.setEditText("1")
        # self.cutComboBoxstart.currentIndexChanged.connect(lambda: self.ChangedcutComboBoxstart())
        self.buttontabgrid.addWidget(self.cutComboBoxstart, 0, 1, 1, 2)

        self.cutComboBoxend = QComboBox()
        self.cutComboBoxend.addItems(ComBoxlist)
        self.cutComboBoxend.setCurrentIndex(0)
        self.cutComboBoxend.setLineEdit(LineEditcutend)
        # self.cutComboBoxend.currentIndexChanged.connect(lambda: self.ChangedcutComboBoxend())
        self.buttontabgrid.addWidget(self.cutComboBoxend, 1, 1, 1, 2)

        # 函数拟合符复选框
        self.cb1 = QCheckBox('双曲', self)
        self.cb1.setChecked(True)
        self.buttontabgrid.addWidget(self.cb1, 2, 0, 1, 1)
        self.cb2 = QCheckBox('指数', self)
        self.cb2.setChecked(True)
        self.buttontabgrid.addWidget(self.cb2, 3, 0, 1, 1)
        self.cb3 = QCheckBox('双曲积分', self)
        self.cb3.setChecked(True)
        self.buttontabgrid.addWidget(self.cb3, 4, 0, 1, 1)
        self.cb4 = QCheckBox('指数积分', self)
        self.cb4.setChecked(True)
        self.buttontabgrid.addWidget(self.cb4, 5, 0, 1, 1)

        self.cb1ComboBoxstart = QComboBox()
        self.cb1ComboBoxstart.addItems(["trf", "dogbox"])
        # self.cb1ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        self.buttontabgrid.addWidget(self.cb1ComboBoxstart, 2, 1, 1, 2)

        self.cb2ComboBoxstart = QComboBox()
        self.cb2ComboBoxstart.addItems(["trf", "dogbox"])
        # self.cb2ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        self.buttontabgrid.addWidget(self.cb2ComboBoxstart, 3, 1, 1, 2)

        self.cb3ComboBoxstart = QComboBox()
        self.cb3ComboBoxstart.addItems(["trf", "dogbox"])
        # self.cb3ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        self.buttontabgrid.addWidget(self.cb3ComboBoxstart, 4, 1, 1, 2)

        self.cb4ComboBoxstart = QComboBox()
        self.cb4ComboBoxstart.addItems(["trf", "dogbox"])
        # self.cb4ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        self.buttontabgrid.addWidget(self.cb4ComboBoxstart, 5, 1, 1, 2)

        # self.plottypeComboBox = QComboBox()
        # # self.plottypeComboBox.addItems(["双曲线拟合", "指数拟合"])
        # # self.cb3ComboBoxstart.addItems(["lm", "trf", "dogbox"])
        # self.grid.addWidget(self.plottypeComboBox, 6, 10, 1, 1)

        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        # self.tab = dragTabWidget(self.statusBar, self.inLineEdit)
        self.tab = QTabWidget()
        self.tab.addTab(self.widget, "数据预处理")
        # self.tab.addTab(self.figurecopy,"双曲线图片")
        # self.tab.addTab(self.figure2copy,"指数图片")
        # self.tab.addTab(self.figure3copy,"参数图片")

        #增加提取I0模块
        #————————————————
        self.exwidget=QWidget()
        self.exgrid = QGridLayout(self)
        self.exLineEditin = dragLineEdit(self.statusBar)
        #exLineEditout = QLineEdit()
        self.exbutton=QPushButton("选择文件夹")
        self.exgrid.addWidget(self.exLineEditin,0,0,1,1)
        self.exgrid.addWidget(self.exbutton,0,1,1,1)
        self.exwidget.setLayout(self.exgrid)
        self.tab.addTab(self.exwidget,"批量提取I0")
        # ————————————————



        self.setCentralWidget(self.tab)
        self.loadache()
        # self.loginthread=login()
        # self.loginthread.start()
        # self.getuserinf=getuserinf()
        # self.getuserinf.start()

    def loadache(self):
        filename = os.getcwd()+"/cache/temp.ache"
        historydatapath=os.getcwd()+"/cache/historydata.ache"
        if (os.path.exists(filename)):
            f = open(filename, 'rb')
            filepath = pickle.load(f)
            f.close()
            # print(filepath)
            if (os.path.exists(filepath)):
                with open(filepath, "rb") as file:
                    data = pickle.load(file)
                    # print(data)
                self.updatareadhistory(data)

        # 读取最近添加缓存
        if (os.path.exists(historydatapath)):
            f = open(historydatapath, 'rb')
            historydata = pickle.load(f)
            f.close()
            self.historydata=historydata
            self.Table7.addItems(self.historydata)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # print()
        # self.savedatafileButtonclicked()
        self.savecache()

    def savecache(self):
        print("保存缓存")
        filename = os.getcwd() + "/cache/temp.ache"
        filepath = os.getcwd() + "/cache/"
        if (not os.path.exists(filepath)):
            os.makedirs(filepath)
        datapath = self.data.inpath + "/" + os.path.basename(self.data.inpath) + ".data"
        with open(filename, "wb") as file:
            pickle.dump(datapath, file, True)


    def readfileButtonclicked(self):
        self.savedatafileButtonclicked()
        print("选取数据")
        self.statusBar().showMessage("正在选择文件夹...")
        path = QFileDialog.getExistingDirectory(self, "请选择数据文件的根目录")
        # path = "C:/Users/ENERGY/Desktop/工作文件/test"
        # path = "D:/工作文件2/lhy"
        if path == "":
            self.statusBar().showMessage("未选择文件夹！")
        elif (path == self.data.inpath):
            self.statusBar().showMessage("读取文件夹位置未改变！")
        else:
            # print(path)
            self.addhistorydata(path)
            # self.uploadinfthread=UploadClient(path)
            # self.uploadinfthread.start()
            if(os.path.exists(path+"/"+os.path.basename(path)+".data")):
                #有历史数据
                # self.inpath = path
                self.thraedreadhistory=readhistory(path+"/"+os.path.basename(path)+".data")
                self.thraedreadhistory.sinOuttext.connect(self.updatestatusbar)
                self.thraedreadhistory.sinOutoutEndThread.connect(self.updatareadhistory)
                self.thraedreadhistory.start()
            else:
                #无历史数据
                self.fitComboBox.clear()
                self.fitComboBox.addItems(["批量拟合"])
                self.inLineEdit.blockSignals(True)
                self.inLineEdit.setText(path)
                self.inLineEdit.blockSignals(False)
                # self.inpath = path
                self.outpath = path + "/预处理后的数据"
                self.outLineEdit.blockSignals(True)
                self.outLineEdit.setText(self.outpath)
                self.outLineEdit.blockSignals(False)
                self.threadread=readthread(path)
                # self.threadread.sinOutoutpath.connect(self.updatepath)
                self.threadread.sinOuttext.connect(self.updatestatusbar)
                self.threadread.sinOutpro.connect(self.updatepro)
                self.threadread.sinOutoutEndThread.connect(self.updateData)
                self.threadread.sinOutoutEndThread.connect(self.savedatafileButtonclicked)
                self.threadread.sinOutbool.connect(self.provisible)
                # self.threadread.sinOutoutData.connect(self.updateData)
                self.threadread.start()

    def outfileButtonclicked(self):
        print("outfileButtonclicked")
        self.statusBar().showMessage("正在输出文件夹...")
        path = QFileDialog.getExistingDirectory(self, "请选择数据文件的根目录")
        # path = "C:/Users/ENERGY/Desktop/工作文件/test"
        if path != "":
            self.outpath = path + "/预处理后的数据"
            self.outLineEdit.setText(self.outpath)

    def inLineEditfinished(self):
        print("inLineEditfinished")
        self.savedatafileButtonclicked()
        path = self.inLineEdit.text()
        if (not (os.path.exists(path))):
            self.statusBar().showMessage("文件夹不存在，请重新输入！")
        elif (path == self.data.inpath):
            self.statusBar().showMessage("读取文件夹位置未改变！")
        else:
            self.addhistorydata(path)
            if (os.path.exists(path + "/" + os.path.basename(path) + ".data")):
                # 有历史数据
                # self.inpath = path
                self.thraedreadhistory = readhistory(path + "/" + os.path.basename(path) + ".data")
                self.thraedreadhistory.sinOuttext.connect(self.updatestatusbar)
                self.thraedreadhistory.sinOutoutEndThread.connect(self.updatareadhistory)
                self.thraedreadhistory.start()
            else:
                # 无历史数据
                self.fitComboBox.clear()
                self.fitComboBox.addItems(["批量拟合"])
                self.inLineEdit.blockSignals(True)
                self.inLineEdit.setText(path)
                self.inLineEdit.blockSignals(False)
                # self.inpath = path
                self.outpath = path + "/预处理后的数据"
                self.outLineEdit.blockSignals(True)
                self.outLineEdit.setText(self.outpath)
                self.outLineEdit.blockSignals(False)
                self.threadread = readthread(path)
                # self.threadread.sinOutoutpath.connect(self.updatepath)
                self.threadread.sinOuttext.connect(self.updatestatusbar)
                self.threadread.sinOutpro.connect(self.updatepro)
                self.threadread.sinOutoutEndThread.connect(self.updateData)
                self.threadread.sinOutbool.connect(self.provisible)
                # self.threadread.sinOutoutData.connect(self.updateData)
                self.threadread.start()

    def outLineEditfinished(self):
        print("outLineEditfinished")
        path = self.outLineEdit.text()
        if (not (os.path.exists(path))):
            self.statusBar().showMessage("路径不存在，输出时将自动创建文件夹！")

        elif (os.path.exists(path + "/预处理后的数据.xls")):
            self.outpath = path
            self.statusBar().showMessage("文件已存在，若不想覆盖文件请更改文件保存路径")
        else:
            self.outpath = path + "/预处理后的数据.xls"
            self.statusBar().showMessage("已更改输出文件路径！")

    def Table2HorizontalHeaderClick(self, index):
        print("Table2HorizontalHeaderClick")
        if self.Table2.verticalHeader().selectionModel().selectedIndexes() == []:
            return
        if (index not in[0,1,5,15] ):
            # print("序号", index)
            colselectv = []
            tempdict = dict()
            maxv = 0
            for indext in self.Table2.verticalHeader().selectionModel().selectedIndexes():
                temp = indext.row()
                if (temp in tempdict):
                    tempdict[temp] += 1
                    if (tempdict[temp] > maxv):
                        maxv = tempdict[temp]
                else:
                    tempdict[temp] = 1
            for key, value in tempdict.items():
                if value == maxv:
                    colselectv.append(key)
            # colselect.discard(1)
            # print("tempdict", tempdict)
            # print("colselect", colselectv)

            # for indext in self.Table2.horizontalHeader().selectionModel().selectedIndexes():
            #     colselect.add(indext.column())
            # print(colselect)
            # colselect.discard(1)

            colselect = set()
            tempdict = dict()
            maxh = 0
            for indext in self.Table2.horizontalHeader().selectionModel().selectedIndexes():
                temp = indext.column()
                if (temp in tempdict):
                    tempdict[temp] += 1
                    if (tempdict[temp] > maxh):
                        maxh = tempdict[temp]
                else:
                    tempdict[temp] = 1

            for key, value in tempdict.items():
                if value == maxh:
                    colselect.add(key)
            colselect.discard(1)
            colselect.discard(0)
            # print("tempdict", tempdict)
            # print("colselect", colselect)
            if len(colselect) == (self.Table2.columnCount() - 2):
                return
            if colselectv == []:
                colselectv = range(self.Table2.rowCount())

            ys = []
            x = []
            # self.Table3.setRowCount(self.Table2.rowCount())
            # self.Table3.setColumnCount(1)
            # self.Table3.setHorizontalHeaderLabels([self.Table2.horizontalHeaderItem(index).text()])
            title = []
            for colnum in colselect:
                title.append(self.Table2.horizontalHeaderItem(colnum).text())
                y = []
                for i in colselectv:
                    if (self.Table2.item(i, colnum).text() == ""):
                        y.append(0)
                    else:
                        y.append(float(self.Table2.item(i, colnum).text().split("±")[0]))
                ys.append(y)
            for time in colselectv:
                x.append(self.data.filelist[self.Table2.item(time, 0).text()].ACQ_Time)
            self.plotfeature(x, ys, title)

    def Table2VerticalHeaderClick(self, index):
        print("Table2VerticalHeaderClick",index)

        self.data.Table2selectrow=index
        # print("序号", index)
        colselectv = []
        tempdict = dict()
        maxv = 0
        for indext in self.Table2.verticalHeader().selectionModel().selectedIndexes():
            temp = indext.row()
            if (temp in tempdict):
                tempdict[temp] += 1
                if (tempdict[temp] > maxv):
                    maxv = tempdict[temp]
            else:
                tempdict[temp] = 1
        for key, value in tempdict.items():
            if value == maxv:
                name = self.Table2.item(key, 0).text()
                colselectv.append(name)
        # colselect.discard(1)
        # print("tempdict", tempdict)
        # print("colselect", colselectv)

        self.Table6.scrollToItem(self.Table6.item(index, 0), QAbstractItemView.PositionAtTop)
        self.Table6.selectRow(index)

        self.fitComboBox.clear()
        self.fitComboBox.addItems(["[" + str(index + 1) + "]" + self.Table2.item(index, 0).text(), "批量拟合"])
        filename = self.Table2.item(index, 0).text()
        self.Table2V = filename

        self.updataTable45()
        if (self.Table4.rowCount() != 0):
            self.Table4.selectRow(self.Table4.rowCount() - 1)
        if (self.Table5.rowCount() != 0):
            self.Table5.selectRow(self.Table5.rowCount() - 1)
        if (self.Table8.rowCount() != 0):
            self.Table8.selectRow(self.Table8.rowCount() - 1)
        if (self.Table9.rowCount() != 0):
            self.Table9.selectRow(self.Table9.rowCount() - 1)

        # x=self.data.filelist[filename].Pro_Data1_X
        # y=self.data.filelist[filename].Pro_Data1

        # table4增添数值

        #
        # for i in range(len()):
        # self.Table4.setItem()

        # 改变显示图像类型下拉框
        # self.plottypeComboBox.clear()
        # if(self.data.filelist[filename].paras["双曲线拟合"]!=[]):
        #     self.plottypeComboBox.addItem("双曲线拟合")
        # if(self.data.filelist[filename].paras["指数拟合"]!=[]):
        #     self.plottypeComboBox.addItem("指数拟合")

        self.Table3.setRowCount(1 + len(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1[0]))
        self.Table3.setColumnCount(len(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1))
        for i in range(len(self.data.filelist[filename].Pro_Data1)):
            self.Table3.setItem(0, i, QTableWidgetItem(str(self.data.filelist[filename].Pro_Data1[i])))
            self.Table3.item(0, i).setBackground(QBrush(QColor(240, 125, 80)))

        for i in range(len(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1)):
            for j in range(len(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1[i])):
                self.Table3.setItem(j + 1, i, QTableWidgetItem(
                    str(self.data.filelist[self.Table2.item(index, 0).text()].Pro_mal1[i][j])))

        # self.Table3.setRowCount(1)
        # self.Table3.setColumnCount(self.Table2.columnCount())
        # coltitle=[]
        #
        # for i in range(self.Table2.columnCount()):
        #     coltitle.append(self.Table2.horizontalHeaderItem(i).text())
        #     self.Table3.setItem(0,i,QTableWidgetItem(self.Table2.item(index,i).text()))
        # self.Table3.setHorizontalHeaderLabels(coltitle)

        # numstart=self.data.filelist[self.Table2.item(index,0).text()].cutstartnumspot1
        # numend=self.data.filelist[self.Table2.item(index,0).text()].cutstartnumspot1
        self.plotdata(colselectv)
        # self.plotdata(filename)

    def Table3HorizontalHeaderClick(self, index):
        print("Table3HorizontalHeaderClick")
        self.FigtabWidget.setCurrentIndex(5)
        # print(index)
        # print(self.Table2.horizontalHeaderItem(index).text())
        # if(index==1):
        row = []
        x = []
        for i in range(1, self.Table3.rowCount()):
            row.append(int(self.Table3.item(i, index).text()))
        self.plotperspot(x, row, self.Table2V + "第" + str(index + 1) + "个数据点重复测试数值变化图")
        self.imagen4Name = self.Table2V + "第" + str(index + 1) + "个数据点重复测试数值变化图"
        self.figure4.make_plot(row)

    def Table3VerticalHeaderClick(self, index):
        print("Table3VerticalHeaderClick")
        self.FigtabWidget.setCurrentIndex(5)
        # print(index)
        # print(self.Table2.horizontalHeaderItem(index).text())
        # if(index==1):
        row = []
        x = []
        for i in range(0, self.Table3.columnCount()):
            row.append(float(self.Table3.item(index, i).text()))
        self.plotperspot(x, row, self.Table2V + "重复测试中每个点的第" + str(index + 1) + "次测量值变化图")
        self.imagen4Name = self.Table2V + "重复测试中每个点的第" + str(index + 1) + "次测量值变化图"

    def updataTable45(self):
        print("updataTable45")
        self.Table4.clear()
        self.Table5.clear()
        self.Table8.clear()
        self.Table9.clear()
        self.Table4.setColumnCount(0)
        self.Table5.setColumnCount(0)
        self.Table8.setColumnCount(0)
        self.Table9.setColumnCount(0)
        self.Table4.setRowCount(0)
        self.Table5.setRowCount(0)
        self.Table8.setRowCount(0)
        self.Table9.setRowCount(0)

        if (self.Table2V != ""):

            if (self.data.filelist[self.Table2V].paras["双曲线拟合"] != []):
                self.Table4.setColumnCount(14)
                self.Table4.setRowCount(len(self.data.filelist[self.Table2V].paras["双曲线拟合"]))
                self.Table4.setHorizontalHeaderLabels(
                    ["文件名", "前截点", "后截点", "Max", "拟合权重","I_0", "τ", "Γ", "D", "τ/Γ", "R_square", "SSE", "MSE", "RMSE"])
                p = 0
                for temp in self.data.filelist[self.Table2V].paras["双曲线拟合"]:
                    self.Table4.setItem(p, 0, QTableWidgetItem(self.Table2V))
                    self.Table4.setItem(p, 1, QTableWidgetItem(str(temp.cutstartnumspot1)))
                    self.Table4.setItem(p, 2, QTableWidgetItem(str(temp.cutendnumspot1)))
                    self.Table4.setItem(p, 3, QTableWidgetItem(str(round(temp.Max, 2))))
                    if temp.fitweightindex==1:
                        self.Table4.setItem(p, 4, QTableWidgetItem(str("1/y")))
                    elif temp.fitweightindex==2:
                        self.Table4.setItem(p, 4, QTableWidgetItem(str("子矩阵方差")))
                    else:
                        self.Table4.setItem(p, 4, QTableWidgetItem(str("1")))
                    self.Table4.setItem(p, 5, QTableWidgetItem(str(round(temp.para[0], 2))+"±"+str(round(temp.para_error[0], 5))))
                    self.Table4.setItem(p, 6, QTableWidgetItem(str(round(temp.para[1], 2))+"±"+str(round(temp.para_error[1], 5))))
                    self.Table4.setItem(p, 7, QTableWidgetItem(str(round(temp.para[2], 2))+"±"+str(round(temp.para_error[2], 5))))
                    self.Table4.setItem(p, 8, QTableWidgetItem(str(round(temp.para[3], 2))+"±"+str(round(temp.para_error[3], 5))))
                    self.Table4.setItem(p, 9, QTableWidgetItem(str(round(temp.para[1] / temp.para[2], 2))))
                    self.Table4.setItem(p, 10, QTableWidgetItem(str(round(temp.R2[0], 5))))
                    self.Table4.setItem(p, 11, QTableWidgetItem(str(round(temp.R2[1], 5))))
                    self.Table4.setItem(p, 12, QTableWidgetItem(str(round(temp.R2[2], 5))))
                    self.Table4.setItem(p, 13, QTableWidgetItem(str(round(temp.R2[3], 5))))
                    self.Table4.item(p, 5).setBackground(QBrush(QColor(205, 155, 155)))
                    self.Table4.item(p, 6).setBackground(QBrush(QColor(205, 155, 155)))
                    self.Table4.item(p, 7).setBackground(QBrush(QColor(205, 155, 155)))
                    self.Table4.item(p, 8).setBackground(QBrush(QColor(205, 155, 155)))
                    self.Table4.item(p, 9).setBackground(QBrush(QColor(205, 155, 155)))
                    # self.Table4.item(p, 7).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table4.item(p, 8).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table4.item(p, 9).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table4.item(p, 10).setBackground(QBrush(QColor(99, 196, 47)))
                    p += 1
            if (self.data.filelist[self.Table2V].paras["指数拟合"] != []):
                self.Table5.setColumnCount(11)
                self.Table5.setRowCount(len(self.data.filelist[self.Table2V].paras["指数拟合"]))
                self.Table5.setHorizontalHeaderLabels(
                    ["文件名", "前截点", "后截点", "Max", "拟合权重", "I_0", "τ", "D", "R_square", "SSE", "MSE", "RMSE"])
                p = 0
                for temp in self.data.filelist[self.Table2V].paras["指数拟合"]:
                    self.Table5.setItem(p, 0, QTableWidgetItem(self.Table2V))
                    self.Table5.setItem(p, 1, QTableWidgetItem(str(temp.cutstartnumspot1)))
                    self.Table5.setItem(p, 2, QTableWidgetItem(str(temp.cutendnumspot1)))
                    self.Table5.setItem(p, 3, QTableWidgetItem(str(round(temp.Max, 2))))
                    if temp.fitweightindex == 1:
                        self.Table5.setItem(p, 4, QTableWidgetItem(str("1/y")))
                    elif temp.fitweightindex == 2:
                        self.Table5.setItem(p, 4, QTableWidgetItem(str("子矩阵方差")))
                    else:
                        self.Table5.setItem(p, 4, QTableWidgetItem(str("1")))
                    self.Table5.setItem(p, 5, QTableWidgetItem(str(round(temp.para[0], 2))+"±"+str(round(temp.para_error[0], 5))))
                    self.Table5.setItem(p, 6, QTableWidgetItem(str(round(temp.para[1], 2))+"±"+str(round(temp.para_error[1], 5))))
                    self.Table5.setItem(p, 7, QTableWidgetItem(str(round(temp.para[2], 2))+"±"+str(round(temp.para_error[2], 5))))
                    self.Table5.setItem(p, 8, QTableWidgetItem(str(round(temp.R2[0], 5))))
                    self.Table5.setItem(p, 9, QTableWidgetItem(str(round(temp.R2[1], 5))))
                    self.Table5.setItem(p, 10, QTableWidgetItem(str(round(temp.R2[2], 5))))
                    self.Table5.setItem(p, 11, QTableWidgetItem(str(round(temp.R2[3], 5))))
                    self.Table5.item(p, 5).setBackground(QBrush(QColor(124, 205, 124)))
                    self.Table5.item(p, 6).setBackground(QBrush(QColor(124, 205, 124)))
                    self.Table5.item(p, 7).setBackground(QBrush(QColor(124, 205, 124)))
                    # self.Table5.item(p, 6).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table5.item(p, 7).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table5.item(p, 8).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table5.item(p, 9).setBackground(QBrush(QColor(99, 196, 47)))

                    p += 1
            if (self.data.filelist[self.Table2V].paras["双曲线积分拟合"] != []):
                self.Table8.setColumnCount(14)
                self.Table8.setRowCount(len(self.data.filelist[self.Table2V].paras["双曲线积分拟合"]))
                self.Table8.setHorizontalHeaderLabels(
                    ["文件名", "前截点", "后截点", "Max", "拟合权重","I_0", "τ", "Γ", "D", "τ/Γ", "R_square", "SSE", "MSE", "RMSE"])
                p = 0
                for temp in self.data.filelist[self.Table2V].paras["双曲线积分拟合"]:
                    self.Table8.setItem(p, 0, QTableWidgetItem(self.Table2V))
                    self.Table8.setItem(p, 1, QTableWidgetItem(str(temp.cutstartnumspot1)))
                    self.Table8.setItem(p, 2, QTableWidgetItem(str(temp.cutendnumspot1)))
                    self.Table8.setItem(p, 3, QTableWidgetItem(str(round(temp.Max, 2))))
                    if temp.fitweightindex==1:
                        self.Table8.setItem(p, 4, QTableWidgetItem(str("1/y")))
                    elif temp.fitweightindex==2:
                        self.Table8.setItem(p, 4, QTableWidgetItem(str("子矩阵方差")))
                    else:
                        self.Table8.setItem(p, 4, QTableWidgetItem(str("1")))
                    self.Table8.setItem(p, 5, QTableWidgetItem(str(round(temp.para[0], 2))+"±"+str(round(temp.para_error[0], 5))))
                    self.Table8.setItem(p, 6, QTableWidgetItem(str(round(temp.para[1], 2))+"±"+str(round(temp.para_error[1], 5))))
                    self.Table8.setItem(p, 7, QTableWidgetItem(str(round(temp.para[2], 2))+"±"+str(round(temp.para_error[2], 5))))
                    self.Table8.setItem(p, 8, QTableWidgetItem(str(round(temp.para[3], 2))+"±"+str(round(temp.para_error[3], 5))))
                    self.Table8.setItem(p, 9, QTableWidgetItem(str(round(temp.para[1] / temp.para[2], 2))))
                    self.Table8.setItem(p, 10, QTableWidgetItem(str(round(temp.R2[0], 5))))
                    self.Table8.setItem(p, 11, QTableWidgetItem(str(round(temp.R2[1], 5))))
                    self.Table8.setItem(p, 12, QTableWidgetItem(str(round(temp.R2[2], 5))))
                    self.Table8.setItem(p, 13, QTableWidgetItem(str(round(temp.R2[3], 5))))
                    self.Table8.item(p, 5).setBackground(QBrush(QColor(205, 155, 155)))
                    self.Table8.item(p, 6).setBackground(QBrush(QColor(205, 155, 155)))
                    self.Table8.item(p, 7).setBackground(QBrush(QColor(205, 155, 155)))
                    self.Table8.item(p, 8).setBackground(QBrush(QColor(205, 155, 155)))
                    self.Table8.item(p, 9).setBackground(QBrush(QColor(205, 155, 155)))
                    # self.Table8.item(p, 7).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table8.item(p, 8).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table8.item(p, 9).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table8.item(p, 10).setBackground(QBrush(QColor(99, 196, 47)))
                    p += 1
            if (self.data.filelist[self.Table2V].paras["指数积分拟合"] != []):
                self.Table9.setColumnCount(11)
                self.Table9.setRowCount(len(self.data.filelist[self.Table2V].paras["指数积分拟合"]))
                self.Table9.setHorizontalHeaderLabels(
                    ["文件名", "前截点", "后截点", "Max", "拟合权重", "I_0", "τ", "D", "R_square", "SSE", "MSE", "RMSE"])
                p = 0
                for temp in self.data.filelist[self.Table2V].paras["指数积分拟合"]:
                    self.Table9.setItem(p, 0, QTableWidgetItem(self.Table2V))
                    self.Table9.setItem(p, 1, QTableWidgetItem(str(temp.cutstartnumspot1)))
                    self.Table9.setItem(p, 2, QTableWidgetItem(str(temp.cutendnumspot1)))
                    self.Table9.setItem(p, 3, QTableWidgetItem(str(round(temp.Max, 2))))
                    if temp.fitweightindex == 1:
                        self.Table9.setItem(p, 4, QTableWidgetItem(str("1/y")))
                    elif temp.fitweightindex == 2:
                        self.Table9.setItem(p, 4, QTableWidgetItem(str("子矩阵方差")))
                    else:
                        self.Table9.setItem(p, 4, QTableWidgetItem(str("1")))
                    self.Table9.setItem(p, 5, QTableWidgetItem(str(round(temp.para[0], 2))+"±"+str(round(temp.para_error[0], 5))))
                    self.Table9.setItem(p, 6, QTableWidgetItem(str(round(temp.para[1], 2))+"±"+str(round(temp.para_error[1], 5))))
                    self.Table9.setItem(p, 7, QTableWidgetItem(str(round(temp.para[2], 2))+"±"+str(round(temp.para_error[2], 5))))
                    self.Table9.setItem(p, 8, QTableWidgetItem(str(round(temp.R2[0], 5))))
                    self.Table9.setItem(p, 9, QTableWidgetItem(str(round(temp.R2[1], 5))))
                    self.Table9.setItem(p, 10, QTableWidgetItem(str(round(temp.R2[2], 5))))
                    self.Table9.setItem(p, 11, QTableWidgetItem(str(round(temp.R2[3], 5))))
                    self.Table9.item(p, 5).setBackground(QBrush(QColor(124, 205, 124)))
                    self.Table9.item(p, 6).setBackground(QBrush(QColor(124, 205, 124)))
                    self.Table9.item(p, 7).setBackground(QBrush(QColor(124, 205, 124)))
                    # self.Table9.item(p, 6).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table9.item(p, 7).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table9.item(p, 8).setBackground(QBrush(QColor(99, 196, 47)))
                    # self.Table9.item(p, 9).setBackground(QBrush(QColor(99, 196, 47)))

                    p += 1

    #此处修改对比图
    def Table4VerticalHeaderClick(self, index):
        print("Table4VerticalHeaderClick")
        self.FigtabWidget.setCurrentIndex(0)
        self.figure.fig.canvas.draw_idle()
        self.figure.axes.clear()
        # plt.grid()

        numstart1 = self.data.filelist[self.Table2V].paras["双曲线拟合"][index].cutstartnum1
        numend1 = self.data.filelist[self.Table2V].paras["双曲线拟合"][index].cutendnum1
        title = self.Table2V + "文件前截" + str(
            self.data.filelist[self.Table2V].paras["双曲线拟合"][index].cutstartnumspot1) + "个点-后截" + str(
            self.data.filelist[self.Table2V].paras["双曲线拟合"][index].cutendnumspot1) + "个点的双曲线拟合图"
        self.figure.fig.canvas.draw_idle()
        self.figure.axes.clear()

        if (self.showcut == 0):
            self.figure.axes.plot(self.data.filelist[self.Table2V].Pro_Data1_X[0:numstart1 + 1],
                                  self.data.filelist[self.Table2V].Pro_Data1[0:numstart1 + 1], "--",
                                  color="green")  # 前半段
            self.figure.axes.plot(self.data.filelist[self.Table2V].Pro_Data1_X[numend1:],
                                  self.data.filelist[self.Table2V].Pro_Data1[numend1:], "--", color="green")  # 后半段段

            self.figure.axes.scatter(self.data.filelist[self.Table2V].Pro_Data1_X[0:numstart1 + 1],
                                     self.data.filelist[self.Table2V].Pro_Data1[0:numstart1 + 1], color="green",
                                     alpha=0.3)  # 前半段
            self.figure.axes.scatter(self.data.filelist[self.Table2V].Pro_Data1_X[numend1:],
                                     self.data.filelist[self.Table2V].Pro_Data1[numend1:], color="green",
                                     alpha=0.3)  # 后半段段

        # 原始曲线

        self.figure.axes.plot(self.data.filelist[self.Table2V].Pro_Data1_X[numstart1:numend1 + 1],
                              self.data.filelist[self.Table2V].Pro_Data1[numstart1:numend1 + 1], color="blue")  # 中段

        # 原始散点
        self.figure.axes.scatter(self.data.filelist[self.Table2V].Pro_Data1_X[numstart1:numend1 + 1],
                                 self.data.filelist[self.Table2V].Pro_Data1[numstart1:numend1 + 1], color="blue",
                                 alpha=0.3)

        try:
            self.figure.axes.plot(self.data.filelist[self.Table2V].paras["双曲线拟合"][index].fitx,
                                  self.data.filelist[self.Table2V].paras["双曲线拟合"][index].fity, color="red")

        except Exception as a:
            print(a)
        # self.figure.axes.scatter(self.data.filelist[filename].Cut_Data1_X,self.data.filelist[filename].Cut_Data1, alpha=0.3)
        self.figure.axes.grid()
        self.figure.axes.set_ylabel("cps")
        self.figure.axes.set_xlabel("t")
        self.figure.axes.set_title(title)
        self.imagen2Name = title
        self.figure.axes.legend()

    def Table5VerticalHeaderClick(self, index):
        print("Table5VerticalHeaderClick")
        self.FigtabWidget.setCurrentIndex(1)
        self.figure2.fig.canvas.draw_idle()
        self.figure2.axes.clear()
        # plt.grid()
        title = ""
        numstart1 = self.data.filelist[self.Table2V].paras["指数拟合"][index].cutstartnum1
        numend1 = self.data.filelist[self.Table2V].paras["指数拟合"][index].cutendnum1
        title = self.Table2V + "文件前截" + str(self.data.filelist[self.Table2V].paras["指数拟合"][
                                                index].cutstartnumspot1) + "个点-后截" + str(
            self.data.filelist[self.Table2V].paras["指数拟合"][
                index].cutendnumspot1) + "个点的指数拟合图"
        self.figure2.fig.canvas.draw_idle()
        self.figure2.axes.clear()
        # 原始曲线
        if (self.showcut == 0):
            self.figure2.axes.plot(self.data.filelist[self.Table2V].Pro_Data1_X[0:numstart1 + 1],
                                   self.data.filelist[self.Table2V].Pro_Data1[0:numstart1 + 1], "--",
                                   color="green")  # 前半段
            self.figure2.axes.plot(self.data.filelist[self.Table2V].Pro_Data1_X[numend1:],
                                   self.data.filelist[self.Table2V].Pro_Data1[numend1:], "--", color="green")  # 后半段段

            self.figure2.axes.scatter(self.data.filelist[self.Table2V].Pro_Data1_X[0:numstart1 + 1],
                                      self.data.filelist[self.Table2V].Pro_Data1[0:numstart1 + 1], color="green",
                                      alpha=0.3)  # 前半段
            self.figure2.axes.scatter(self.data.filelist[self.Table2V].Pro_Data1_X[numend1:],
                                      self.data.filelist[self.Table2V].Pro_Data1[numend1:], color="green",
                                      alpha=0.3)  # 后半段段

        # 原始曲线

        self.figure2.axes.plot(self.data.filelist[self.Table2V].Pro_Data1_X[numstart1:numend1 + 1],
                               self.data.filelist[self.Table2V].Pro_Data1[numstart1:numend1 + 1], color="blue")  # 中段

        # 原始散点
        self.figure2.axes.scatter(self.data.filelist[self.Table2V].Pro_Data1_X[numstart1:numend1 + 1],
                                  self.data.filelist[self.Table2V].Pro_Data1[numstart1:numend1 + 1], color="blue",
                                  alpha=0.3)

        try:
            self.figure2.axes.plot(self.data.filelist[self.Table2V].paras["指数拟合"][index].fitx,
                                   self.data.filelist[self.Table2V].paras["指数拟合"][index].fity, color="red")

        except Exception as a:
            print(a)
        # self.figure2.axes.scatter(self.data.filelist[filename].Cut_Data1_X,self.data.filelist[filename].Cut_Data1, alpha=0.3)
        self.figure2.axes.grid()
        self.figure2.axes.set_ylabel("cps")
        self.figure2.axes.set_xlabel("t")
        self.figure2.axes.set_title(title)
        self.imagen2Name = title
        self.figure2.axes.legend()

    def Table8VerticalHeaderClick(self, index):
        print("Table8VerticalHeaderClick")
        self.FigtabWidget.setCurrentIndex(2)
        self.figure6.fig.canvas.draw_idle()
        self.figure6.axes.clear()
        # plt.grid()

        numstart1 = self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].cutstartnum1
        numend1 = self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].cutendnum1
        title = self.Table2V + "文件前截" + str(
            self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].cutstartnumspot1) + "个点-后截" + str(
            self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].cutendnumspot1) + "个点的双曲线积分拟合图"
        self.figure6.fig.canvas.draw_idle()
        self.figure6.axes.clear()

        if (self.showcut == 0):

            self.figure6.axes.plot(self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].xfit[0:numstart1 + 1],
                                  self.data.filelist[self.Table2V].Pro_Data1[0:numstart1 + 1], "--",
                                  color="green")  # 前半段
            self.figure6.axes.plot(self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].xfit[numend1:],
                                  self.data.filelist[self.Table2V].Pro_Data1[numend1:], "--", color="green")  # 后半段段

            self.figure6.axes.scatter(self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].xfit[0:numstart1 + 1],
                                     self.data.filelist[self.Table2V].Pro_Data1[0:numstart1 + 1], color="green",
                                     alpha=0.3)  # 前半段
            self.figure6.axes.scatter(self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].xfit[numend1:],
                                     self.data.filelist[self.Table2V].Pro_Data1[numend1:], color="green",
                                     alpha=0.3)  # 后半段段

        # 原始曲线

        self.figure6.axes.plot(self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].xfit[numstart1:numend1 + 1],
                              self.data.filelist[self.Table2V].Pro_Data1[numstart1:numend1 + 1], color="blue")  # 中段

        # 原始散点
        self.figure6.axes.scatter(self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].xfit[numstart1:numend1 + 1],
                                 self.data.filelist[self.Table2V].Pro_Data1[numstart1:numend1 + 1], color="blue",
                                 alpha=0.3)

        try:
            self.figure6.axes.plot(self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].fitx,
                                  self.data.filelist[self.Table2V].paras["双曲线积分拟合"][index].fity, color="red")

        except Exception as a:
            print(a)
        # self.figure.axes.scatter(self.data.filelist[filename].Cut_Data1_X,self.data.filelist[filename].Cut_Data1, alpha=0.3)
        self.figure6.axes.grid()
        self.figure6.axes.set_ylabel("cps")
        self.figure6.axes.set_xlabel("t")
        self.figure6.axes.set_title(title)
        self.imagen2Name = title
        self.figure6.axes.legend()

    def Table9VerticalHeaderClick(self, index):
        print("Table5VerticalHeaderClick")
        self.FigtabWidget.setCurrentIndex(3)
        self.figure7.fig.canvas.draw_idle()
        self.figure7.axes.clear()
        # plt.grid()
        title = ""
        numstart1 = self.data.filelist[self.Table2V].paras["指数积分拟合"][index].cutstartnum1
        numend1 = self.data.filelist[self.Table2V].paras["指数积分拟合"][index].cutendnum1
        title = self.Table2V + "文件前截" + str(self.data.filelist[self.Table2V].paras["指数积分拟合"][
                                                index].cutstartnumspot1) + "个点-后截" + str(
            self.data.filelist[self.Table2V].paras["指数积分拟合"][
                index].cutendnumspot1) + "个点的指数拟合图"
        self.figure7.fig.canvas.draw_idle()
        self.figure7.axes.clear()
        # 原始曲线
        if (self.showcut == 0):
            self.figure7.axes.plot(self.data.filelist[self.Table2V].paras["指数积分拟合"][index].xfit[0:numstart1 + 1],
                                   self.data.filelist[self.Table2V].Pro_Data1[0:numstart1 + 1], "--",
                                   color="green")  # 前半段
            self.figure7.axes.plot(self.data.filelist[self.Table2V].paras["指数积分拟合"][index].xfit[numend1:],
                                   self.data.filelist[self.Table2V].Pro_Data1[numend1:], "--", color="green")  # 后半段段

            self.figure7.axes.scatter(self.data.filelist[self.Table2V].paras["指数积分拟合"][index].xfit[0:numstart1 + 1],
                                      self.data.filelist[self.Table2V].Pro_Data1[0:numstart1 + 1], color="green",
                                      alpha=0.3)  # 前半段
            self.figure7.axes.scatter(self.data.filelist[self.Table2V].paras["指数积分拟合"][index].xfit[numend1:],
                                      self.data.filelist[self.Table2V].Pro_Data1[numend1:], color="green",
                                      alpha=0.3)  # 后半段段

        # 原始曲线

        self.figure7.axes.plot(self.data.filelist[self.Table2V].paras["指数积分拟合"][index].xfit[numstart1:numend1 + 1],
                               self.data.filelist[self.Table2V].Pro_Data1[numstart1:numend1 + 1], color="blue")  # 中段

        # 原始散点
        self.figure7.axes.scatter(self.data.filelist[self.Table2V].paras["指数积分拟合"][index].xfit[numstart1:numend1 + 1],
                                  self.data.filelist[self.Table2V].Pro_Data1[numstart1:numend1 + 1], color="blue",
                                  alpha=0.3)

        try:
            self.figure7.axes.plot(self.data.filelist[self.Table2V].paras["指数拟合"][index].fitx,
                                   self.data.filelist[self.Table2V].paras["指数拟合"][index].fity, color="red")

        except Exception as a:
            print(a)
        # self.figure2.axes.scatter(self.data.filelist[filename].Cut_Data1_X,self.data.filelist[filename].Cut_Data1, alpha=0.3)
        self.figure7.axes.grid()
        self.figure7.axes.set_ylabel("cps")
        self.figure7.axes.set_xlabel("t")
        self.figure7.axes.set_title(title)
        self.imagen2Name = title
        self.figure7.axes.legend()

    def table7clicked(self,index:QModelIndex):
        path=self.historydata[index.row()]
        print(path)
        if (index.row()==0):
            return

        if(not os.path.exists(path)):
            self.statusBar().showMessage("此文件夹已删除，请重新选择！")
            self.historydata.pop(index.row())
            self.Table7.clear()
            self.Table7.addItems(self.historydata)
            return
        # self.uploadinfthread=UploadClient(path)
        # self.uploadinfthread.start()
        if (os.path.exists(path + "/" + os.path.basename(path) + ".data")):
            # 有历史数据
            # self.inpath = path
            self.thraedreadhistory = readhistory(path + "/" + os.path.basename(path) + ".data")
            self.thraedreadhistory.sinOuttext.connect(self.updatestatusbar)
            self.thraedreadhistory.sinOutoutEndThread.connect(self.updatareadhistory)
            self.thraedreadhistory.start()
        else:
            # 无历史数据
            self.fitComboBox.clear()
            self.fitComboBox.addItems(["批量拟合"])
            self.inLineEdit.blockSignals(True)
            self.inLineEdit.setText(path)
            self.inLineEdit.blockSignals(False)
            # self.inpath = path
            self.outpath = path + "/预处理后的数据"
            self.outLineEdit.blockSignals(True)
            self.outLineEdit.setText(self.outpath)
            self.outLineEdit.blockSignals(False)
            self.threadread = readthread(path)
            # self.threadread.sinOutoutpath.connect(self.updatepath)
            self.threadread.sinOuttext.connect(self.updatestatusbar)
            self.threadread.sinOutpro.connect(self.updatepro)
            self.threadread.sinOutoutEndThread.connect(self.updateData)
            self.threadread.sinOutoutEndThread.connect(self.savedatafileButtonclicked)
            self.threadread.sinOutbool.connect(self.provisible)
            # self.threadread.sinOutoutData.connect(self.updateData)
            self.threadread.start()
        self.addhistorydata(path)

    def cutshowchange(self, index):
        print("cutshowchange")
        self.showcut = index
        self.data.showcut=index


    def featurexchange(self, index):
        print("featurexchange")
        self.featurex = index
        self.data.featurex = index

    def fitweightComboBoxindexchanged(self,index):
        print("fitweightComboBoxindexchanged")
        self.fitweightindex = index
        self.data.fitweightindex = index

    def ChangedcutComboBoxstart(self, index):
        pass

    def savefileButtonclicked(self):
        if (self.Table2.rowCount() > 0):
            self.savedatathread=savefilethread(self.data)
            self.savedatathread.sinOuttext.connect(self.updatestatusbar)
            self.savedatathread.sinOutpro.connect(self.updatepro)
            self.savedatathread.sinOutbool.connect(self.provisible)
            self.savedatathread.start()

            # self.data.writeXls(self.outpath)
        else:
            self.statusBar().showMessage(
                "请添加数据文件！")

    def savefilesonButtonclicked(self):
        # self.data.writesondataXls(self.outpath)
        if (self.Table2.rowCount() > 0):
            self.savesondatathread=savesondatathread(self.data)
            self.savesondatathread.sinOuttext.connect(self.updatestatusbar)
            self.savesondatathread.sinOutpro.connect(self.updatepro)
            self.savesondatathread.sinOutbool.connect(self.provisible)
            self.savesondatathread.start()
            # self.data.writeXls(self.outpath)
        else:
            self.statusBar().showMessage(
                "请添加数据文件！")

    def savefilesontxtButtonclicked(self):
        # self.data.writesondataXls(self.outpath)
        if (self.Table2.rowCount() > 0):
            self.savesondatatxtthread=savesondatatxtthread(self.data)
            self.savesondatatxtthread.sinOuttext.connect(self.updatestatusbar)
            self.savesondatatxtthread.sinOutpro.connect(self.updatepro)
            self.savesondatatxtthread.sinOutbool.connect(self.provisible)
            self.savesondatatxtthread.start()
            # self.data.writeXls(self.outpath)
        else:
            self.statusBar().showMessage(
                "请添加数据文件！")

    def savesinglefilesonButtonclicked(self):
        # self.data.writesinglefiledata(self.outpath)
        # self.data.writesondataXls(self.outpath)
        if (self.Table2.rowCount() > 0):
            self.savesondatathread=savesingledatathread(self.data)
            self.savesondatathread.sinOuttext.connect(self.updatestatusbar)
            self.savesondatathread.sinOutpro.connect(self.updatepro)
            self.savesondatathread.sinOutbool.connect(self.provisible)
            self.savesondatathread.start()
            # self.data.writeXls(self.outpath)
        else:
            self.statusBar().showMessage(
                "请添加数据文件！")




    def savedatafileButtonclicked(self):
        print("savedatafileButtonclicked")
        try:
            # print("self.data.inpath:",self.data.inpath)
            if(self.data.inpath!=""):
                self.statusBar().showMessage(
                    "正在保存当前状态...")
                # self.data.inpath = self.inpath
                self.data.outpath = self.outpath
                self.data.imagen1Name = self.imagen1Name
                self.data.imagen2Name = self.imagen2Name
                self.data.imagen6Name = self.imagen6Name
                self.data.imagen7Name = self.imagen7Name
                self.data.Table2V = self.Table2V
                self.data.Table2H = self.Table2H
                self.data.showcut = self.showcut
                self.data.featurex = self.featurex
                self.data.b1low = self.b1low
                self.data.b1top = self.b1top
                self.data.b2low = self.b2low
                self.data.b2top = self.b2top
                # print("self.cb1.isChecked",int(self.cb1.isChecked()))
                # print("self.cb2.isChecked",int(self.cb2.isChecked()))
                self.data.cb1setChecked=int(self.cb1.isChecked())
                self.data.cb2setChecked=int(self.cb2.isChecked())
                # self.data.currentimage1=self.figure.fig
                # self.data.currentimage2=self.figure2.fig
                # self.data.currentimage3=self.figure3.fig
                # self.data.currentimage4=self.figure4.fig
                # self.data.currentimage5,ax=self.figure5.axes
                self.data.fitComboBoxtext = self.fitComboBox.currentText()
                self.data.cutComboBoxstarttext = self.cutComboBoxstart.currentText()
                self.data.cutComboBoxendtext = self.cutComboBoxend.currentText()
                self.savehistory=savehistory(self.data.inpath,self.data)
                self.savehistory.sinOuttext.connect(self.updatestatusbar)
                self.savehistory.start()



        except Exception as a:
            print(a)
            traceback.print_exc()



    def saveImage1Buttonlicked(self):
        if (not os.path.exists(self.outpath + "/双曲线图片文件/")):
            os.makedirs(self.outpath + "/双曲线图片文件/")

        if (self.imagen1Name != ""):
            self.figure.axes.get_figure().savefig(self.outpath + "/双曲线图片文件/" + self.imagen1Name + ".png")
            self.statusBar().showMessage(
                "图片成功保存到" + self.outpath + "/双曲线图片文件/" + self.imagen1Name + ".png")
        else:
            self.statusBar().showMessage(
                "无图片！")

    def saveImage2Buttonlicked(self):
        if (not os.path.exists(self.outpath + "/指数图片文件/")):
            os.makedirs(self.outpath + "/指数图片文件/")
        if (self.imagen2Name != ""):
            self.figure2.axes.get_figure().savefig(self.outpath + "/指数图片文件/" + self.imagen2Name + ".png")
            self.statusBar().showMessage(
                "图片成功保存到" + self.outpath + "/指数图片文件/" + self.imagen2Name + ".png")
        else:
            self.statusBar().showMessage(
                "无图片！")

    def saveImage3Buttonlicked(self):
        if (not os.path.exists(self.outpath + "/参数图片文件/")):
            os.makedirs(self.outpath + "/参数图片文件/")
        if (self.imagen3Name != ""):
            self.figure3.axes.get_figure().savefig(self.outpath + "/参数图片文件/" + self.imagen3Name + ".png")
            self.statusBar().showMessage(
                "图片成功保存到" + self.outpath + "/参数图片文件/" + self.imagen3Name + ".png")
        else:
            self.statusBar().showMessage(
                "无图片！")

    def saveImage4Buttonlicked(self):
        if (not os.path.exists(self.outpath + "/概率分布图片文件/")):
            os.makedirs(self.outpath + "/概率分布图片文件/")
        if (self.imagen4Name != ""):
            self.figure4.axes.get_figure().savefig(self.outpath + "概率分布图片文件/" + self.imagen4Name + ".png")
            self.statusBar().showMessage(
                "图片成功保存到" + self.outpath + "/概率分布图片文件/" + self.imagen4Name + ".png")
        else:
            self.statusBar().showMessage(
                "无图片！")

    def saveImage5Buttonlicked(self):
        if (not os.path.exists(self.outpath + "/对比图片文件/")):
            os.makedirs(self.outpath + "/对比图片文件/")
        if (self.imagen5Name != ""):
            self.figure5.axes.get_figure().savefig(self.outpath + "/对比图片文件/" + self.imagen5Name + ".png")
            self.statusBar().showMessage(
                "图片成功保存到" + self.outpath + "/对比图片文件/" + self.imagen5Name + ".png")
        else:
            self.statusBar().showMessage(
                "无图片！")

    def fitButtonlicked(self):
        print("fitButtonlicked in")
        # try:
        if(self.data==""):
            self.statusBar().showMessage(
                "请先读取数据！")
        if self.data == "":
            return
        title = ""
        startnum = int(self.cutComboBoxstart.currentText())
        endnum = int(self.cutComboBoxend.currentText())
        if (self.fitComboBox.currentText() != "批量拟合"):
            # self.statusBar().showMessage("开始进行批量数据拟合...")
            index = self.fitComboBox.currentText().find("]")
            title = self.fitComboBox.currentText()[(index + 1):]
            # print(title)
        temppara=[]
        if (self.cb1.isChecked()):
            temppara.append([1, self.cb1ComboBoxstart.currentText(), startnum, endnum, title, self.b1low, self.b1top,
                              self.b2low, self.b2top,self.fitweightindex])
        if (self.cb2.isChecked()):
            temppara.append([2, self.cb2ComboBoxstart.currentText(), startnum, endnum, title, self.b1low, self.b1top,
                              self.b2low, self.b2top,self.fitweightindex])
        if (self.cb3.isChecked()):
            temppara.append([3, self.cb3ComboBoxstart.currentText(), startnum, endnum, title, self.b1low, self.b1top,
                              self.b2low, self.b2top,self.fitweightindex])
        if (self.cb4.isChecked()):
            temppara.append([4, self.cb4ComboBoxstart.currentText(), startnum, endnum, title, self.b1low, self.b1top,
                              self.b2low, self.b2top,self.fitweightindex])
        # print(len(self.data.filelist))
        self.threadfit = fitthread(self.data, temppara)
        self.threadfit.sinOutoutfitEndThread.connect(self.updatefitdata)
        self.threadfit.sinOutoutfitEndThread.connect(self.savedatafileButtonclicked)
        self.threadfit.sinOutpro.connect(self.updatepro)
        self.threadfit.sinOuttext.connect(self.updatestatusbar)
        self.threadfit.sinOutbool.connect(self.provisible)
        self.threadfit.start()

    def deletedataButtonclicked(self):
        print("deletedataButtonclicked")
        rows=[indext.row() for indext in self.Table2.verticalHeader().selectionModel().selectedIndexes()]
        rows=set(rows)
        names=[self.Table2.item(key, 0).text() for key in rows]
        for name in names:
            self.data.filenames.remove(name)
            del self.data.filelist[name]

        self.updatefitdata()
        self.savedatafileButtonclicked()
        self.statusBar().showMessage(
            '已移除' + str(len(rows)) + '条数据!')
        self.fitComboBox.clear()
        self.fitComboBox.addItems(["批量拟合"])

    def getMeandataclicked(self):
        self.threadgetMean = getMeanthread(self.data)
        self.threadgetMean.sinOutoutfitEndThread.connect(self.updatefitdata)
        self.threadgetMean.sinOutoutfitEndThread.connect(self.savedatafileButtonclicked)
        self.threadgetMean.sinOutoutfitEndThread.connect(self.fitMeandata)
        self.threadgetMean.sinOuttext.connect(self.updatestatusbar)
        self.threadgetMean.sinOutbool.connect(self.provisible)
        self.threadgetMean.start()


    def fitMeandata(self):
        title=self.data.filenames[-1]
        startnum = int(self.cutComboBoxstart.currentText())
        endnum = int(self.cutComboBoxend.currentText())
        temppara = []
        if (self.cb1.isChecked()):
            temppara.append([1, self.cb1ComboBoxstart.currentText(), startnum, endnum, title, self.b1low, self.b1top,
                             self.b2low, self.b2top, self.fitweightindex])
        if (self.cb2.isChecked()):
            temppara.append([2, self.cb2ComboBoxstart.currentText(), startnum, endnum, title, self.b1low, self.b1top,
                             self.b2low, self.b2top, self.fitweightindex])
        if (self.cb3.isChecked()):
            temppara.append([3, self.cb3ComboBoxstart.currentText(), startnum, endnum, title, self.b1low, self.b1top,
                             self.b2low, self.b2top, self.fitweightindex])
        if (self.cb4.isChecked()):
            temppara.append([4, self.cb4ComboBoxstart.currentText(), startnum, endnum, title, self.b1low, self.b1top,
                             self.b2low, self.b2top, self.fitweightindex])
        # print(len(self.data.filelist))
        self.threadfitMean = fitthread(self.data, temppara)
        self.threadfitMean.sinOutoutfitEndThread.connect(self.updatefitdata)
        self.threadfitMean.sinOutoutfitEndThread.connect(self.savedatafileButtonclicked)
        self.threadfitMean.sinOutpro.connect(self.updatepro)
        self.threadfitMean.sinOuttext.connect(self.updatestatusbar)
        self.threadfitMean.sinOutbool.connect(self.provisible)
        self.threadfitMean.start()





    def backdataclicked(self):
        # print("self.data.inpath:",self.data.inpath)
        datapath = self.data.inpath + "/" + os.path.basename(self.data.inpath) + ".data"
        # print(datapath)
        if os.path.exists(datapath):
            os.remove(datapath)
            # 无历史数据
            self.fitComboBox.clear()
            self.fitComboBox.addItems(["批量拟合"])
            self.inLineEdit.blockSignals(True)
            self.inLineEdit.setText(self.data.inpath)
            self.inLineEdit.blockSignals(False)
            # self.inpath = self.data.inpath
            self.outpath = self.data.inpath + "/预处理后的数据"
            self.outLineEdit.blockSignals(True)
            self.outLineEdit.setText(self.outpath)
            self.outLineEdit.blockSignals(False)
            self.threadread = readthread(self.data.inpath)
            # self.threadread.sinOutoutpath.connect(self.updatepath)
            self.threadread.sinOuttext.connect(self.updatestatusbar)
            self.threadread.sinOutpro.connect(self.updatepro)
            self.threadread.sinOutoutEndThread.connect(self.updateData)
            self.threadread.sinOutoutEndThread.connect(self.savedatafileButtonclicked)
            self.threadread.sinOutbool.connect(self.provisible)
            # self.threadread.sinOutoutData.connect(self.updateData)
            self.threadread.start()

    def generateMenu2(self, pos):
        # print("generateMenu2")
        row_num = -1
        # fittype = QListWidgetItem(self.listwidget2.currentItem()).text()
        # filename = QListWidgetItem(self.listwidget1.currentItem()).text()
        rowlabel = str(self.Table2.currentIndex().row() + 1)
        collabel = str(self.Table2.horizontalHeaderItem(self.Table2.currentIndex().column()).text())
        # collabel=self.listwidget3.takeHorizontalHeaderItem(self.listwidget3.currentIndex().column()).text()
        currtext = self.Table2.currentItem().text()

        for i in self.Table2.selectionModel().selection().indexes():
            row_num = i.row()

        if row_num < self.Table2.rowCount():
            menu = QMenu()
            # item1 = menu.addAction("复制单元格["+rowlabel+","+collabel+"]"+currtext)
            item1 = menu.addAction('复制单元格内容->' + currtext)
            item2 = menu.addAction('复制当前行(带文件名)->[' + rowlabel + ']')
            item3 = menu.addAction('复制当前列(带列名)->[' + collabel + ']')
            item4 = menu.addAction('复制当前行->[' + rowlabel + ']')
            item5 = menu.addAction('复制当前列->[' + collabel + ']')
            action = menu.exec_(self.Table2.mapToGlobal(pos))
            if action == item1:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.Table2.currentItem().text())
                self.statusBar().showMessage(
                    '已复制："' + currtext + '"')
            elif action == item2:
                clipboard = QApplication.clipboard()
                text = ""
                ind = self.Table2.currentIndex().row()
                for j in range(self.Table2.columnCount()):
                    text += self.Table2.item(ind, j).text() + "\t"
                clipboard.setText(text)
                self.statusBar().showMessage(
                    '已复制:"' + self.Table2.item(self.Table2.currentIndex().row(), 0).text() + "的参数与数据(带文件名)")

            elif action == item3:
                clipboard = QApplication.clipboard()
                text = ""
                ind = self.Table2.currentIndex().column()
                text += collabel + "\t"
                for i in range(self.Table2.rowCount()):
                    text += self.Table2.item(i, ind).text() + "\t"
                clipboard.setText(text)
                self.statusBar().showMessage("已提取每组参数中的" + collabel + "列特征(带列名)")
            elif action == item4:
                clipboard = QApplication.clipboard()
                text = ""
                ind = self.Table2.currentIndex().row()
                for j in range(1, self.Table2.columnCount()):
                    text += self.Table2.item(ind, j).text() + "\t"
                clipboard.setText(text)
                self.statusBar().showMessage(
                    '已复制:"' + self.Table2.item(self.Table2.currentIndex().row(), 0).text() + "的参数与数据")
            elif action == item5:
                clipboard = QApplication.clipboard()
                text = ""
                ind = self.Table2.currentIndex().column()
                for i in range(self.Table2.rowCount()):
                    text += self.Table2.item(i, ind).text() + "\t"
                clipboard.setText(text)
                self.statusBar().showMessage("已提取每组参数中的" + collabel + "列特征")
            else:
                return

    def plotfeature(self, x, ys, title=[], xlabel="t", ylabel="cps"):
        # print("plotfeature")
        # xtamp=[]    #时间戳
        # for temp in x:
        #     xtamp.append(time.mktime(temp.timetuple()))
        ydicts = []
        if (self.featurex == 0):
            for ytemp in ys:
                # print(xtamp)
                # print(ytemp)
                try:
                    # print(list(zip(*(sorted(dict(zip(x, ytemp)).items(),key=lambda item:item[0], reverse=False)))))
                    ydict = list(zip(*(sorted(dict(zip(x, ytemp)).items(), key=lambda item: item[0], reverse=False))))
                except Exception as a:
                    print(a)

                ydicts.append(ydict)
        else:
            for i in range(len(ys)):
                xtemp = range(1, len(x) + 1)
                ydicts.append([xtemp, ys[i]])

        # print(ydicts)

        self.FigtabWidget.setCurrentIndex(2)
        titleall = "所选数据文件"
        for t in title:
            titleall += "第[" + t + "]列"
        titleall += "变化折线图"
        # if(x==[]):
        #     x=range(1,len(ys)+1)
        # print(x)
        # print(y)
        self.figure3.fig.canvas.draw_idle()
        self.figure3.axes.clear()

        for i in range(len(ydicts)):
            datacell = ydicts[i]
            # print("datacell", datacell)
            # print(title[i])
            self.figure3.axes.plot(datacell[0], datacell[1], label=title[i])
            self.figure3.axes.scatter(datacell[0], datacell[1], label=title[i], alpha=0.5)

        # for i in range(len(ys)):
        #     print(title[i])
        #     self.figure3.axes.plot(x,ys[i],label=title[i])
        #     self.figure3.axes.scatter(x,ys[i], label=title[i],alpha=0.5)
        self.figure3.axes.set_ylabel("参数值")
        if (self.featurex == 0):
            self.figure3.axes.set_xlabel("ACQ-Time")
        else:
            self.figure3.axes.set_xlabel("文件序号")
        self.figure3.axes.set_title(titleall)
        self.imagen3Name = titleall
        # self.figure.axes.xlim(x[0], x[-1])
        self.figure3.axes.grid()
        self.figure3.axes.legend()

    def plotperspot(self, x, y, title="", xlabel="t", ylabel="cps"):
        print("plotperspot")
        # self.FigtabWidget.setCurrentIndex(2)
        if (x == []):
            x = range(1, len(y) + 1)
        # print(x)
        # print(y)
        self.figure3.fig.canvas.draw_idle()
        self.figure3.axes.clear()
        self.figure3.axes.plot(x, y, color="blue")
        self.figure3.axes.scatter(x, y, color="blue", alpha=0.5)
        # pg = sns.distplot(y)
        # self.figure3.axes=pg.fig
        # self.figure3.draw()
        # self.figure3.sns.distplot(y)
        # self.figure3.axes.hist(y)
        self.figure3.axes.set_ylabel("光子数")
        self.figure3.axes.set_xlabel("点序号")
        self.figure3.axes.set_title(title)
        self.imagen3Name = title
        # self.figure.axes.xlim(x[0], x[-1])
        self.figure3.axes.grid()
        self.figure3.axes.legend()

    def plotdata(self, filenames, title="", num=-1, xlabel="t", ylabel="cps"):
        print("plotdata")

        self.figure.fig.canvas.draw_idle()
        self.figure.axes.clear()
        self.figure2.fig.canvas.draw_idle()
        self.figure2.axes.clear()
        self.figure6.fig.canvas.draw_idle()
        self.figure6.axes.clear()
        self.figure7.fig.canvas.draw_idle()
        self.figure7.axes.clear()
        self.figure5.fig.canvas.draw_idle()
        self.figure5.axes.clear()
        # 跳转Tab
        filetext = ""
        # self.FigtabWidget.setCurrentIndex(self.tabWidget.currentIndex())
        for filename in filenames:
            filetext += filename + ","

            # if ((self.data.filelist[filename].paras["指数拟合"] == []) and (
            #         self.data.filelist[filename].paras["双曲线拟合"] == [])):
            #     continue

            # if(self.data.filelist[filename].paras["双曲线拟合"]==[]):
            #     if(self.data.filelist[filename].paras["指数拟合"]==[]):
            #         pass
            #     else:
            #         self.FigtabWidget.setCurrentIndex(1)
            # else:
            #     self.FigtabWidget.setCurrentIndex(0)

            if (self.data.filelist[filename].paras["双曲线拟合"] != []):
                numstart1 = self.data.filelist[filename].paras["双曲线拟合"][num].cutstartnum1
                numend1 = self.data.filelist[filename].paras["双曲线拟合"][num].cutendnum1
                numendspot1 = self.data.filelist[filename].paras["双曲线拟合"][num].cutendnumspot1
            else:
                numstart1 = 0
                numend1 = len(self.data.filelist[filename].Pro_Data1) - 1
                numendspot1 = 0
            if (self.data.filelist[filename].paras["指数拟合"] != []):
                numstart2 = self.data.filelist[filename].paras["指数拟合"][num].cutstartnum1
                numend2 = self.data.filelist[filename].paras["指数拟合"][num].cutendnum1
                numendspot2 = self.data.filelist[filename].paras["指数拟合"][num].cutendnumspot1
            else:
                numstart2 = 0
                numend2 = len(self.data.filelist[filename].Pro_Data1) - 1
                numendspot2 = 0

            if (self.data.filelist[filename].paras["双曲线积分拟合"] != []):
                numstart3 = self.data.filelist[filename].paras["双曲线积分拟合"][num].cutstartnum1
                numend3 = self.data.filelist[filename].paras["双曲线积分拟合"][num].cutendnum1
                numendspot3 = self.data.filelist[filename].paras["双曲线积分拟合"][num].cutendnumspot1
            else:
                numstart3 = 0
                numend3 = len(self.data.filelist[filename].Pro_Data1) - 1
                numendspot3 = 0

            if (self.data.filelist[filename].paras["指数积分拟合"] != []):
                numstart4 = self.data.filelist[filename].paras["指数积分拟合"][num].cutstartnum1
                numend4 = self.data.filelist[filename].paras["指数积分拟合"][num].cutendnum1
                numendspot4 = self.data.filelist[filename].paras["指数积分拟合"][num].cutendnumspot1
            else:
                numstart4 = 0
                numend4 = len(self.data.filelist[filename].Pro_Data1) - 1
                numendspot4 = 0

            # 原始曲线中段折线
            self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[numstart1:numend1 + 1],
                                  self.data.filelist[filename].Pro_Data1[numstart1:numend1 + 1],
                                  label=filename + "文件前截" + str(numstart1) + "个点后截" + str(
                                      numendspot1) + "个点双曲线拟合图")  # 中段
            self.figure2.axes.plot(self.data.filelist[filename].Pro_Data1_X[numstart2:numend2 + 1],
                                   self.data.filelist[filename].Pro_Data1[numstart2:numend2 + 1],
                                   label=filename + "文件前截" + str(numstart1) + "个点后截" + str(
                                       numendspot2) + "个点双曲线拟合图")  # 中段

            if (self.data.filelist[filename].paras["双曲线积分拟合"] != []):
                self.figure6.axes.plot(self.data.filelist[filename].paras["双曲线积分拟合"][num].xfit[numstart3:numend3 + 1],
                                      self.data.filelist[filename].Pro_Data1[numstart3:numend3 + 1],
                                      label=filename + "文件前截" + str(numstart3) + "个点后截" + str(
                                          numendspot3) + "个点双曲线积分拟合图")  # 中段

            if (self.data.filelist[filename].paras["指数积分拟合"] != []):
                self.figure7.axes.plot(self.data.filelist[filename].paras["指数积分拟合"][num].xfit[numstart4:numend4 + 1],
                                       self.data.filelist[filename].Pro_Data1[numstart4:numend4 + 1],
                                       label=filename + "文件前截" + str(numstart4) + "个点后截" + str(
                                           numendspot4) + "个点指数积分拟合图")  # 中段

            self.figure5.axes.plot(self.data.filelist[filename].Pro_Data1_X[numstart2:numend2 + 1],
                                   self.data.filelist[filename].Pro_Data1[numstart2:numend2 + 1],
                                   label=filename + "文件前截" + str(numstart1) + "个点后截" + str(numendspot1) + "原始曲线")  # 中段

            #显示裁剪状态下 前段，后段的折线和散点
            if (self.showcut == 0):
                #折线
                self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[0:numstart1 + 1],
                                      self.data.filelist[filename].Pro_Data1[0:numstart1 + 1], "--")  # 前半段
                self.figure.axes.plot(self.data.filelist[filename].Pro_Data1_X[numend1:],
                                      self.data.filelist[filename].Pro_Data1[numend1:], "--", color="green")  # 后半段段

                self.figure2.axes.plot(self.data.filelist[filename].Pro_Data1_X[0:numstart2 + 1],
                                       self.data.filelist[filename].Pro_Data1[0:numstart2 + 1], "--")  # 前半段
                self.figure2.axes.plot(self.data.filelist[filename].Pro_Data1_X[numend2:],
                                       self.data.filelist[filename].Pro_Data1[numend2:], "--")  # 后半段段
                if (self.data.filelist[filename].paras["双曲线积分拟合"] != []):
                    self.figure6.axes.plot(self.data.filelist[filename].paras["双曲线积分拟合"][num].xfit[0:numstart3 + 1],
                                           self.data.filelist[filename].Pro_Data1[0:numstart3 + 1], "--")  # 前半段

                    self.figure6.axes.plot(self.data.filelist[filename].paras["双曲线积分拟合"][num].xfit[numend3:],
                                           self.data.filelist[filename].Pro_Data1[numend3:], "--")  # 后半段段

                if (self.data.filelist[filename].paras["指数积分拟合"] != []):
                    self.figure7.axes.plot(self.data.filelist[filename].paras["指数积分拟合"][num].xfit[0:numstart4 + 1],
                                           self.data.filelist[filename].Pro_Data1[0:numstart4 + 1], "--")  # 前半段
                    self.figure7.axes.plot(self.data.filelist[filename].paras["指数积分拟合"][num].xfit[numend4:],
                                           self.data.filelist[filename].Pro_Data1[numend4:], "--")  # 后半段段

                self.figure5.axes.plot(self.data.filelist[filename].Pro_Data1_X[0:numstart2 + 1],
                                       self.data.filelist[filename].Pro_Data1[0:numstart2 + 1], "--")  # 前半段
                self.figure5.axes.plot(self.data.filelist[filename].Pro_Data1_X[numend2:],
                                       self.data.filelist[filename].Pro_Data1[numend2:], "--")  # 后半段段

                #散点
                self.figure.axes.scatter(self.data.filelist[filename].Pro_Data1_X[0:numstart1 + 1],
                                         self.data.filelist[filename].Pro_Data1[0:numstart1 + 1], alpha=0.3)  # 前半段
                self.figure.axes.scatter(self.data.filelist[filename].Pro_Data1_X[numend1:],
                                         self.data.filelist[filename].Pro_Data1[numend1:], alpha=0.3)  # 后半段段


                self.figure2.axes.scatter(self.data.filelist[filename].Pro_Data1_X[0:numstart2 + 1],
                                          self.data.filelist[filename].Pro_Data1[0:numstart2 + 1], alpha=0.3)  # 前半段
                self.figure2.axes.scatter(self.data.filelist[filename].Pro_Data1_X[numend2:],
                                          self.data.filelist[filename].Pro_Data1[numend2:], alpha=0.3)  # 后半段段

                if (self.data.filelist[filename].paras["双曲线积分拟合"] != []):
                    self.figure6.axes.scatter(self.data.filelist[filename].paras["双曲线积分拟合"][num].xfit[0:numstart3 + 1],
                                             self.data.filelist[filename].Pro_Data1[0:numstart3 + 1], alpha=0.3)  # 前半段
                    self.figure6.axes.scatter(self.data.filelist[filename].paras["双曲线积分拟合"][num].xfit[numend3:],
                                             self.data.filelist[filename].Pro_Data1[numend3:], alpha=0.3)  # 后半段段

                if (self.data.filelist[filename].paras["指数积分拟合"] != []):
                    self.figure7.axes.scatter(self.data.filelist[filename].paras["指数积分拟合"][num].xfit[0:numstart4 + 1],
                                              self.data.filelist[filename].Pro_Data1[0:numstart4 + 1], alpha=0.3)  # 前半段
                    self.figure7.axes.scatter(self.data.filelist[filename].paras["指数积分拟合"][num].xfit[numend4:],
                                              self.data.filelist[filename].Pro_Data1[numend4:], alpha=0.3)  # 后半段段



                self.figure5.axes.scatter(self.data.filelist[filename].Pro_Data1_X[0:numstart2 + 1],
                                          self.data.filelist[filename].Pro_Data1[0:numstart2 + 1], alpha=0.3)  # 前半段
                self.figure5.axes.scatter(self.data.filelist[filename].Pro_Data1_X[numend2:],
                                          self.data.filelist[filename].Pro_Data1[numend2:], alpha=0.3)  # 后半段段

            # 原始散点
            self.figure.axes.scatter(self.data.filelist[filename].Pro_Data1_X[numstart1:numend1 + 1],
                                     self.data.filelist[filename].Pro_Data1[numstart1:numend1 + 1], alpha=0.3)

            self.figure2.axes.scatter(self.data.filelist[filename].Pro_Data1_X[numstart2:numend2 + 1],
                                      self.data.filelist[filename].Pro_Data1[numstart2:numend2 + 1], alpha=0.3)
            if (self.data.filelist[filename].paras["双曲线积分拟合"] != []):
                self.figure6.axes.scatter(self.data.filelist[filename].paras["双曲线积分拟合"][num].xfit[numstart2:numend2 + 1],
                                          self.data.filelist[filename].Pro_Data1[numstart2:numend2 + 1], alpha=0.3)
            if (self.data.filelist[filename].paras["指数积分拟合"] != []):
                self.figure7.axes.scatter(self.data.filelist[filename].paras["指数积分拟合"][num].xfit[numstart2:numend2 + 1],
                                          self.data.filelist[filename].Pro_Data1[numstart2:numend2 + 1], alpha=0.3)

            self.figure5.axes.scatter(self.data.filelist[filename].Pro_Data1_X[numstart2:numend2 + 1],
                                      self.data.filelist[filename].Pro_Data1[numstart2:numend2 + 1], alpha=0.3)

            #拟合曲线
            if (self.data.filelist[filename].paras["双曲线拟合"] != []):
                self.figure.axes.plot(self.data.filelist[filename].paras["双曲线拟合"][num].fitx,
                                      self.data.filelist[filename].paras["双曲线拟合"][num].fity, color="red")
                self.figure5.axes.plot(self.data.filelist[filename].paras["双曲线拟合"][num].fitx,
                                       self.data.filelist[filename].paras["双曲线拟合"][num].fity, color="red",
                                       label="双曲线拟合，参数(I0:" + str(
                                           round(self.data.filelist[filename].paras["双曲线拟合"][num].para[0],
                                                 2)) + ",τ:" + str(
                                           round(self.data.filelist[filename].paras["双曲线拟合"][num].para[1],
                                                 5)) + ",Γ:" + str(
                                           round(self.data.filelist[filename].paras["双曲线拟合"][num].para[2],
                                                 5)) + ",D:" + str(
                                           round(self.data.filelist[filename].paras["双曲线拟合"][num].para[3],
                                                 2)) + ",R2:" + str(
                                           round(self.data.filelist[filename].paras["双曲线拟合"][num].R2[0], 5)) + ")")

            if (self.data.filelist[filename].paras["指数拟合"] != []):
                self.figure2.axes.plot(self.data.filelist[filename].paras["指数拟合"][num].fitx,
                                       self.data.filelist[filename].paras["指数拟合"][num].fity, color="red")
                self.figure5.axes.plot(self.data.filelist[filename].paras["指数拟合"][num].fitx,
                                       self.data.filelist[filename].paras["指数拟合"][num].fity, "--", color="green",
                                       label="指数拟合，参数(I0:" + str(
                                           round(self.data.filelist[filename].paras["指数拟合"][num].para[0],
                                                 2)) + ",τ:" + str(
                                           round(self.data.filelist[filename].paras["指数拟合"][num].para[1],
                                                 5)) + ",D:" + str(
                                           round(self.data.filelist[filename].paras["指数拟合"][num].para[2],
                                                 2)) + ",R2:" + str(
                                           round(self.data.filelist[filename].paras["指数拟合"][num].R2[0], 5)) + ")")

            if (self.data.filelist[filename].paras["双曲线积分拟合"] != []):
                self.figure6.axes.plot(self.data.filelist[filename].paras["双曲线积分拟合"][num].fitx,
                                      self.data.filelist[filename].paras["双曲线积分拟合"][num].fity, color="red")
                self.figure5.axes.plot(self.data.filelist[filename].paras["双曲线积分拟合"][num].fitx,
                                       self.data.filelist[filename].paras["双曲线积分拟合"][num].fity,':', color="yellow",
                                       label="双曲线积分拟合，参数(I0:" + str(
                                           round(self.data.filelist[filename].paras["双曲线积分拟合"][num].para[0],
                                                 2)) + ",τ:" + str(
                                           round(self.data.filelist[filename].paras["双曲线积分拟合"][num].para[1],
                                                 5)) + ",Γ:" + str(
                                           round(self.data.filelist[filename].paras["双曲线积分拟合"][num].para[2],
                                                 5)) + ",D:" + str(
                                           round(self.data.filelist[filename].paras["双曲线积分拟合"][num].para[3],
                                                 2)) + ",R2:" + str(
                                           round(self.data.filelist[filename].paras["双曲线积分拟合"][num].R2[0], 5)) + ")")

            if (self.data.filelist[filename].paras["指数积分拟合"] != []):
                self.figure7.axes.plot(self.data.filelist[filename].paras["指数积分拟合"][num].fitx,
                                       self.data.filelist[filename].paras["指数积分拟合"][num].fity, color="red")
                self.figure5.axes.plot(self.data.filelist[filename].paras["指数积分拟合"][num].fitx,
                                       self.data.filelist[filename].paras["指数积分拟合"][num].fity,'-.', color="orange",
                                       label="指数积分拟合，参数(I0:" + str(
                                           round(self.data.filelist[filename].paras["指数积分拟合"][num].para[0],
                                                 2)) + ",τ:" + str(
                                           round(self.data.filelist[filename].paras["指数积分拟合"][num].para[1],
                                                 5)) + ",D:" + str(
                                           round(self.data.filelist[filename].paras["指数积分拟合"][num].para[2],
                                                 2)) + ",R2:" + str(
                                           round(self.data.filelist[filename].paras["指数积分拟合"][num].R2[0], 5)) + ")")



            # self.figure.axes.scatter(self.data.filelist[filename].Cut_Data1_X,self.data.filelist[filename].Cut_Data1, alpha=0.3)
        filetext1 = filetext + "双曲线拟合图"
        filetext2 = filetext + "指数拟合图"
        filetext6 = filetext + "双曲线积分拟合图"
        filetext7 = filetext + "指数积分拟合图"
        filetext3 = filetext + "双曲线拟合-指数拟合对比图-双曲线积分拟合图-指数积分拟合对比图"

        self.figure.axes.legend()
        self.figure.axes.grid()
        self.figure.axes.set_ylabel(ylabel)
        self.figure.axes.set_xlabel(xlabel)
        self.figure.axes.set_title(filetext1)
        # print("filenames",filenames)
        # print("len(filenames)",len(filenames))
        if (len(filenames) == 1):
            if (self.data.filelist[filename].paras["双曲线拟合"] == []):
                self.imagen1Name=filenames[0]+"文件原始数据图(无拟合数据)"
            else:
                self.imagen1Name = filenames[0] + "文件前截" + str(
                    self.data.filelist[filenames[0]].paras["双曲线拟合"][num].cutstartnum1) + "后截" + str(
                    self.data.filelist[filenames[0]].paras["双曲线拟合"][num].cutendnum1) + "双曲线拟合图"
        else:
            self.imagen1Name = filetext1

        self.figure2.axes.legend()
        self.figure2.axes.grid()
        self.figure2.axes.set_ylabel(ylabel)
        self.figure2.axes.set_xlabel(xlabel)
        self.figure2.axes.set_title(filetext2)

        # self.figure5.axes.set_title(filetext2)
        if (len(filenames) == 1):
            if (self.data.filelist[filename].paras["指数拟合"] == []):
                self.imagen2Name=filenames[0]+"文件原始数据图(无拟合数据)"
            else:
                self.imagen2Name = filenames[0] + "文件前截" + str(
                    self.data.filelist[filenames[0]].paras["指数拟合"][num].cutstartnum1) + "后截" + str(
                    self.data.filelist[filenames[0]].paras["指数拟合"][num].cutendnum1) + "指数拟合图"
        else:
            self.imagen2Name = filetext2


        self.figure6.axes.legend()
        self.figure6.axes.grid()
        self.figure6.axes.set_ylabel(ylabel)
        self.figure6.axes.set_xlabel(xlabel)
        self.figure6.axes.set_title(filetext6)

        # self.figure5.axes.set_title(filetext2)
        if (len(filenames) == 1):
            if (self.data.filelist[filename].paras["双曲线积分拟合"] == []):
                self.imagen6Name=filenames[0]+"文件原始数据图(无拟合数据)"
            else:
                self.imagen6Name = filenames[0] + "文件前截" + str(
                    self.data.filelist[filenames[0]].paras["双曲线积分拟合"][num].cutstartnum1) + "后截" + str(
                    self.data.filelist[filenames[0]].paras["双曲线积分拟合"][num].cutendnum1) + "双曲线积分拟合图"
        else:
            self.imagen6Name = filetext6



        self.figure7.axes.legend()
        self.figure7.axes.grid()
        self.figure7.axes.set_ylabel(ylabel)
        self.figure7.axes.set_xlabel(xlabel)
        self.figure7.axes.set_title(filetext7)

        # self.figure5.axes.set_title(filetext2)
        if (len(filenames) == 1):
            if (self.data.filelist[filename].paras["指数积分拟合"] == []):
                self.imagen7Name=filenames[0]+"文件原始数据图(无拟合数据)"
            else:
                self.imagen7Name = filenames[0] + "文件前截" + str(
                    self.data.filelist[filenames[0]].paras["指数积分拟合"][num].cutstartnum1) + "后截" + str(
                    self.data.filelist[filenames[0]].paras["指数积分拟合"][num].cutendnum1) + "指数积分拟合图"
        else:
            self.imagen7Name = filetext7

        self.figure5.axes.legend()
        self.figure5.axes.grid()
        self.figure5.axes.set_ylabel(ylabel)
        self.figure5.axes.set_xlabel(xlabel)
        self.figure5.axes.set_title(filetext3)

        if (len(filenames) == 1):
            if ((self.data.filelist[filename].paras["指数拟合"] == []) and (
                    self.data.filelist[filename].paras["双曲线拟合"] == [])):
                self.imagen5Name=filenames[0]+"文件原始数据图(无拟合数据)"
            elif(self.data.filelist[filename].paras["指数拟合"] == []):
                self.imagen5Name=self.imagen1Name
            elif(self.data.filelist[filename].paras["双曲线拟合"] == []):
                self.imagen5Name=self.imagen2Name
            else:
                self.imagen5Name = filenames[0] + "文件前截" + str(
                    self.data.filelist[filenames[0]].paras["双曲线拟合"][num].cutstartnum1) + "后截" + str(
                    self.data.filelist[filenames[0]].paras["双曲线拟合"][num].cutendnum1) + "双曲线拟合与前截" + str(
                    self.data.filelist[filenames[0]].paras["指数拟合"][num].cutstartnum1) + "后截" + str(
                    self.data.filelist[filenames[0]].paras["指数拟合"][num].cutendnum1) + "双曲线拟合对比图"
        else:
            self.imagen5Name = filetext3

    # 拟合上下限
    def b11lowchange(self, text):
        self.b1low[0] = text
        self.data.b1low[0] = text


    def b11topchange(self, text):
        self.b1top[0] = text
        self.data.b1top[0] = text


    def b12lowchange(self, text):
        self.b1low[1] = text
        self.data.b1low[1] = text


    def b12topchange(self, text):
        self.b1top[1] = text
        self.data.b1top[1] = text


    def b13lowchange(self, text):
        self.b1low[2] = text
        self.data.b1low[2] = text


    def b13topchange(self, text):
        self.b1top[2] = text
        self.data.b1top[2] = text


    def b14lowchange(self, text):
        self.b1low[3] = text
        self.data.b1low[3] = text


    def b14topchange(self, text):
        self.b1top[3] = text
        self.data.b1top[3] = text


    def b21lowchange(self, text):
        self.b2low[0] = text
        self.data.b2low[0] = text


    def b21topchange(self, text):
        self.b2top[0] = text
        self.data.b2top[0] = text


    def b22lowchange(self, text):
        self.b2low[1] = text
        self.data.b2low[1] = text


    def b22topchange(self, text):
        self.b2top[1] = text
        self.data.b2top[1] = text


    def b23lowchange(self, text):
        self.b2low[2] = text
        self.data.b2low[2] = text


    def b23topchange(self, text):
        self.b2top[2] = text
        self.data.b2top[2] = text

    def Table2verticalScrollbarvaluechanged(self,index):
        self.data.Table2verticalScrollindex=index

    # def updatepath(self,path):
    #     print("path0")
    #     self.inLineEdit.blockSignals(True)
    #     self.inLineEdit.setText(path)
    #     self.inLineEdit.blockSignals(False)
    #     print("path1")
    #     self.inpath = path
    #     self.outpath = self.inpath + "/预处理后的数据"
    #     print("path1")
    #     self.outLineEdit.blockSignals(True)
    #     self.outLineEdit.setText(self.outpath)
    #     self.outLineEdit.blockSignals(False)
    #     print("地址")

    def updatestatusbar(self,text):
        # print("提示数据")
        self.statusBar().showMessage(text)
        # print("提示更新end")
    def updatepro(self,num):
        # print("更新进度条")
        self.progressBar.setValue(num)
        # print("更新进度条end")
    def updateData(self,data):
        # print( "updateData in ")
        # print(self.data)
        # print(data)
        self.data=data
        # if isdone==True:
        # self.data=data
        # print("数据更新")
        self.Table1.clear()
        self.Table2.clear()

        self.Table3.clear()
        self.Table4.clear()
        self.Table5.clear()
        self.Table8.clear()
        self.Table9.clear()
        i = 0
        self.Table2.setRowCount(len(self.data.filelist))
        # self.Table2.setColumnCount(self.data.maxCol+4)
        self.Table2.setColumnCount(5)
        self.Table6.setRowCount(len(self.data.filelist))
        # self.Table2.setColumnCount(self.data.maxCol+4)
        self.Table6.setColumnCount(15)
        t2 = ["文件名", "ACQ_Time", "(原始)Max", "(原始)Min", "数据量"]
        # for z in range(self.data.maxCol):
        # t2.append(str(z))

        self.Table2.setHorizontalHeaderLabels(t2)
        self.Table6.setHorizontalHeaderLabels(
            ["文件名", "Project", "Name", "part", "Operator", "Desc", "Excited_Peroid(ms)", "Excited_Time(ms)",
             "Acq_Delay_Time(us)", "Gate_Time(ms)", "Count_Num_per_gate", "Repeat_Times", "Acq_Gate_Times",
             "Interval_per_Gate(us)", "Channel_Number"])
        # print(self.data.maxCol)
        for key in self.data.filelist:
            # print("迭代",i)
            # print(self.data.filelist[key].Cut_Data1)
            self.Table2.setItem(i, 0, QTableWidgetItem(key))
            self.Table2.setItem(i, 1,
                                QTableWidgetItem(self.data.filelist[key].ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
            self.Table2.setItem(i, 2, QTableWidgetItem(str(self.data.filelist[key].Max)))
            self.Table2.setItem(i, 3, QTableWidgetItem(str(self.data.filelist[key].Min)))
            self.Table2.setItem(i, 4, QTableWidgetItem(str(len(self.data.filelist[key].Pro_Data1))))

            self.Table6.setItem(i, 0, QTableWidgetItem(key))
            self.Table6.setItem(i, 1, QTableWidgetItem(str(self.data.filelist[key].Project)))
            self.Table6.setItem(i, 2, QTableWidgetItem(str(self.data.filelist[key].Name)))
            self.Table6.setItem(i, 3, QTableWidgetItem(str(self.data.filelist[key].part)))
            self.Table6.setItem(i, 4, QTableWidgetItem(str(self.data.filelist[key].Operator)))
            self.Table6.setItem(i, 5, QTableWidgetItem(str(self.data.filelist[key].Desc)))
            self.Table6.setItem(i, 6, QTableWidgetItem(str(self.data.filelist[key].Excited_Peroid)))
            self.Table6.setItem(i, 7, QTableWidgetItem(str(self.data.filelist[key].Excited_Time)))
            self.Table6.setItem(i, 8, QTableWidgetItem(str(self.data.filelist[key].Acq_Delay_Time)))
            self.Table6.setItem(i, 9, QTableWidgetItem(str(self.data.filelist[key].Gate_Time)))
            self.Table6.setItem(i, 10, QTableWidgetItem(str(self.data.filelist[key].Count_Num_per_gate)))
            self.Table6.setItem(i, 11, QTableWidgetItem(str(self.data.filelist[key].Repeat_Times)))
            self.Table6.setItem(i, 12, QTableWidgetItem(str(self.data.filelist[key].Acq_Gate_Times)))
            self.Table6.setItem(i, 13, QTableWidgetItem(str(self.data.filelist[key].Interval_per_Gate)))
            self.Table6.setItem(i, 14, QTableWidgetItem(str(self.data.filelist[key].Channel_Number)))
            i += 1

    def updatefitdata(self):
        # self.data=data
        print("updatefitdata")
        self.Table2.clear()
        self.Table2.setRowCount(len(self.data.filelist))
        # self.Table2.setColumnCount(4+14)
        i = 0
        # title2=["文件名","ACQ_Time","(双曲线)I_0", "(双曲线)τ", "(双曲线)Γ", "(双曲线)D","(指数)I_0", "(指数)τ", "(指数)D","(双曲线积分)I_0", "(双曲线积分)τ", "(双曲线积分)Γ", "(双曲线)D","(指数积分)I_0", "(指数积分)τ", "(指数)D"]
        title2 = ["文件名", "ACQ_Time", "Max(原始)", "数据量", "双曲Max","双曲拟合权重", "双曲前截", "双曲后截", "(双曲)R_square", "(双曲)I_0", "(双曲)τ",
                  "(双曲)Γ", "(双曲)D", "(双曲)τ/Γ", "指数Max", "指数拟合权重","指数前截", "指数后截", "(指数)R_square", "(指数)I_0", "(指数)τ", "(指数)D",
                  "双曲积分Max","双曲积分拟合权重", "双曲积分前截", "双曲积分后截", "(双曲积分)R_square", "(双曲积分)I_0", "(双曲积分)τ",
                  "(双曲积分)Γ", "(双曲积分)D", "(双曲积分)τ/Γ", "指数积分Max", "指数积分拟合权重","指数积分前截", "指数积分后截", "(指数积分)R_square", "(指数积分)I_0", "(指数积分)τ", "(指数积分)D"]
        self.Table2.setColumnCount(len(title2))
        self.Table2.setHorizontalHeaderLabels(title2)

        for key, value in self.data.filelist.items():
            row = []
            if (value.paras["双曲线拟合"] != []):
                row.append(value.paras["双曲线拟合"][-1].Max)

                if value.paras["双曲线拟合"][-1].fitweightindex == 1:
                    row.append(str("1/y"))
                elif value.paras["双曲线拟合"][-1].fitweightindex == 2:
                    row.append(str("子矩阵方差"))
                else:
                    row.append(str("1"))
                row.append(value.paras["双曲线拟合"][-1].cutstartnumspot1)
                row.append(value.paras["双曲线拟合"][-1].cutendnumspot1)
                row.append(value.paras["双曲线拟合"][-1].R2[0])
                for t in range(4):
                    row.append(str(round(value.paras["双曲线拟合"][-1].para[t],3))+"±"+str(round(abs(value.paras["双曲线拟合"][-1].para_error[t]),5)))
                row.append(value.paras["双曲线拟合"][-1].para[1] / value.paras["双曲线拟合"][-1].para[2])
            else:
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")

            if (value.paras["指数拟合"] != []):
                row.append(value.paras["指数拟合"][-1].Max)
                if value.paras["指数拟合"][-1].fitweightindex == 1:
                    row.append(str("1/y"))
                elif value.paras["指数拟合"][-1].fitweightindex == 2:
                    row.append(str("子矩阵方差"))
                else:
                    row.append(str("1"))
                row.append(value.paras["指数拟合"][-1].cutstartnumspot1)
                row.append(value.paras["指数拟合"][-1].cutendnumspot1)
                row.append(value.paras["指数拟合"][-1].R2[0])
                for t in range(3):
                    row.append(str(round(value.paras["指数拟合"][-1].para[t],3))+"±"+str(round(abs(value.paras["指数拟合"][-1].para_error[t]),5)))
            else:
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")

            if (value.paras["双曲线积分拟合"] != []):
                row.append(value.paras["双曲线积分拟合"][-1].Max)

                if value.paras["双曲线积分拟合"][-1].fitweightindex == 1:
                    row.append(str("1/y"))
                elif value.paras["双曲线积分拟合"][-1].fitweightindex == 2:
                    row.append(str("子矩阵方差"))
                else:
                    row.append(str("1"))
                row.append(value.paras["双曲线积分拟合"][-1].cutstartnumspot1)
                row.append(value.paras["双曲线积分拟合"][-1].cutendnumspot1)
                row.append(value.paras["双曲线积分拟合"][-1].R2[0])
                for t in range(4):
                    row.append(str(round(value.paras["双曲线积分拟合"][-1].para[t], 3)) + "±" + str(
                        round(abs(value.paras["双曲线积分拟合"][-1].para_error[t]), 5)))
                row.append(value.paras["双曲线积分拟合"][-1].para[1] / value.paras["双曲线积分拟合"][-1].para[2])
            else:
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")

            if (value.paras["指数积分拟合"] != []):
                row.append(value.paras["指数积分拟合"][-1].Max)
                if value.paras["指数积分拟合"][-1].fitweightindex == 1:
                    row.append(str("1/y"))
                elif value.paras["指数积分拟合"][-1].fitweightindex == 2:
                    row.append(str("子矩阵方差"))
                else:
                    row.append(str("1"))
                row.append(value.paras["指数积分拟合"][-1].cutstartnumspot1)
                row.append(value.paras["指数积分拟合"][-1].cutendnumspot1)
                row.append(value.paras["指数积分拟合"][-1].R2[0])
                for t in range(3):
                    row.append(str(round(value.paras["指数积分拟合"][-1].para[t], 3)) + "±" + str(
                        round(abs(value.paras["指数积分拟合"][-1].para_error[t]), 5)))
            else:
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")


            self.Table2.setItem(i, 0, QTableWidgetItem(key))
            self.Table2.setItem(i, 1, QTableWidgetItem(value.ACQ_Time.strftime('%Y-%m-%d  %H:%M:%S.%f')))
            self.Table2.setItem(i, 2, QTableWidgetItem(str(value.Max)))
            self.Table2.setItem(i, 3, QTableWidgetItem(str(len(value.Pro_Data1))))
            j = 4
            for para in row:
                if not isinstance(para, str):
                # if (para != "" and):
                    self.Table2.setItem(i, j, QTableWidgetItem(str(round(para, 4))))
                else:
                    self.Table2.setItem(i, j, QTableWidgetItem(para))
                    # self.Table2.setItem(i, j, QTableWidgetItem(str(para)))
                j += 1
            for k in range(4, 9):
                self.Table2.item(i, k).setBackground(QBrush(QColor(255, 193, 193)))
                # self.Table2.item(i+7, k).setBackground(QBrush(QColor(240, 125, 125)))
            for k in range(9, 14):
                self.Table2.item(i, k).setBackground(QBrush(QColor(205, 155, 155)))
                # self.Table2.item(i+7, k).setBackground(QBrush(QColor(240, 125, 125)))
            for k in range(14, 19):
                self.Table2.item(i, k).setBackground(QBrush(QColor(154, 255, 154)))
            for k in range(19, 22):
                self.Table2.item(i, k).setBackground(QBrush(QColor(124, 205, 124)))

            #积分拟合数据
            for k in range(22, 27):
                self.Table2.item(i, k).setBackground(QBrush(QColor(255, 193, 193)))
                # self.Table2.item(i+7, k).setBackground(QBrush(QColor(240, 125, 125)))
            for k in range(27, 32):
                self.Table2.item(i, k).setBackground(QBrush(QColor(205, 155, 155)))
                # self.Table2.item(i+7, k).setBackground(QBrush(QColor(240, 125, 125)))
            for k in range(32, 37):
                self.Table2.item(i, k).setBackground(QBrush(QColor(154, 255, 154)))
            for k in range(37, 40):
                self.Table2.item(i, k).setBackground(QBrush(QColor(124, 205, 124)))
            i += 1

        # 若不是批量拟合，只改变一行数据
        if (self.fitComboBox.currentText() != "批量拟合"):
            index = self.fitComboBox.currentText().find("]")
            # self.plotdata(self.fitComboBox.currentText()[(index + 1):])
        self.Table4.clear()
        self.Table5.clear()
        self.Table8.clear()
        self.Table9.clear()
        self.Table4.setColumnCount(0)
        self.Table5.setColumnCount(0)
        self.Table8.setColumnCount(0)
        self.Table9.setColumnCount(0)
        self.Table4.setRowCount(0)
        self.Table5.setRowCount(0)
        self.Table8.setRowCount(0)
        self.Table9.setRowCount(0)
        if self.data.Table2selectrow!=-1:
            self.Table2.scrollToItem(self.Table2.item(self.data.Table2verticalScrollindex, 0), QAbstractItemView.PositionAtTop)
            self.Table2.verticalHeader().setCurrentIndex(self.Table2.model().index(self.data.Table2selectrow,0))
            print("temp",self.data.Table2selectrow)
            # self.Table2VerticalHeaderClick(self.data.Table2selectrow)



    def updatareadhistory(self,data:datastruct):
        self.data=data
        self.fitComboBox.clear()
        self.fitComboBox.addItems(["批量拟合"])
        # self.inpath=
        self.outpath = self.data.outpath
        self.inLineEdit.blockSignals(True)
        self.inLineEdit.setText(self.data.inpath)
        self.inLineEdit.blockSignals(False)
        self.outLineEdit.blockSignals(True)
        self.outLineEdit.setText(self.data.outpath)
        self.outLineEdit.blockSignals(False)
        self.imagen1Name = self.data.imagen1Name
        self.imagen2Name = self.data.imagen2Name
        self.imagen6Name = self.data.imagen6Name
        self.imagen7Name = self.data.imagen7Name
        # print(self.data.cb1setChecked)
        # print(self.data.cb2setChecked)
        self.cb1.setChecked(bool(self.data.cb1setChecked))
        self.cb2.setChecked(bool(self.data.cb2setChecked))
        # self.figure.fig.canvas.draw_idle()
        # self.figure.axes.clear()
        # self.figure2.fig.canvas.draw_idle()
        # self.figure2.axes.clear()
        # self.figure3.fig.canvas.draw_idle()
        # self.figure3.axes.clear()
        # self.figure4.fig.canvas.draw_idle()
        # self.figure4.axes.clear()
        # self.figure5.fig.canvas.draw_idle()
        # self.figure5.axes.clear()
        # print(type(self.figure2.fig))
        # self.figure.fig.canvas.flush_events()
        # self.figure.fig.clf()
        # self.figure2.fig.clf()
        # self.figure3.fig.clf()
        # self.figure4.fig.clf()
        # self.figure5.clf()

        # self.figure.fig=self.data.currentimage1
        # self.figure2.fig=self.data.currentimage2
        # self.figure3.fig =self.data.currentimage3
        # self.figure4.fig =self.data.currentimage4
        # print(type(self.figure2.fig))
        # self.figure5.fig =self.data.currentimage5
        # self.figure.fig.canvas.flush_events()
        # self.figure2.fig.canvas.flush_events()
        # self.figure3.fig.canvas.flush_events()
        # self.figure4.fig.canvas.flush_events()
        # self.data.figure5.fig.canvas.flush_events()
        self.Table2V = self.data.Table2V
        self.Table2H = self.data.Table2H
        self.showcutComboBox.setCurrentIndex(self.data.showcut)
        self.featurexComboBox.setCurrentIndex(self.data.featurex)
        self.fitweightComboBox.setCurrentIndex(self.data.fitweightindex)
        # self.showcut = self.data.showcut
        # self.featurex = self.data.featurex

        self.b11ComboBoxlow.setCurrentText(self.data.b1low[0])
        self.b12ComboBoxlow.setCurrentText(self.data.b1low[1])
        self.b13ComboBoxlow.setCurrentText(self.data.b1low[2])
        self.b14ComboBoxlow.setCurrentText(self.data.b1low[3])
        self.b11ComboBoxtop.setCurrentText(self.data.b1top[0])
        self.b12ComboBoxtop.setCurrentText(self.data.b1top[1])
        self.b13ComboBoxtop.setCurrentText(self.data.b1top[2])
        self.b14ComboBoxtop.setCurrentText(self.data.b1top[3])

        self.b21ComboBoxlow.setCurrentText(self.data.b2low[0])
        self.b22ComboBoxlow.setCurrentText(self.data.b2low[1])
        self.b23ComboBoxlow.setCurrentText(self.data.b2low[2])
        self.b21ComboBoxtop.setCurrentText(self.data.b2top[0])
        self.b22ComboBoxtop.setCurrentText(self.data.b2top[1])
        self.b23ComboBoxtop.setCurrentText(self.data.b2top[2])
        if (self.data.fitComboBoxtext != "批量拟合"):
            self.fitComboBox.clear()
            self.fitComboBox.addItems(["批量拟合", self.data.fitComboBoxtext])
            self.fitComboBox.setCurrentIndex(1)
        self.cutComboBoxstart.setCurrentText(self.data.cutComboBoxstarttext)
        self.cutComboBoxend.setCurrentText(self.data.cutComboBoxendtext)

        # self.b1low = self.data.b1low
        # self.b1top = self.data.b1top
        # self.b2low = self.data.b2low
        # self.b2top = self.data.b2top
        i = 0
        self.Table6.setRowCount(len(self.data.filelist))
        self.Table6.setColumnCount(15)
        self.Table6.setHorizontalHeaderLabels(
            ["文件名", "Project", "Name", "part", "Operator", "Desc", "Excited_Peroid(ms)", "Excited_Time(ms)",
             "Acq_Delay_Time(us)", "Gate_Time(ms)", "Count_Num_per_gate", "Repeat_Times", "Acq_Gate_Times",
             "Interval_per_Gate(us)", "Channel_Number"])
        for key in self.data.filelist:
            self.Table6.setItem(i, 0, QTableWidgetItem(key))
            self.Table6.setItem(i, 1, QTableWidgetItem(str(self.data.filelist[key].Project)))
            self.Table6.setItem(i, 2, QTableWidgetItem(str(self.data.filelist[key].Name)))
            self.Table6.setItem(i, 3, QTableWidgetItem(str(self.data.filelist[key].part)))
            self.Table6.setItem(i, 4, QTableWidgetItem(str(self.data.filelist[key].Operator)))
            self.Table6.setItem(i, 5, QTableWidgetItem(str(self.data.filelist[key].Desc)))
            self.Table6.setItem(i, 6, QTableWidgetItem(str(self.data.filelist[key].Excited_Peroid)))
            self.Table6.setItem(i, 7, QTableWidgetItem(str(self.data.filelist[key].Excited_Time)))
            self.Table6.setItem(i, 8, QTableWidgetItem(str(self.data.filelist[key].Acq_Delay_Time)))
            self.Table6.setItem(i, 9, QTableWidgetItem(str(self.data.filelist[key].Gate_Time)))
            self.Table6.setItem(i, 10, QTableWidgetItem(str(self.data.filelist[key].Count_Num_per_gate)))
            self.Table6.setItem(i, 11, QTableWidgetItem(str(self.data.filelist[key].Repeat_Times)))
            self.Table6.setItem(i, 12, QTableWidgetItem(str(self.data.filelist[key].Acq_Gate_Times)))
            self.Table6.setItem(i, 13, QTableWidgetItem(str(self.data.filelist[key].Interval_per_Gate)))
            self.Table6.setItem(i, 14, QTableWidgetItem(str(self.data.filelist[key].Channel_Number)))
            i += 1
        self.updatefitdata()
        self.statusBar().showMessage("已加载"+str(len(self.data.filelist))+"条历史数据！")


    def addhistorydata(self,data):
        # 更新historydata
        if data in self.historydata:
            self.historydata.remove(data)
        self.historydata.insert(0,data)

        # 保存历史添加
        filepath = os.getcwd() + "/cache/"
        if (not os.path.exists(filepath)):
            os.makedirs(filepath)

        filename = os.getcwd() + "/cache/historydata.ache"

        with open(filename, "wb") as file:
            pickle.dump(self.historydata, file, True)
            print("历史添加保存成功！")

        # 更新table7
        self.Table7.clear()
        self.Table7.addItems(self.historydata)

    def provisible(self,isvisible):
        # print("更新进度条可见")
        self.progressBar.setVisible(isvisible)
        # print("更新进度条可见end")



class dragLineEdit(QLineEdit):
    def __init__(self, statusBar):
        super(dragLineEdit, self).__init__()
        self.statusBar = statusBar

    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        filename = evn.mimeData().text().split("///")[1]
        # print(filename)
        if (os.path.isdir(filename)):
            self.setText(filename)
        else:
            self.statusBar().showMessage("文件无效，请选择文件目录！")

    def dragMoveEvent(self, evn):
        self.statusBar().showMessage("正在进行拖入操作...")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ui = main()
    ui.show()
    sys.exit(app.exec_())


