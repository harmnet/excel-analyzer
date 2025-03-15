#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
火山引擎API调用工具

这个模块提供了一个通用的火山引擎API调用类，可以被其他程序方便地调用。
支持模型对话、参数自定义、流式输出等功能。
"""

import os
import json
from typing import List, Dict, Union, Optional, Any, Callable, Generator
from openai import OpenAI


class VolcanoEngineAPI:
    """火山引擎API调用类，提供与火山引擎API交互的方法"""
    
    def __init__(self, api_key: str = "026f661d-3948-42e1-acdd-81e64e62da1b", base_url: str = "https://ark.cn-beijing.volces.com/api/v3"):
        """
        初始化VolcanoEngineAPI实例
        
        参数:
            api_key: 火山引擎API密钥，如果为None，则尝试从环境变量VOLCANO_API_KEY获取
            base_url: 火山引擎API的基础URL
        """
        self.api_key = api_key or os.environ.get("VOLCANO_API_KEY")
        if not self.api_key:
            raise ValueError("API密钥未提供，请通过参数传入或设置VOLCANO_API_KEY环境变量")
        
        self.base_url = base_url
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "deepseek-r1-250120",
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> Union[Any, Generator]:
        """
        调用火山引擎的聊天完成API
        
        参数:
            messages: 消息列表，包含角色和内容
            model: 使用的模型，默认为"deepseek-r1-250120"
            stream: 是否使用流式输出，默认为False
            temperature: 温度参数，控制回答的随机性
            max_tokens: 最大生成token数
            top_p: 核采样参数
            frequency_penalty: 频率惩罚参数
            presence_penalty: 存在惩罚参数
            stop: 停止生成的标记
            stream_callback: 流式输出的回调函数，默认为None
            
        返回:
            API响应对象或流式输出的生成器
        """
        # 构建请求参数
        params = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        # 添加可选参数
        if temperature is not None:
            params["temperature"] = temperature
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        if top_p is not None:
            params["top_p"] = top_p
        if frequency_penalty is not None:
            params["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            params["presence_penalty"] = presence_penalty
        if stop is not None:
            params["stop"] = stop
        
        try:
            # 调用API
            response = self.client.chat.completions.create(**params)
            
            # 处理流式输出
            if stream:
                return self._handle_streaming_response(response, stream_callback)
            else:
                return response
        except Exception as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def _handle_streaming_response(self, stream, callback: Optional[Callable] = None):
        """
        处理流式响应
        
        参数:
            stream: 流式响应对象
            callback: 回调函数，用于处理每个流式响应块
            
        返回:
            生成器，产生流式响应的每个部分
        """
        for chunk in stream:
            if not chunk.choices:
                continue
            
            content = chunk.choices[0].delta.content
            if content is not None and callback:
                callback(content)
            
            yield chunk
    
    def simple_chat(
        self,
        query: str,
        system_prompt: Optional[str] = "你是人工智能助手",
        model: str = "deepseek-r1-250120",
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> Union[Any, Generator]:
        """
        简单的聊天接口，只需提供查询内容
        
        参数:
            query: 用户查询内容
            system_prompt: 系统提示词，默认为"你是人工智能助手"
            model: 使用的模型
            stream: 是否使用流式输出
            temperature: 温度参数
            max_tokens: 最大生成token数
            stream_callback: 流式输出的回调函数
            
        返回:
            API响应对象或流式输出的生成器
        """
        # 构建消息列表
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        # 调用聊天完成API
        return self.chat_completion(
            messages=messages,
            model=model,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            stream_callback=stream_callback
        )
    
    def multi_turn_chat(
        self,
        conversation_history: List[Dict[str, str]],
        model: str = "deepseek-r1-250120",
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> Union[Any, Generator]:
        """
        多轮对话接口，提供完整的对话历史
        
        参数:
            conversation_history: 对话历史，包含角色和内容的消息列表
            model: 使用的模型
            stream: 是否使用流式输出
            temperature: 温度参数
            max_tokens: 最大生成token数
            stream_callback: 流式输出的回调函数
            
        返回:
            API响应对象或流式输出的生成器
        """
        # 调用聊天完成API
        return self.chat_completion(
            messages=conversation_history,
            model=model,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            stream_callback=stream_callback
        )
    
    def extract_response_content(self, response: Any) -> str:
        """
        从API响应中提取内容
        
        参数:
            response: API响应对象
            
        返回:
            响应内容文本
        """
        try:
            return response.choices[0].message.content
        except (AttributeError, IndexError):
            raise ValueError("无法从响应中提取内容")
    
    def extract_streaming_content(self, stream) -> str:
        """
        从流式响应中提取完整内容
        
        参数:
            stream: 流式响应对象
            
        返回:
            完整的响应内容文本
        """
        content = ""
        for chunk in stream:
            if not chunk.choices:
                continue
            
            delta_content = chunk.choices[0].delta.content
            if delta_content is not None:
                content += delta_content
        
        return content


# 使用示例
if __name__ == "__main__":
    # 从环境变量获取API密钥
    # import os
    # os.environ["VOLCANO_API_KEY"] = "你的API密钥"
    
    # 初始化API客户端
    api = VolcanoEngineAPI(api_key="026f661d-3948-42e1-acdd-81e64e62da1b")  # 替换为你的实际API密钥
    
    # 示例1：标准请求
    print("----- 标准请求 -----")
    response = api.simple_chat(
        query="常见的十字花科植物有哪些？",
        system_prompt="你是人工智能助手"
    )
    print(api.extract_response_content(response))
    
    # 示例2：流式请求
    print("\n----- 流式请求 -----")
    
    def print_callback(content):
        print(content, end="")
    
    stream = api.simple_chat(
        query="常见的十字花科植物有哪些？",
        system_prompt="你是人工智能助手",
        stream=True,
        stream_callback=print_callback
    )
    
    # 消耗生成器
    for _ in stream:
        pass
    
    print()  # 换行 