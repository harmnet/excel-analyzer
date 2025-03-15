import deepseek as ds

# 打印模块的所有属性和方法
print("Deepseek 模块内容:")
print("==================")
for item in dir(ds):
    if not item.startswith('_'):  # 不显示内部/私有属性
        print(item)

# 打印版本信息（如果有）
if hasattr(ds, '__version__'):
    print("\nDeepseek 版本:", ds.__version__)

# data = ds.load_data("《商务数据分析基础》数据集-电子商务2025",format = "xlsx")
# clean_data = ds.fill_missing(data, strategy="median")