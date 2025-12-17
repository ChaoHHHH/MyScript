"""
Author: Chao
Date: 2025年12月17日21:24:31

PWmat在绘制能带中，最后使用plot_band_structure.x后会生成bandstructure_1 or will also get 2 if spin = 2，总之会有这样的文件，本scrip用来绘制能带图
"""

import matplotlib.pyplot as plt

        #############
        # I N P U T #
        #############
###################################
file = ".//plotband//bandstructure_1.txt"

MIN_ENERGY = -10.0 # eV
MAX_ENERGY = 11.0  # eV

###################################


plt.rcParams['font.sans-serif'] = ['Arial']  # 指定默认字体为Arial
plt.rcParams['axes.unicode_minus'] = False   # 用来正常显示负号
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'bold'  # 设置字体粗细为粗体
plt.rcParams['axes.titleweight'] = 'bold'  # 坐标轴标题粗体
plt.rcParams['axes.labelweight'] = 'bold'  # 坐标轴标签粗体


with open(file) as f:

    lines = f.readlines()

    energys = [[]]
    kpoints = [[]]
    i = 0
    klabels = []

    for line in lines:
        line = line.split()
        if len(line) != 0:
            if len(line) == 2:
                kpoints[i].append(float(line[0]))
                energys[i].append(float(line[1]))
            elif len(line) == 3:
                if i == 0:
                    klabels.append([line[2], float(line[0])]) #label and kpoints eg.  ['M', 0.6029]
                else:
                    kpoints[i].append(float(line[0]))
                    energys[i].append(float(line[1]))
        else:
            energys.append([])
            kpoints.append([])
            i += 1

for i, _ in enumerate(kpoints):
    if len(kpoints[i]) != 0:
        plt.plot(kpoints[i],energys[i],c='k')
    else:
        pass

plt.ylim((MIN_ENERGY,MAX_ENERGY))
plt.xlim((min(kpoints[0]),max(kpoints[0])))

# 提取klabel的位置和标签
k_label_positions = []
k_label_names = []
for label, pos in klabels:
    k_label_positions.append(pos)
    k_label_names.append(label)

# 设置x轴刻度和标签
plt.xticks(k_label_positions, k_label_names)

# 可选：在高对称点处添加垂直线
for pos in k_label_positions:
    plt.axvline(x=pos, color='gray', linestyle='-', linewidth=0.5)

# 可选：设置y=0处的水平线
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)

plt.ylabel('Energy(eV)')

plt.show()