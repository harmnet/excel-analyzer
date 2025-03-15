import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd
import numpy as np

# 设置中文字体
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'  # 请根据你的系统调整字体路径
font_prop = font_manager.FontProperties(fname=font_path)

# 销售驱动因素数据
factors = {
    '驱动因素': ['促销活动', '渠道选择', '市场趋势'],
    '影响程度': [8, 20, 0.5]
}

# 创建DataFrame
df_factors = pd.DataFrame(factors)

# 画雷达图
categories = df_factors['驱动因素']
values = df_factors['影响程度']

# 计算角度
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # 闭合雷达图

# 标准化数据以适应雷达图
values_normalized = values / np.max(values) * 100
values_normalized = np.append(values_normalized, values_normalized[0])

# 创建图形
plt.figure(figsize=(10, 6))
ax = plt.subplot(111, polar=True)

# 绘制雷达图
ax.plot(angles, values_normalized, 'o-', linewidth=2, color='lightcoral')
ax.fill(angles, values_normalized, alpha=0.25, color='lightcoral')

# 设置刻度标签
ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontproperties=font_prop)

# 设置y轴标签
ax.set_rlabel_position(0)
plt.yticks([20, 40, 60, 80, 100], ["20%", "40%", "60%", "80%", "100%"], 
           color="grey", size=8)
plt.ylim(0, 100)

# 添加标题
plt.title('销售驱动因素分析', fontproperties=font_prop, y=1.1)

plt.tight_layout()

# 显示图表
plt.show()
