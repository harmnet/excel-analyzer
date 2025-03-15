# Excel数据集异常值分析工具

这是一个使用大型语言模型分析Excel数据集中异常值的图形界面工具。该工具可以帮助数据分析师快速识别数据集中的异常值，并提供详细的分析报告。

## 功能特点

- 简洁直观的图形用户界面
- 支持多种大型语言模型（Moonshot、硅基流动、火山引擎）
- 自动分批处理大型数据集
- 生成结构化的异常值分析报告
- 将分析结果保存为Word文档
- 支持Windows系统独立运行（无需安装Python）

## 使用方法

### 直接运行Python脚本

1. 确保已安装Python 3.7+
2. 安装必要的依赖：
   ```
   pip install pandas openpyxl openai python-docx PyQt5
   ```
3. 运行主程序：
   ```
   python excel_analyzer_gui.py
   ```

### 使用Windows可执行文件

1. 双击运行`Excel数据集异常值分析工具.exe`
2. 如果遇到杀毒软件拦截，请添加信任或例外
3. 首次运行可能需要等待较长时间

## 打包为Windows可执行文件

1. 安装PyInstaller：
   ```
   pip install pyinstaller
   ```
2. 运行打包脚本：
   ```
   python build_windows_exe.py
   ```
3. 打包完成后，可执行文件将位于`dist`目录中

## 支持的模型

- Moonshot AI (32K/128K上下文)
- 硅基流动 DeepSeek-R1/V3 (64K上下文)
- 硅基流动 千问QwQ-32B (32K上下文)
- 火山引擎 DeepSeek-R1 (64K上下文)

## 注意事项

- Excel文件大小限制为500KB
- 分析大型数据集可能需要较长时间
- 默认API密钥可能有使用限制，建议使用自己的API密钥

## 常见问题

### API调用速度慢

大型语言模型API调用速度受多种因素影响：
- 模型计算资源消耗大
- 网络传输延迟
- API服务商的限流机制
- 数据批次处理和等待时间设置

### 如何使用自己的API密钥

目前需要直接修改源代码中的默认API密钥常量：
- Moonshot API: `DEFAULT_MOONSHOT_API_KEY`
- 硅基流动API: `DEFAULT_SILICONFLOW_API_KEY`
- 火山引擎API: `DEFAULT_VOLCANO_API_KEY`

## 许可证

本项目仅供学习和研究使用。 