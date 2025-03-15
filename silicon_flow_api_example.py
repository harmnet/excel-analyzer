#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
硅基流动API调用示例

这个脚本展示了如何使用SiliconFlowAPI类进行各种API调用。
"""

import os
import json
from silicon_flow_api import SiliconFlowAPI

def print_separator():
    """打印分隔线"""
    print("\n" + "-" * 50 + "\n")

def stream_callback(chunk):
    """流式输出的回调函数"""
    try:
        content = chunk["choices"][0]["delta"]["content"]
        if content:
            print(content, end="", flush=True)
    except (KeyError, IndexError):
        pass

def main():
    """主函数，展示SiliconFlowAPI的使用方法"""
    
    # 设置API密钥（实际使用时请替换为你的API密钥或通过环境变量设置）
    # os.environ["SILICONFLOW_API_KEY"] = "你的API密钥"
    
    # 方法1：通过环境变量设置API密钥
    # api_key = os.environ.get("SILICONFLOW_API_KEY")
    # api = SiliconFlowAPI(api_key=api_key)
    
    # 方法2：直接传入API密钥
    api = SiliconFlowAPI(api_key="你的API密钥")  # 替换为你的实际API密钥
    
    # 示例1：简单对话
    print("示例1：简单对话")
    try:
        response = api.simple_chat(
            query="中国大模型行业2025年将会迎来哪些机遇和挑战？",
            temperature=0.7,
            max_tokens=512
        )
        print(f"回答: {api.extract_response_content(response)}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print_separator()
    
    # 示例2：带系统提示词的对话
    print("示例2：带系统提示词的对话")
    try:
        system_prompt = "你是一位专业的科技分析师，擅长分析技术趋势和市场前景。请用专业、客观的语言回答问题。"
        response = api.simple_chat(
            query="量子计算在未来5年内可能会有哪些突破？",
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=800
        )
        print(f"回答: {api.extract_response_content(response)}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print_separator()
    
    # 示例3：多轮对话
    print("示例3：多轮对话")
    try:
        conversation = [
            {"role": "system", "content": "你是一个专业的AI助手，擅长回答技术问题。"},
            {"role": "user", "content": "什么是大语言模型？"},
            {"role": "assistant", "content": "大语言模型（Large Language Model，简称LLM）是一种基于深度学习的自然语言处理模型，它通过在海量文本数据上训练，学习语言的规律和知识，从而能够理解和生成人类语言。"},
            {"role": "user", "content": "它们有哪些主要应用场景？"}
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
        for _ in api.simple_chat(
            query="请简要介绍一下人工智能的发展历程",
            stream=True,
            stream_callback=stream_callback
        ):
            pass  # 回调函数会处理输出
        print()  # 换行
    except Exception as e:
        print(f"\n错误: {str(e)}")
    
    print_separator()
    
    # 示例5：函数调用
    print("示例5：函数调用")
    try:
        tools = [
            {
                "type": "function",
                "function": {
                    "description": "获取当前天气信息",
                    "name": "get_weather",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "城市名称，如北京、上海等"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "温度单位"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]
        response = api.function_calling_chat(
            query="北京今天的天气怎么样？",
            tools=tools
        )
        
        # 检查是否有函数调用
        message = response["choices"][0]["message"]
        if "tool_calls" in message:
            tool_calls = message["tool_calls"]
            print(f"函数调用: {json.dumps(tool_calls, ensure_ascii=False, indent=2)}")
        else:
            print(f"回答: {message['content']}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print_separator()
    
    # 示例6：自定义参数
    print("示例6：自定义参数")
    try:
        response = api.chat_completion(
            messages=[{"role": "user", "content": "写一首关于人工智能的短诗"}],
            model="Pro/deepseek-ai/DeepSeek-V3",
            temperature=0.9,  # 高温度，更有创意
            max_tokens=200,
            top_p=0.95,
            top_k=40,
            frequency_penalty=0.7  # 增加多样性
        )
        print(f"回答: {api.extract_response_content(response)}")
    except Exception as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main() 