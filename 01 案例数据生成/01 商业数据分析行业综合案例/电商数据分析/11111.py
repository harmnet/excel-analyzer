import pandas as pd

# 生成身份证号数据
start_id = 500235199510204666
id_list = [str(start_id + i) for i in range(4695)]

# 创建DataFrame
df = pd.DataFrame(id_list, columns=['身份证号'])

# 导出到excel文件
file_path = '/Users/harmnet/Desktop/身份证号.xlsx'
df.to_excel(file_path, index=False)

print(f"数据已成功导出到 {file_path}")
