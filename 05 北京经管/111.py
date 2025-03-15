import matplotlib.pyplot as plt

# 示例数据
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

# 创建折线图
plt.plot(x, y)

# 添加标题和轴标签
plt.title('简单折线图示例')
plt.xlabel('x轴')
plt.ylabel('y轴')

# 显示图形
plt.show()