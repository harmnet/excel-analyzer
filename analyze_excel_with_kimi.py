#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Excel数据集异常值分析程序

这个程序使用pandas读取Excel文件，然后将数据发送给Moonshot API，
让Kimi大模型分析数据集中的异常值，以表格形式返回异常字段的描述、问题分析和处理建议。
"""

import os
import sys
import time
import datetime
import json
import pandas as pd
from pathlib import Path
from openai import OpenAI

def show_spinner(seconds, message="处理中"):
    """显示加载动画"""
    spinner = "|/-\\"
    for _ in range(int(seconds * 5)):
        for char in spinner:
            sys.stdout.write(f"\r{message} {char}")
            sys.stdout.flush()
            time.sleep(0.2)
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
    sys.stdout.flush()

def main():
    print("="*50)
    print("Excel数据集异常值分析程序")
    print("="*50)
    print("本程序将使用Kimi大模型分析Excel数据集中的异常值")
    print()
    
    try:
        # 设置API密钥
        api_key = "sk-uMgSk5k16xVya8DMUSpBH0inGDg0v42XT6bKLuqlTkbcJtTA"
        
        # 获取用户主目录
        home_dir = Path(os.path.expanduser("~"))
        
        # 构建Excel文件的完整路径
        excel_file_path = home_dir / "Desktop" / "《商务数据分析基础》数据集-电子商务-完整数据.xlsx"
        
        # 检查文件是否存在
        if not excel_file_path.exists():
            print(f"错误：文件 {excel_file_path} 不存在！")
            print("请确认文件名称是否正确，以及文件是否位于桌面上")
            return
        
        print(f"找到文件：{excel_file_path}")
        print("文件大小：{:.2f} MB".format(excel_file_path.stat().st_size / (1024 * 1024)))
        
        # 使用pandas读取Excel文件
        print("\n正在读取Excel文件...")
        show_spinner(1, "读取中")
        
        try:
            # 读取Excel文件
            df = pd.read_excel(excel_file_path)
            print(f"成功读取Excel文件，共有 {len(df)} 行，{len(df.columns)} 列")
            
            # 显示数据预览
            print("\n数据预览 (前5行):")
            print(df.head().to_string())
            
            # 显示数据类型
            print("\n数据类型:")
            print(df.dtypes)
            
            # 将数据转换为文本格式
            print("\n正在准备数据...")
            show_spinner(1, "准备中")
            
            # 使用全部数据进行分析
            print(f"将使用全部 {len(df)} 行数据进行分析")
            print("(使用moonshot-v1-128k模型，可以处理大量数据)")
            
            # 转换为文本格式
            data_text = "数据集信息：\n"
            data_text += f"- 行数：{len(df)}\n"
            data_text += f"- 列数：{len(df.columns)}\n"
            data_text += f"- 列名：{', '.join(df.columns.tolist())}\n\n"
            
            # 添加数据类型信息
            data_text += "数据类型：\n"
            for col, dtype in df.dtypes.items():
                data_text += f"- {col}: {dtype}\n"
            
            data_text += "\n数据预览（全部数据）：\n"
            data_text += df.to_string(max_rows=None, max_cols=None)
            
            print("\n正在初始化Moonshot API客户端...")
            show_spinner(1, "初始化中")
            
            # 初始化OpenAI客户端
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.moonshot.cn/v1"
            )
            
            # 设置使用的模型
            model_name = "moonshot-v1-128k"
            print(f"\n使用模型：{model_name}")
            print("该模型拥有128K的上下文窗口，可以处理更大的文件和更复杂的分析任务")
            
            # 构建查询提示
            query = """
            请详细分析这个Excel数据集中哪些字段的值存在异常。
            
            请以表格形式提供以下信息：
            1. 异常字段名称
            2. 异常值描述（包括异常值的范围、类型或具体例子）
            3. 问题分析（为什么这些值被认为是异常的，可能的原因）
            4. 处理建议（如何清洗或修正这些异常值的具体方法）
            
            表格应该包含这四列，并为每个发现的异常字段提供一行数据。
            如果没有发现异常，请说明数据集看起来正常。
            
            在回答前，请先简要描述一下这个数据集的基本情况，包括：
            - 数据集的行数和列数
            - 各列的数据类型
            - 数据集的主要内容和用途
            - 数据的时间范围（如果适用）
            
            最后，请提供一些关于这个数据集整体质量的建议，以及如何更好地利用这些数据进行商务分析。
            """
            
            # 发送聊天请求
            print("\n正在请求Kimi分析数据集...")
            print(f"(使用{model_name}模型分析，过程可能需要几分钟时间，请耐心等待)")
            
            start_time = time.time()
            
            # 添加重试机制
            max_retries = 3
            retry_count = 0
            retry_delay = 30
            
            while retry_count < max_retries:
                try:
                    print(f"正在发送聊天请求... (尝试 {retry_count + 1}/{max_retries})")
                    
                    # 使用简单的消息格式
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {
                                "role": "system",
                                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手。你将分析一个Excel数据集，寻找其中的异常值。"
                            },
                            {
                                "role": "system",
                                "content": data_text
                            },
                            {
                                "role": "user",
                                "content": query
                            }
                        ],
                        temperature=0.2
                    )
                    
                    # 计算处理时间
                    process_time = time.time() - start_time
                    
                    # 获取Kimi的回答内容
                    analysis_result = response.choices[0].message.content
                    
                    # 打印Kimi的回答
                    print("\n" + "="*80 + "\n")
                    print("Kimi的数据集异常分析结果：\n")
                    print(analysis_result)
                    print("\n" + "="*80)
                    print(f"\n分析耗时：{process_time:.2f} 秒")
                    
                    # 保存分析结果到文件
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    result_file_path = home_dir / "Desktop" / f"数据集异常分析结果_{model_name}_{timestamp}.txt"
                    
                    with open(result_file_path, "w", encoding="utf-8") as f:
                        f.write("数据集异常分析结果\n")
                        f.write("="*50 + "\n\n")
                        f.write(f"分析时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"分析文件: {excel_file_path.name}\n")
                        f.write(f"使用模型: {model_name}\n")
                        f.write(f"处理耗时: {process_time:.2f} 秒\n\n")
                        f.write("="*50 + "\n\n")
                        f.write(analysis_result)
                    
                    print(f"\n分析结果已保存到: {result_file_path}")
                    
                    # 成功获取结果，跳出循环
                    break
                    
                except Exception as e:
                    error_str = str(e)
                    retry_count += 1
                    
                    # 打印详细的错误信息
                    print(f"\n错误详情: {error_str}")
                    print(f"错误类型: {type(e).__name__}")
                    
                    # 如果是API错误，尝试提取更多信息
                    if hasattr(e, 'response'):
                        try:
                            error_response = e.response
                            print(f"API错误状态码: {error_response.status_code}")
                            error_json = error_response.json()
                            print(f"API错误信息: {json.dumps(error_json, ensure_ascii=False, indent=2)}")
                        except:
                            print("无法解析API错误响应")
                    
                    # 检查是否是频率限制错误
                    if "rate_limit_reached_error" in error_str:
                        # 尝试从错误消息中提取等待时间
                        import re
                        wait_time_match = re.search(r'try again after (\d+) seconds', error_str)
                        wait_time = int(wait_time_match.group(1)) if wait_time_match else retry_delay
                        
                        # 增加等待时间，确保至少等待30秒
                        wait_time = max(wait_time, 30)
                        
                        print(f"调用API时遇到频率限制，等待 {wait_time} 秒后重试... (尝试 {retry_count}/{max_retries})")
                        
                        # 倒计时显示
                        for i in range(wait_time, 0, -1):
                            print(f"\r等待中... {i} 秒", end="", flush=True)
                            time.sleep(1)
                        print("\r等待完成，继续请求...                 ")
                        
                        # 增加下次重试的等待时间
                        retry_delay = min(retry_delay * 2, 120)
                        continue
                    
                    # 如果不是频率限制错误，或者已经达到最大重试次数，则抛出异常
                    if retry_count >= max_retries:
                        raise Exception(f"调用API失败: 达到最大重试次数 ({max_retries})")
                    
                    print(f"调用API失败，{retry_delay}秒后重试: {error_str}")
                    time.sleep(retry_delay)
                    # 增加下次重试的等待时间
                    retry_delay = min(retry_delay * 2, 120)
            
            # 如果所有重试都失败，抛出异常
            if retry_count >= max_retries:
                raise Exception("调用API失败: 达到最大重试次数")
                
        except pd.errors.EmptyDataError:
            print("错误：Excel文件为空")
        except pd.errors.ParserError:
            print("错误：无法解析Excel文件，文件可能已损坏")
        except Exception as e:
            print(f"分析过程中出错：{str(e)}")
            print("请检查您的API密钥是否正确，以及网络连接是否正常")
        
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错：{str(e)}")
    finally:
        print("\n程序执行完毕")

if __name__ == "__main__":
    main()