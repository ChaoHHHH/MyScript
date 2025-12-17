import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 数据
defects = ['远悬挂键', '近悬挂键', '远氧空位', '近氧空位']
vbm = [5.8220, 5.8293, 5.8259, 5.8251]  # 价带顶
cbm = [6.5203, 6.5176, 6.5175, 6.5260]  # 导带底
defect_levels = [7.5835, 7.4102, 9.1753, 8.5640]  # 缺陷态能级

# 创建图形
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [2, 1]})

# 第一个子图：详细能级图
x_positions = np.arange(len(defects))
width = 0.25

# 绘制能级条形图
bars1 = ax1.bar(x_positions - width, vbm, width, label='VBM (价带顶)', color='#1f77b4', alpha=0.8)
bars2 = ax1.bar(x_positions, cbm, width, label='CBM (导带底)', color='#ff7f0e', alpha=0.8)
bars3 = ax1.bar(x_positions + width, defect_levels, width, label='缺陷态能级', color='#2ca02c', alpha=0.8)

# 添加数值标签
def add_labels(bars, ax):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.4f}', ha='center', va='bottom', fontsize=9)

add_labels(bars1, ax1)
add_labels(bars2, ax1)
add_labels(bars3, ax1)

# 设置x轴
ax1.set_xlabel('缺陷类型', fontsize=12, fontweight='bold')
ax1.set_ylabel('能量 (eV)', fontsize=12, fontweight='bold')
ax1.set_title('四种点缺陷的能级位置对比', fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x_positions)
ax1.set_xticklabels(defects, fontsize=11)
ax1.set_ylim(5.5, 10)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend(loc='upper left', fontsize=10)

# 第二个子图：能级示意图
ax2.set_title('能级示意图', fontsize=14, fontweight='bold', pad=20)
ax2.set_xlim(0, 1)
ax2.set_ylim(5, 10)
ax2.set_ylabel('能量 (eV)', fontsize=12, fontweight='bold')
ax2.set_xticks([])  # 隐藏x轴

# 绘制导带底和价带顶的参考线
ax2.axhline(y=6.0, xmin=0.1, xmax=0.9, color='#ff7f0e', linewidth=3, alpha=0.7, label='导带底范围')
ax2.axhline(y=5.8, xmin=0.1, xmax=0.9, color='#1f77b4', linewidth=3, alpha=0.7, label='价带顶范围')

# 为每种缺陷绘制能级线
colors = ['#d62728', '#9467bd', '#8c564b', '#e377c2']
y_offset = 0.15

for i, defect in enumerate(defects):
    # 绘制缺陷能级线
    ax2.plot([0.2, 0.8], [defect_levels[i], defect_levels[i]], 
             color=colors[i], linewidth=2.5, alpha=0.8, label=f'{defect}: {defect_levels[i]:.4f} eV')
    
    # 添加缺陷标签
    ax2.text(0.85, defect_levels[i], f'{defect_levels[i]:.4f}', 
             va='center', ha='left', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[i], alpha=0.2))

# 添加带隙区域说明
ax2.fill_between([0.1, 0.9], 5.82, 6.52, alpha=0.1, color='gray', label='带隙区域')
ax2.text(0.5, 6.17, '带隙', ha='center', va='center', fontsize=11, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))

# 设置图例
ax2.legend(loc='upper right', fontsize=9)

# 调整布局
plt.tight_layout()

# 添加总体说明
plt.figtext(0.5, 0.01, 
            '注：VBM为价带顶，CBM为导带底。缺陷态能级位置反映了缺陷在禁带中的位置，\n'
            '远氧空位的缺陷态能级最高(9.1753 eV)，表明其最接近导带；近悬挂键的缺陷态能级最低(7.4102 eV)。',
            ha='center', fontsize=10, style='italic', bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.5))

plt.show()

# 也可以选择绘制更简洁的版本
print("\n正在绘制简洁版能级图...\n")

# 简洁版能级图
fig2, ax3 = plt.subplots(figsize=(12, 8))

# 为每种缺陷创建能级示意图
for i, defect in enumerate(defects):
    # 绘制VBM和CBM的连线（表示带隙）
    ax3.plot([i-0.2, i+0.2], [vbm[i], vbm[i]], 'b-', linewidth=2, alpha=0.7)
    ax3.plot([i-0.2, i+0.2], [cbm[i], cbm[i]], 'r-', linewidth=2, alpha=0.7)
    ax3.plot([i, i], [vbm[i], cbm[i]], 'k--', linewidth=1, alpha=0.5)
    
    # 绘制缺陷能级
    ax3.plot([i-0.3, i+0.3], [defect_levels[i], defect_levels[i]], 
             color=colors[i], linewidth=3, alpha=0.8)
    
    # 添加能级数值
    ax3.text(i, vbm[i]-0.15, f'VBM: {vbm[i]:.4f}', ha='center', va='top', fontsize=9)
    ax3.text(i, cbm[i]+0.15, f'CBM: {cbm[i]:.4f}', ha='center', va='bottom', fontsize=9)
    ax3.text(i, defect_levels[i]+0.15, f'缺陷: {defect_levels[i]:.4f}', 
             ha='center', va='bottom', fontsize=10, fontweight='bold', color=colors[i])
    
    # 添加缺陷类型标签
    ax3.text(i, 4.8, defect, ha='center', va='top', fontsize=11, fontweight='bold')

# 设置图形属性
ax3.set_xlabel('缺陷类型', fontsize=12, fontweight='bold')
ax3.set_ylabel('能量 (eV)', fontsize=12, fontweight='bold')
ax3.set_title('点缺陷能级位置示意图', fontsize=14, fontweight='bold', pad=20)
ax3.set_xlim(-0.5, len(defects)-0.5)
ax3.set_ylim(4.5, 10)
ax3.set_xticks(range(len(defects)))
ax3.set_xticklabels(defects, fontsize=11)
ax3.grid(True, alpha=0.3, linestyle='--')

# 添加图例
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='b', lw=2, label='VBM (价带顶)'),
    Line2D([0], [0], color='r', lw=2, label='CBM (导带底)'),
    Line2D([0], [0], color='k', lw=1, linestyle='--', label='带隙'),
    Line2D([0], [0], color=colors[0], lw=3, label='缺陷态能级'),
]
ax3.legend(handles=legend_elements, loc='upper right', fontsize=10)

plt.tight_layout()
plt.show()