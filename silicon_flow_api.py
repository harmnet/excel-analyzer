#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
硅基流动API调用工具

这个模块提供了一个通用的硅基流动API调用类，可以被其他程序方便地调用。
支持模型对话、参数自定义、流式输出等功能。
"""

import os
import json
import requests
from typing import List, Dict, Union, Optional, Any, Callable


class SiliconFlowAPI:
    """硅基流动API调用类，提供与硅基流动API交互的方法"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.siliconflow.cn/v1"):
        """
        初始化SiliconFlowAPI实例
        
        参数:
            api_key: 硅基流动API密钥，如果为None，则尝试从环境变量SILICONFLOW_API_KEY获取
            base_url: 硅基流动API的基础URL
        """
        self.api_key = api_key or os.environ.get("SILICONFLOW_API_KEY")
        if not self.api_key:
            raise ValueError("API密钥未提供，请通过参数传入或设置SILICONFLOW_API_KEY环境变量")
        
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "Pro/deepseek-ai/DeepSeek-V3",
        stream: bool = False,
        max_tokens: int = 512,
        stop: Optional[List[str]] = None,
        temperature: float = 0.7,
        top_p: float = 0.7,
        top_k: int = 50,
        frequency_penalty: float = 0.5,
        n: int = 1,
        response_format: Optional[Dict[str, str]] = None,
        tools: Optional[List[Dict]] = None,
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> Union[Dict, Any]:
        """
        调用硅基流动的聊天完成API
        
        参数:
            messages: 消息列表，包含角色和内容
            model: 使用的模型，默认为"Pro/deepseek-ai/DeepSeek-V3"
            stream: 是否使用流式输出，默认为False
            max_tokens: 最大生成token数，默认为512
            stop: 停止生成的标记列表，默认为None
            temperature: 温度参数，控制回答的随机性，默认为0.7
            top_p: 核采样参数，默认为0.7
            top_k: 取样的候选数量，默认为50
            frequency_penalty: 频率惩罚参数，默认为0.5
            n: 生成回答的数量，默认为1
            response_format: 响应格式，默认为None
            tools: 工具列表，默认为None
            stream_callback: 流式输出的回调函数，默认为None
            
        返回:
            API响应对象或流式输出的生成器
        """
        url = f"{self.base_url}/chat/completions"
        
        # 构建请求参数
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "frequency_penalty": frequency_penalty,
            "n": n
        }
        
        # 添加可选参数
        if stop:
            payload["stop"] = stop
        else:
            payload["stop"] = ["null"]
            
        if response_format:
            payload["response_format"] = response_format
        else:
            payload["response_format"] = {"type": "text"}
            
        if tools:
            payload["tools"] = tools
        
        try:
            if stream:
                return self._handle_streaming_response(url, payload, stream_callback)
            else:
                response = requests.post(url, json=payload, headers=self.headers)
                response.raise_for_status()  # 抛出HTTP错误
                return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def _handle_streaming_response(self, url: str, payload: Dict, callback: Optional[Callable] = None):
        """
        处理流式响应
        
        参数:
            url: API端点URL
            payload: 请求参数
            callback: 回调函数，用于处理每个流式响应块
            
        返回:
            生成器，产生流式响应的每个部分
        """
        with requests.post(url, json=payload, headers=self.headers, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    # 移除"data: "前缀并解析JSON
                    if line.startswith(b"data: "):
                        json_str = line[6:].decode('utf-8')
                        if json_str.strip() == "[DONE]":
                            break
                        try:
                            chunk = json.loads(json_str)
                            if callback:
                                callback(chunk)
                            yield chunk
                        except json.JSONDecodeError:
                            continue
    
    def simple_chat(
        self,
        query: str,
        system_prompt: Optional[str] = None,
        model: str = "Pro/deepseek-ai/DeepSeek-V3",
        temperature: float = 0.7,
        max_tokens: int = 512,
        stream: bool = False,
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> Union[Dict, Any]:
        """
        简单的聊天接口，只需提供查询内容
        
        参数:
            query: 用户查询内容
            system_prompt: 系统提示词，如果为None则不添加系统消息
            model: 使用的模型
            temperature: 温度参数
            max_tokens: 最大生成token数
            stream: 是否使用流式输出
            stream_callback: 流式输出的回调函数
            
        返回:
            API响应对象或流式输出的生成器
        """
        # 构建消息列表
        messages = []
        
        # 添加系统提示词（如果有）
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 添加用户查询
        messages.append({"role": "user", "content": query})
        
        # 调用聊天完成API
        return self.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            stream_callback=stream_callback
        )
    
    def multi_turn_chat(
        self,
        conversation_history: List[Dict[str, str]],
        model: str = "Pro/deepseek-ai/DeepSeek-V3",
        temperature: float = 0.7,
        max_tokens: int = 512,
        stream: bool = False,
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> Union[Dict, Any]:
        """
        多轮对话接口，提供完整的对话历史
        
        参数:
            conversation_history: 对话历史，包含角色和内容的消息列表
            model: 使用的模型
            temperature: 温度参数
            max_tokens: 最大生成token数
            stream: 是否使用流式输出
            stream_callback: 流式输出的回调函数
            
        返回:
            API响应对象或流式输出的生成器
        """
        # 调用聊天完成API
        return self.chat_completion(
            messages=conversation_history,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            stream_callback=stream_callback
        )
    
    def function_calling_chat(
        self,
        query: str,
        tools: List[Dict],
        system_prompt: Optional[str] = None,
        model: str = "Pro/deepseek-ai/DeepSeek-V3",
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> Dict:
        """
        函数调用聊天接口，支持工具使用
        
        参数:
            query: 用户查询内容
            tools: 工具列表，包含工具定义
            system_prompt: 系统提示词，如果为None则不添加系统消息
            model: 使用的模型
            temperature: 温度参数
            max_tokens: 最大生成token数
            
        返回:
            API响应对象
        """
        # 构建消息列表
        messages = []
        
        # 添加系统提示词（如果有）
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 添加用户查询
        messages.append({"role": "user", "content": query})
        
        # 调用聊天完成API
        return self.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools
        )
    
    def extract_response_content(self, response: Dict) -> str:
        """
        从API响应中提取内容
        
        参数:
            response: API响应对象
            
        返回:
            响应内容文本
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise ValueError("无法从响应中提取内容")


# 使用示例
if __name__ == "__main__":
    # 从环境变量获取API密钥
    # import os
    # os.environ["SILICONFLOW_API_KEY"] = "你的API密钥"
    
    # 初始化API客户端
    api = SiliconFlowAPI(api_key="sk-bivnwauskdbvpspvmdorrgkrpwlyfxbfcezqsfsevowzubdj")
    
    # 示例1：简单对话
    response = api.simple_chat(
        query="中国大模型行业2025年将会迎来哪些机遇和挑战？",
        temperature=0.7,
        max_tokens=512
    )
    print(api.extract_response_content(response))
    
    # 示例2：多轮对话
    conversation = [
        {"role": "system", "content": "你是一个专业的AI助手，擅长回答技术问题。"},
        {"role": "user", "content": "什么是大语言模型？"},
        {"role": "assistant", "content": "大语言模型（Large Language Model，简称LLM）是一种基于深度学习的自然语言处理模型，它通过在海量文本数据上训练，学习语言的规律和知识，从而能够理解和生成人类语言。"},
        {"role": "user", "content": "它们有哪些主要应用场景？"}
    ]
    response = api.multi_turn_chat(conversation)
    print(api.extract_response_content(response))
    
    # 示例3：函数调用
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
    print(json.dumps(response, ensure_ascii=False, indent=2)) 