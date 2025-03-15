import os
import pandas as pd
import re

# 文件路径配置
desktop_path = "/Users/harmnet/Desktop"
excel_file = os.path.join(desktop_path, "副本正式题目3-更改后.xlsx")

# 检查文件是否存在
if not os.path.exists(excel_file):
    print(f"文件 {excel_file} 不存在！")
    exit(1)

# 读取Excel文件
try:
    df = pd.read_excel(excel_file)
    print(f"成功读取文件，共有 {len(df)} 行数据")
except Exception as e:
    print(f"读取文件时出错: {str(e)}")
    exit(1)

# 获取G列的列名
answer_column = df.columns[6]  # G列对应索引6
print(f"使用{answer_column}列(G列)作为答案列")

# 处理答案格式
def format_answer(answer):
    if not isinstance(answer, str):
        return answer
    
    # 如果答案中已经包含"/"，则不处理
    if "/" in answer:
        return answer
    
    # 检查是否是类似"ABCD"格式的多选题答案
    if re.match(r'^[A-Z]+$', answer):
        # 将"ABCD"转换为"A/B/C/D"
        return "/".join(list(answer))
    
    return answer

# 应用格式化函数到答案列
df[answer_column] = df[answer_column].apply(format_answer)
print("答案格式处理完成")

# 计算每个文件应包含的题目数量
total_questions = len(df)
questions_per_file = 199
num_files = (total_questions + questions_per_file - 1) // questions_per_file  # 向上取整

print(f"总共 {total_questions} 道题目，将拆分为 {num_files} 个文件")

# 拆分并保存文件
for i in range(num_files):
    start_idx = i * questions_per_file
    end_idx = min((i + 1) * questions_per_file, total_questions)
    
    # 提取当前批次的数据
    current_df = df.iloc[start_idx:end_idx].copy()
    
    # 保存为新文件
    output_file = os.path.join(desktop_path, f"试题_{i+1}.xlsx")
    current_df.to_excel(output_file, index=False)
    print(f"已保存文件: {output_file}，包含 {len(current_df)} 道题目")

print("所有文件处理完成！")
