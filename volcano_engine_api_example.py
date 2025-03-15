#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
火山引擎API调用示例

这个脚本展示了如何使用VolcanoEngineAPI类进行各种API调用。
"""

import os
import time
from volcano_engine_api import VolcanoEngineAPI

def print_separator():
    """打印分隔线"""
    print("\n" + "-" * 50 + "\n")

def stream_callback(content):
    """流式输出的回调函数"""
    print(content, end="", flush=True)

def main():
    """主函数，展示VolcanoEngineAPI的使用方法"""
    
    # 设置API密钥（实际使用时请替换为你的API密钥或通过环境变量设置）
    # os.environ["VOLCANO_API_KEY"] = "你的API密钥"
    
    # 方法1：通过环境变量设置API密钥
    # api_key = os.environ.get("VOLCANO_API_KEY")
    # api = VolcanoEngineAPI(api_key=api_key)
    
    # 方法2：直接传入API密钥
    api = VolcanoEngineAPI(api_key="026f661d-3948-42e1-acdd-81e64e62da1b")  # 替换为你的实际API密钥
    
    # 示例1：简单对话
    print("示例1：简单对话")
    try:
        response = api.simple_chat(
            query="请介绍一下火山引擎的主要功能",
            system_prompt="你是一位专业的技术顾问，擅长介绍各种云服务和技术产品"
        )
        print(f"回答: {api.extract_response_content(response)}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print_separator()
    
    # 示例2：设置温度参数
    print("示例2：设置温度参数")
    try:
        response = api.simple_chat(
            query="写一首关于人工智能的短诗",
            system_prompt="你是一位富有创意的诗人",
            temperature=0.8  # 较高的温度使输出更有创意
        )
        print(f"回答: {api.extract_response_content(response)}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print_separator()
    
    # 示例3：多轮对话
    print("示例3：多轮对话")
    try:
        conversation = [
            {"role": "system", "content": "你是一位专业的科学顾问，擅长解释科学概念"},
            {"role": "user", "content": "什么是量子计算？"},
            {"role": "assistant", "content": "量子计算是一种利用量子力学现象（如叠加和纠缠）进行计算的技术。传统计算机使用位（0或1）作为信息的基本单位，而量子计算机使用量子比特（可以同时处于0和1的叠加状态）。这使得量子计算机在某些特定问题上可能比传统计算机快得多。"},
            {"role": "user", "content": "量子计算机与传统计算机相比有什么优势？"}
        ]
        response = api.multi_turn_chat(conversation)
        print(f"回答: {api.extract_response_content(response)}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print_separator()
    
    # 示例4：流式输出
    print("示例4：流式输出")
    try:
        print("回答: ", end="")
        stream = api.simple_chat(
            query="请简要介绍一下深度学习的基本原理",
            system_prompt="你是一位AI研究专家",
            stream=True,
            stream_callback=stream_callback
        )
        
        # 消耗生成器
        for _ in stream:
            pass
        
        print()  # 换行
    except Exception as e:
        print(f"\n错误: {str(e)}")
    
    print_separator()
    
    # 示例5：设置最大生成token数
    print("示例5：设置最大生成token数")
    try:
        response = api.simple_chat(
            query="请详细介绍一下火山引擎的人工智能服务",
            max_tokens=150  # 限制回答长度
        )
        print(f"回答: {api.extract_response_content(response)}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print_separator()
    
    # 示例6：完整参数设置
    print("示例6：完整参数设置")
    try:
        response = api.chat_completion(
            messages=[
                {"role": "system", "content": "你是一位专业的技术文档撰写者"},
                {"role": "user", "content": "请写一个Python函数，用于计算斐波那契数列"}
            ],
            model="deepseek-r1-250120",
            temperature=0.2,  # 低温度，更确定性的输出
            max_tokens=300,
            top_p=0.9,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )
        print(f"回答: {api.extract_response_content(response)}")
    except Exception as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main() 