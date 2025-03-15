#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kimi文件API调用示例

这个脚本展示了如何使用KimiFileAPI类进行文件上传和对话。
"""

import os
from kimi_file_api import KimiFileAPI

def main():
    """主函数，展示KimiFileAPI的使用方法"""
    
    # 设置API密钥（实际使用时请替换为你的API密钥或通过环境变量设置）
    # os.environ["MOONSHOT_API_KEY"] = "你的API密钥"
    
    # 方法1：通过环境变量设置API密钥
    # api_key = os.environ.get("MOONSHOT_API_KEY")
    # kimi_api = KimiFileAPI(api_key=api_key)
    
    # 方法2：直接传入API密钥
    kimi_api = "sk-uMgSk5k16xVya8DMUSpBH0inGDg0v42XT6bKLuqlTkbcJtTA"
    
    # 示例1：一站式处理 - 上传文件并进行对话
    print("示例1：一站式处理 - 上传文件并进行对话")
    try:
        response = kimi_api.process_file_and_chat(
            file_path="example.pdf",  # 替换为你的文件路径
            query="请简单介绍这个文件讲了什么",
            temperature=0.3
        )
        print(f"Kimi回答: {response.choices[0].message.content}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print("\n" + "-" * 50 + "\n")
    
    # 示例2：分步骤操作
    print("示例2：分步骤操作")
    try:
        # 步骤1：上传文件
        print("步骤1：上传文件")
        file_obj = kimi_api.upload_file("example.pdf")  # 替换为你的文件路径
        print(f"文件ID: {file_obj.id}")
        
        # 步骤2：获取文件内容
        print("步骤2：获取文件内容")
        content = kimi_api.get_file_content(file_obj.id)
        print(f"文件内容长度: {len(content)} 字符")
        
        # 步骤3：进行对话
        print("步骤3：进行对话")
        response = kimi_api.chat_with_file(
            file_content=content,
            query="请总结一下这个文档的主要内容",
            temperature=0.3
        )
        print(f"Kimi回答: {response.choices[0].message.content}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print("\n" + "-" * 50 + "\n")
    
    # 示例3：自定义系统提示词和模型
    print("示例3：自定义系统提示词和模型")
    try:
        custom_system_prompt = "你是一位专业的文档分析专家，请用简洁的语言分析文档内容。"
        response = kimi_api.process_file_and_chat(
            file_path="example.pdf",  # 替换为你的文件路径
            query="这个文档的创新点是什么？",
            system_prompt=custom_system_prompt,
            model="moonshot-v1-32k",
            temperature=0.2
        )
        print(f"Kimi回答: {response.choices[0].message.content}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print("\n" + "-" * 50 + "\n")
    
    # 示例4：添加额外的消息进行多轮对话
    print("示例4：添加额外的消息进行多轮对话")
    try:
        # 上传文件
        file_obj = kimi_api.upload_file("example.pdf")  # 替换为你的文件路径
        
        # 获取文件内容
        content = kimi_api.get_file_content(file_obj.id)
        
        # 构建多轮对话
        additional_messages = [
            {"role": "user", "content": "这个文档主要讲了什么？"},
            {"role": "assistant", "content": "这个文档主要介绍了XLNet模型，它是一种基于Transformer-XL的预训练语言模型，结合了自回归语言建模和自编码方法的优点。"},
            {"role": "user", "content": "XLNet与BERT有什么区别？"}
        ]
        
        # 进行对话
        response = kimi_api.chat_with_file(
            file_content=content,
            query="",  # 这里不需要额外的查询，因为已经在additional_messages中包含了
            additional_messages=additional_messages
        )
        print(f"Kimi回答: {response.choices[0].message.content}")
    except Exception as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main() 