import numpy as np
import matplotlib.pyplot as plt
import matplotlib; matplotlib.use('TkAgg')
plt.rc('font',family='Times New Roman')
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

    data41=[]
    data42=[]
    data43=[]
    data44=[]
    x41=[]
    x42=[]
    x43=[]
    x44=[]
    x=[i*0.1 for i in range(200)]

    for i in range(50):
        data41.append(data4[i*4])
        data42.append(data4[i*4+1])
        data43.append(data4[i*4+2])
        data44.append(data4[i*4+3])
        x41.append(x[i*4])
        x42.append(x[i*4+1])
        x43.append(x[i*4+2])
        x44.append(x[i*4+3])
    plt.figure(figsize=(20, 7))
    matplotlib.rcParams.update({'font.size': 20})

    plt.bar(x=x41,  # 柱体在 x 轴上的坐标位置
           height=data41,  # 柱体的高度
           align='edge',  # x 轴上的坐标与柱体对其的位置
           color='aqua',  # 柱体的填充颜色
           edgecolor="red",
           linewidth=1,
           fill=False,
           # tick_label=labels,  # 每个柱体的标签名称
           alpha=1,  # 柱体填充颜色的透明度
           width=0.4,  # 柱体的宽度
           bottom=0.2,  # 柱体基线的 y 轴坐标
           )

    plt.bar(x=x42,  # 柱体在 x 轴上的坐标位置
           height=data42,  # 柱体的高度
           align='edge',  # x 轴上的坐标与柱体对其的位置
           color='aqua',  # 柱体的填充颜色
           edgecolor="black",
           linewidth=1,
            fill=False,
           # tick_label=labels,  # 每个柱体的标签名称
           alpha=1,  # 柱体填充颜色的透明度
           width=0.4,  # 柱体的宽度
           bottom=0.2,  # 柱体基线的 y 轴坐标
           )

    plt.bar(x=x43,  # 柱体在 x 轴上的坐标位置
           height=data43,  # 柱体的高度
           align='edge',  # x 轴上的坐标与柱体对其的位置
           color='aqua',  # 柱体的填充颜色
           edgecolor="green",
           linewidth=1,
            fill=False,
           # tick_label=labels,  # 每个柱体的标签名称
           alpha=1,  # 柱体填充颜色的透明度
           width=0.4,  # 柱体的宽度
           bottom=0.2,  # 柱体基线的 y 轴坐标
           )

    plt.bar(x=x44,  # 柱体在 x 轴上的坐标位置
           height=data44,  # 柱体的高度
           align='edge',  # x 轴上的坐标与柱体对其的位置
           color='aqua',  # 柱体的填充颜色
           edgecolor="blue",
           linewidth=1,
        fill=False,
           # tick_label=labels,  # 每个柱体的标签名称
           alpha=1,  # 柱体填充颜色的透明度
           width=0.4,  # 柱体的宽度
           bottom=0.2,  # 柱体基线的 y 轴坐标
           )

    # plt.title("(b)", fontsize=24,loc="right")  # 设置标题
    plt.xlabel("Delay time(ms)", fontsize=23)  # 设置x坐标标注，字体为18号
    plt.ylabel("Photon intensity(CPS)", fontsize=23)  # 设置y坐标标注
    plt.ticklabel_format(style='sci', axis='y', scilimits=(-4,4))
    plt.gca().ticklabel_format(useMathText=True)
    # plt.ticklabel_format(style='plain', axis='y')
    # plt.legend()
    plt.savefig('image1.png', dpi =600, bbox_inches = 'tight')
    # plt.axis('off')
    # plt.gcf().set_size_inches(512 / 100, 512 / 100)
    # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())
    # plt.subplots_adjust(top=1, bottom=0, right=0.93, left=0, hspace=0, wspace=0)
    # plt.margins(0, 0)
    # plt.savefig('image.png')

    plt.show()


main()