import numpy as np
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('TkAgg')

class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
            self.format = r'$\mathdefault{%s}$' % self.format


class main():

    data1=[]
    for line in open("D:/工作文件2/延迟数据/发光与时辰-B.txt").readlines():
        linenew = line.strip()
        if (linenew != ""):
            data1.append(int(linenew))

    data2=[]
    for line in open("D:/工作文件2/延迟数据/发光与时辰-D.txt").readlines():
        linenew = line.strip()
        if (linenew != ""):
            data2.append(int(linenew))

    data3=[]
    for line in open("D:/工作文件2/延迟数据/背景噪声-D.txt").readlines():
        linenew = line.strip()
        if (linenew != ""):
            data3.append(int(linenew))

    data4=[]
    for line in open("D:/工作文件2/延迟数据/手指发光-D.txt").readlines():
        linenew = line.strip()
        if (linenew != ""):
            data4.append(int(linenew))



    x=[i*0.1 for i in range(200)]
    matplotlib.rcParams.update({'font.size': 13})




    fig=plt.figure(figsize=(20, 7))
    ax1 = fig.add_subplot(1, 2, 1)  ##左右布局
    ax2 = fig.add_subplot(1, 2, 2)
    plt.sca(ax1)
    # plt.plot(x,data1,c="red", marker = '+',label="the DL curve of index finger",markersize=3)
    plt.plot(x,data1,c="red", marker = '+',markersize=5)

    # plt.plot(x,data1,c="red")
    # plt.scatter(x,data1,marker='+',color='none',edgecolors='red',s=10)
    # plt.plot(x,data2,c="blue",marker = 'o',label="the DL curve measured after the finger is removed",markersize=3)
    plt.plot(x,data2,c="blue",marker = 'o',markersize=5)
    # plt.plot(x,data2,c="blue",marker = 'o',markersize=5,markerfacecolor='none')
    # plt.scatter(x,data2,marker='o', color='none', edgecolors='blue', s=10)
    # plt.xlabel("Delay time(ms)", fontproperties=my_font, fontsize=18)  # 设置x坐标标注，字体为18号
    # plt.ylabel("Photon intensity(CPS)", fontproperties=my_font, fontsize=18)  # 设置y坐标标注
    # plt.title("10点到12点每分钟温度变化图", fontproperties=my_font, fontsize=24)  # 设置标题
    plt.title("(a)",fontsize=18)  # 设置标题
    # plt.title("(a)",fontsize=24,loc="right")  # 设置标题
    plt.xlabel("Delay time(ms)", fontsize=18)  # 设置x坐标标注，字体为18号
    plt.ylabel("Photon intensity(CPS)", fontsize=18)  # 设置y坐标标注
    plt.ticklabel_format(style='plain', axis='y')
    # plt.legend()
    # plt.grid(alpha=0.4)  # 添加网格，alpha = 0.4透明度

    plt.sca(ax2)
    # plt.plot(x, data3, c="red", marker='+')
    plt.plot(x, data3, c="red", marker='+', label="the DL curve of index finger", markersize=5)

    # plt.plot(x,data1,c="red")
    # plt.scatter(x,data1,marker='+',color='none',edgecolors='red',s=10)
    # plt.plot(x, data4, c="blue", marker='o')
    plt.plot(x, data4, c="blue", marker='o', label="the DL curve measured after the finger is removed", markersize=5)
    # plt.plot(x, data4, c="blue", marker='o', label="the DL curve measured after the finger is removed", markersize=5,markerfacecolor='none')
    # plt.scatter(x,data2,marker='o', color='none', edgecolors='blue', s=10)
    # plt.xlabel("Delay time(ms)", fontproperties=my_font, fontsize=18)  # 设置x坐标标注，字体为18号
    # plt.ylabel("Photon intensity(CPS)", fontproperties=my_font, fontsize=18)  # 设置y坐标标注
    # plt.title("10点到12点每分钟温度变化图", fontproperties=my_font, fontsize=24)  # 设置标题
    plt.title("(b)", fontsize=18)  # 设置标题
    # plt.title("(b)", fontsize=24,loc="right")  # 设置标题
    plt.xlabel("Delay time(ms)", fontsize=18)  # 设置x坐标标注，字体为18号
    plt.ylabel("Photon intensity(CPS)", fontsize=18)  # 设置y坐标标注
    plt.ticklabel_format(style='plain', axis='y')
    plt.legend()
    # handles, labels = ax2.get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper center')
    # legend=plt.legend(handles=[line1,line2],labels=["the DL curve of index finger","the DL curve measured after the finger is removed"])
    # plt.grid(alpha=0.4)  # 添加网格，alpha = 0.4透明度

    ax1.yaxis.set_major_formatter(OOMFormatter(4, "%1.1f"))
    ax1.ticklabel_format(axis='y', style='sci', scilimits=(-4, -4))
    ax2.yaxis.set_major_formatter(OOMFormatter(4, "%1.1f"))
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(-4, -4))
    plt.savefig('image.png', dpi =600, bbox_inches = 'tight')
    # plt.axis('off')
    # plt.gcf().set_size_inches(512 / 100, 512 / 100)
    # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())
    # plt.subplots_adjust(top=1, bottom=0, right=0.93, left=0, hspace=0, wspace=0)
    # plt.margins(0, 0)
    # plt.savefig('image.png')

    plt.show()


main()