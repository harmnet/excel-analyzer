import os
import glob
from pptx import Presentation

# 文件路径配置
ppt_folder = "/Users/harmnet/Desktop/02 PPT课件"  # PPT文件夹路径

# 获取所有PPT文件（包括子文件夹）
ppt_files = []
for root, dirs, files in os.walk(ppt_folder):
    for file in files:
        if file.endswith(".pptx"):
            ppt_files.append(os.path.join(root, file))

if not ppt_files:
    print(f"在 {ppt_folder} 及其子文件夹中未找到任何.pptx文件")
    exit(1)

print(f"找到 {len(ppt_files)} 个PPT文件，开始统计页数...")

# 初始化总页数计数器
total_pages = 0

# 统计每个PPT的页数
for ppt_file in ppt_files:
    try:
        prs = Presentation(ppt_file)
        slide_count = len(prs.slides)
        total_pages += slide_count
        # 显示相对路径，方便定位文件
        rel_path = os.path.relpath(ppt_file, ppt_folder)
        print(f"{rel_path}: {slide_count} 页")
    except Exception as e:
        rel_path = os.path.relpath(ppt_file, ppt_folder)
        print(f"{rel_path}: 无法读取 ({str(e)})")

print(f"\n统计完成！总页码数: {total_pages} 页")
