#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Excel数据集异常值分析工具打包脚本
用于将Python脚本打包成Windows可执行文件(.exe)

使用方法:
1. 安装必要的依赖: pip install pyinstaller
2. 运行此脚本: python build_windows_exe.py
3. 在dist目录中找到生成的.exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("开始打包Excel数据集异常值分析工具...")
    
    # 确保PyInstaller已安装
    try:
        import PyInstaller
        print("检测到PyInstaller已安装")
    except ImportError:
        print("未检测到PyInstaller，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller安装完成")
    
    # 确保其他依赖已安装
    dependencies = [
        "pandas", "openpyxl", "openai", "python-docx", "PyQt5"
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"检测到{dep}已安装")
        except ImportError:
            print(f"未检测到{dep}，正在安装...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"{dep}安装完成")
    
    # 创建临时目录用于存放图标和其他资源
    temp_dir = Path("temp_build")
    if not temp_dir.exists():
        temp_dir.mkdir()
    
    # 创建图标文件
    icon_path = temp_dir / "app_icon.ico"
    if not icon_path.exists():
        try:
            # 尝试使用PIL创建一个简单的图标
            from PIL import Image, ImageDraw
            
            # 创建一个128x128的图像
            img = Image.new('RGBA', (128, 128), color=(255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # 绘制一个简单的图标 - 紫荆红色的圆形
            draw.ellipse((10, 10, 118, 118), fill=(158, 33, 65, 255))
            
            # 保存为ICO文件
            img.save(str(icon_path), format='ICO')
            print(f"创建图标文件: {icon_path}")
        except Exception as e:
            print(f"创建图标失败: {e}")
            print("将使用默认图标")
            icon_path = None
    
    # 构建PyInstaller命令
    pyinstaller_cmd = [
        "pyinstaller",
        "--name=Excel数据集异常值分析工具",
        "--onefile",
        "--windowed",
        "--clean",
    ]
    
    # 添加图标
    if icon_path and icon_path.exists():
        pyinstaller_cmd.append(f"--icon={icon_path}")
    
    # 添加主脚本
    pyinstaller_cmd.append("excel_analyzer_gui.py")
    
    # 执行PyInstaller命令
    print("正在执行PyInstaller打包命令...")
    print(" ".join(pyinstaller_cmd))
    subprocess.check_call(pyinstaller_cmd)
    
    # 清理临时文件
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    
    # 检查打包结果
    dist_dir = Path("dist")
    exe_file = dist_dir / "Excel数据集异常值分析工具.exe"
    
    if exe_file.exists():
        print("\n打包成功!")
        print(f"可执行文件位置: {exe_file.absolute()}")
        print("\n使用说明:")
        print("1. 双击exe文件运行程序")
        print("2. 如果遇到杀毒软件拦截，请添加信任或例外")
        print("3. 首次运行可能需要等待较长时间")
    else:
        print("\n打包失败，未找到生成的exe文件")
        print("请检查上述输出中的错误信息")

if __name__ == "__main__":
    main() 