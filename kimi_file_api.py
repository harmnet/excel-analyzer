#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kimi文件API调用工具

这个模块提供了一个通用的Kimi文件API调用类，可以被其他程序方便地调用。
支持上传文件、获取文件内容、基于文件内容进行对话等功能。
"""

import os
import time
import re
import json
import requests
from pathlib import Path
from typing import List, Dict, Union, Optional, Any
from openai import OpenAI


class KimiFileAPI:
    """Kimi文件API调用类，提供与Kimi文件API交互的方法"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.moonshot.cn/v1"):
        """
        初始化KimiFileAPI实例
        
        参数:
            api_key: Moonshot API密钥，如果为None，则尝试从环境变量MOONSHOT_API_KEY获取
            base_url: Moonshot API的基础URL
        """
        self.api_key = api_key or os.environ.get("MOONSHOT_API_KEY")
        if not self.api_key:
            raise ValueError("API密钥未提供，请通过参数传入或设置MOONSHOT_API_KEY环境变量")
        
        self.base_url = base_url
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # 设置请求头
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def upload_file(self, file_path: Union[str, Path], purpose: str = "file-extract") -> Any:
        """
        上传文件到Kimi API
        
        参数:
            file_path: 文件路径，可以是字符串或Path对象
            purpose: 文件用途，默认为"file-extract"
            
        返回:
            文件对象，包含文件ID等信息
        """
        file_path = Path(file_path) if isinstance(file_path, str) else file_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 添加重试机制
        max_retries = 3  # 减少重试次数
        retry_count = 0
        retry_delay = 30  # 增加初始等待时间到30秒
        
        while retry_count < max_retries:
            try:
                print(f"正在上传文件... (尝试 {retry_count + 1}/{max_retries})")
                # 使用OpenAI客户端上传文件
                with open(file_path, "rb") as file:
                    file_object = self.client.files.create(
                        file=file,
                        purpose=purpose
                    )
                return file_object
            except Exception as e:
                error_str = str(e)
                retry_count += 1
                
                # 检查是否是频率限制错误
                if "rate_limit_reached_error" in error_str:
                    # 尝试从错误消息中提取等待时间
                    wait_time_match = re.search(r'try again after (\d+) seconds', error_str)
                    wait_time = int(wait_time_match.group(1)) if wait_time_match else retry_delay
                    
                    # 增加等待时间，确保至少等待30秒
                    wait_time = max(wait_time, 30)
                    
                    print(f"上传文件时遇到API频率限制，等待 {wait_time} 秒后重试... (尝试 {retry_count}/{max_retries})")
                    
                    # 倒计时显示
                    for i in range(wait_time, 0, -1):
                        print(f"\r等待中... {i} 秒", end="", flush=True)
                        time.sleep(1)
                    print("\r等待完成，继续请求...                 ")
                    
                    # 增加下次重试的等待时间
                    retry_delay = min(retry_delay * 2, 120)  # 最多等待120秒
                    continue
                
                # 如果不是频率限制错误，或者已经达到最大重试次数，则抛出异常
                if retry_count >= max_retries:
                    raise Exception(f"上传文件失败，达到最大重试次数 ({max_retries}): {error_str}")
                
                print(f"上传文件失败，{retry_delay}秒后重试: {error_str}")
                time.sleep(retry_delay)
                # 增加下次重试的等待时间
                retry_delay = min(retry_delay * 2, 120)
                continue
        
        # 如果所有重试都失败，抛出异常
        raise Exception(f"上传文件失败: 达到最大重试次数")
    
    def get_file_content(self, file_id: str) -> str:
        """
        获取已上传文件的内容
        
        参数:
            file_id: 文件ID，通过upload_file方法获取
            
        返回:
            文件内容的文本表示
        """
        # 添加重试机制
        max_retries = 3  # 减少重试次数
        retry_count = 0
        retry_delay = 30  # 增加初始等待时间到30秒
        
        while retry_count < max_retries:
            try:
                print(f"正在获取文件内容... (尝试 {retry_count + 1}/{max_retries})")
                # 使用OpenAI客户端获取文件内容
                content_response = self.client.files.content(file_id)
                return content_response.text
            except Exception as e:
                error_str = str(e)
                retry_count += 1
                
                # 检查是否是频率限制错误
                if "rate_limit_reached_error" in error_str:
                    # 尝试从错误消息中提取等待时间
                    wait_time_match = re.search(r'try again after (\d+) seconds', error_str)
                    wait_time = int(wait_time_match.group(1)) if wait_time_match else retry_delay
                    
                    # 增加等待时间，确保至少等待30秒
                    wait_time = max(wait_time, 30)
                    
                    print(f"获取文件内容时遇到API频率限制，等待 {wait_time} 秒后重试... (尝试 {retry_count}/{max_retries})")
                    
                    # 倒计时显示
                    for i in range(wait_time, 0, -1):
                        print(f"\r等待中... {i} 秒", end="", flush=True)
                        time.sleep(1)
                    print("\r等待完成，继续请求...                 ")
                    
                    # 增加下次重试的等待时间
                    retry_delay = min(retry_delay * 2, 120)  # 最多等待120秒
                    continue
                
                # 如果不是频率限制错误，或者已经达到最大重试次数，则抛出异常
                if retry_count >= max_retries:
                    raise Exception(f"获取文件内容失败，达到最大重试次数 ({max_retries}): {error_str}")
                
                print(f"获取文件内容失败，{retry_delay}秒后重试: {error_str}")
                time.sleep(retry_delay)
                # 增加下次重试的等待时间
                retry_delay = min(retry_delay * 2, 120)
                continue
        
        # 如果所有重试都失败，抛出异常
        raise Exception(f"获取文件内容失败: 达到最大重试次数")
    
    def chat_with_file(
        self, 
        file_id: Optional[str] = None,
        file_content: Optional[str] = None,
        query: str = "",
        model: str = "moonshot-v1-32k",
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        additional_messages: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """
        基于文件内容与Kimi进行对话
        
        参数:
            file_id: 文件ID，如果提供，会自动获取文件内容
            file_content: 文件内容，如果已经有文件内容，可以直接提供
            query: 用户查询内容
            model: 使用的模型，默认为"moonshot-v1-32k"
            system_prompt: 系统提示词，如果为None则使用默认提示词
            temperature: 温度参数，控制回答的随机性
            max_tokens: 最大生成token数
            additional_messages: 额外的消息列表，可以添加到对话中
            
        返回:
            Kimi的回答对象
        """
        if not file_id and not file_content:
            raise ValueError("必须提供file_id或file_content中的一个")
        
        # 如果提供了file_id但没有file_content，则获取文件内容
        if file_id and not file_content:
            file_content = self.get_file_content(file_id)
        
        # 默认系统提示词
        default_system_prompt = "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
        
        # 构建消息列表
        messages = [
            {
                "role": "system",
                "content": system_prompt or default_system_prompt,
            }
        ]
        
        # 添加文件内容作为系统消息
        if file_content:
            messages.append({
                "role": "system",
                "content": file_content,
            })
        
        # 添加额外的消息
        if additional_messages:
            messages.extend(additional_messages)
        
        # 添加用户查询
        if query:
            messages.append({"role": "user", "content": query})
        
        # 调用chat completion API
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            params["max_tokens"] = max_tokens
        
        # 添加重试机制
        max_retries = 3  # 减少重试次数
        retry_count = 0
        retry_delay = 30  # 增加初始等待时间到30秒
        
        while retry_count < max_retries:
            try:
                print(f"正在发送聊天请求... (尝试 {retry_count + 1}/{max_retries})")
                completion = self.client.chat.completions.create(**params)
                return completion
            except Exception as e:
                error_str = str(e)
                retry_count += 1
                
                # 检查是否是频率限制错误
                if "rate_limit_reached_error" in error_str:
                    # 尝试从错误消息中提取等待时间
                    wait_time_match = re.search(r'try again after (\d+) seconds', error_str)
                    wait_time = int(wait_time_match.group(1)) if wait_time_match else retry_delay
                    
                    # 增加等待时间，确保至少等待30秒
                    wait_time = max(wait_time, 30)
                    
                    print(f"调用聊天API时遇到频率限制，等待 {wait_time} 秒后重试... (尝试 {retry_count}/{max_retries})")
                    
                    # 倒计时显示
                    for i in range(wait_time, 0, -1):
                        print(f"\r等待中... {i} 秒", end="", flush=True)
                        time.sleep(1)
                    print("\r等待完成，继续请求...                 ")
                    
                    # 增加下次重试的等待时间
                    retry_delay = min(retry_delay * 2, 120)  # 最多等待120秒
                    continue
                
                # 如果不是频率限制错误，或者已经达到最大重试次数，则抛出异常
                if retry_count >= max_retries:
                    raise Exception(f"调用聊天API失败，达到最大重试次数 ({max_retries}): {error_str}")
                
                print(f"调用聊天API失败，{retry_delay}秒后重试: {error_str}")
                time.sleep(retry_delay)
                # 增加下次重试的等待时间
                retry_delay = min(retry_delay * 2, 120)
                continue
        
        # 如果所有重试都失败，抛出异常
        raise Exception(f"调用聊天API失败: 达到最大重试次数")
    
    def process_file_and_chat(
        self, 
        file_path: Union[str, Path],
        query: str,
        model: str = "moonshot-v1-32k",
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        additional_messages: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """
        一站式处理：上传文件并基于文件内容进行对话
        
        参数:
            file_path: 文件路径
            query: 用户查询内容
            model: 使用的模型
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大生成token数
            additional_messages: 额外的消息列表
            
        返回:
            Kimi的回答对象
        """
        # 上传文件
        print("正在上传文件到Moonshot API...")
        file_object = self.upload_file(file_path)
        print(f"文件上传成功，文件ID: {file_object.id}")
        
        # 获取文件内容
        print("正在获取文件内容...")
        file_content = self.get_file_content(file_object.id)
        content_preview = file_content[:100] + "..." if len(file_content) > 100 else file_content
        print(f"文件内容获取成功，预览: {content_preview}")
        
        # 进行对话
        print(f"正在使用模型 {model} 进行对话分析...")
        return self.chat_with_file(
            file_content=file_content,
            query=query,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_messages=additional_messages
        )


# 使用示例
if __name__ == "__main__":
    # 从环境变量获取API密钥
    # import os
    # os.environ["MOONSHOT_API_KEY"] = "你的API密钥"
    
    # 初始化API客户端
    api_key = "sk-uMgSk5k16xVya8DMUSpBH0inGDg0v42XT6bKLuqlTkbcJtTA"
    kimi_api = KimiFileAPI(api_key=api_key)
    
    # 示例1：上传文件并进行对话
    response = kimi_api.process_file_and_chat(
        file_path="example.pdf",
        query="请简单介绍这个文件讲了什么"
    )
    print(response.choices[0].message.content)
    
    # 示例2：分步骤操作
    # 上传文件
    # file_obj = kimi_api.upload_file("example.pdf")
    # 获取文件内容
    # content = kimi_api.get_file_content(file_obj.id)
    # 进行对话
    # response = kimi_api.chat_with_file(
    #     file_content=content,
    #     query="请总结一下这个文档的主要内容"
    # )
    # print(response.choices[0].message.content) 