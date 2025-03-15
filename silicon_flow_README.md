# 硅基流动API调用工具

这个项目提供了一个通用的硅基流动API调用类，可以被其他程序方便地调用。支持模型对话、参数自定义、流式输出、函数调用等功能。

## 功能特点

- 简单对话：快速进行单轮对话
- 多轮对话：支持完整的对话历史
- 流式输出：实时获取模型生成内容
- 函数调用：支持工具使用和函数调用
- 参数自定义：灵活配置模型参数
- 错误处理：完善的异常处理机制

## 安装

### 前提条件

- Python 3.7+
- requests库

### 安装依赖

```bash
pip install requests
```

## 使用方法

### 基本用法

1. 首先，设置硅基流动API密钥：

```python
import os
os.environ["SILICONFLOW_API_KEY"] = "你的API密钥"
```

或者在初始化时直接传入：

```python
from silicon_flow_api import SiliconFlowAPI
api = SiliconFlowAPI(api_key="你的API密钥")
```

2. 简单对话：

```python
response = api.simple_chat(
    query="中国大模型行业2025年将会迎来哪些机遇和挑战？",
    temperature=0.7,
    max_tokens=512
)
print(api.extract_response_content(response))
```

### 多轮对话

```python
conversation = [
    {"role": "system", "content": "你是一个专业的AI助手，擅长回答技术问题。"},
    {"role": "user", "content": "什么是大语言模型？"},
    {"role": "assistant", "content": "大语言模型（Large Language Model，简称LLM）是一种基于深度学习的自然语言处理模型..."},
    {"role": "user", "content": "它们有哪些主要应用场景？"}
]
response = api.multi_turn_chat(conversation)
print(api.extract_response_content(response))
```

### 流式输出

```python
def stream_callback(chunk):
    try:
        content = chunk["choices"][0]["delta"]["content"]
        if content:
            print(content, end="", flush=True)
    except (KeyError, IndexError):
        pass

for _ in api.simple_chat(
    query="请简要介绍一下人工智能的发展历程",
    stream=True,
    stream_callback=stream_callback
):
    pass  # 回调函数会处理输出
```

### 函数调用

```python
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
```

### 自定义参数

```python
response = api.chat_completion(
    messages=[{"role": "user", "content": "写一首关于人工智能的短诗"}],
    model="Pro/deepseek-ai/DeepSeek-V3",
    temperature=0.9,  # 高温度，更有创意
    max_tokens=200,
    top_p=0.95,
    top_k=40,
    frequency_penalty=0.7  # 增加多样性
)
print(api.extract_response_content(response))
```

## 完整示例

请参考 `silicon_flow_api_example.py` 文件，其中包含了多个使用示例。

## API参考

### SiliconFlowAPI类

#### 初始化

```python
SiliconFlowAPI(api_key=None, base_url="https://api.siliconflow.cn/v1")
```

- `api_key`: 硅基流动API密钥，如果为None，则尝试从环境变量SILICONFLOW_API_KEY获取
- `base_url`: 硅基流动API的基础URL

#### 方法

- `chat_completion(messages, model="Pro/deepseek-ai/DeepSeek-V3", stream=False, max_tokens=512, stop=None, temperature=0.7, top_p=0.7, top_k=50, frequency_penalty=0.5, n=1, response_format=None, tools=None, stream_callback=None)`: 调用硅基流动的聊天完成API
- `simple_chat(query, system_prompt=None, model="Pro/deepseek-ai/DeepSeek-V3", temperature=0.7, max_tokens=512, stream=False, stream_callback=None)`: 简单的聊天接口，只需提供查询内容
- `multi_turn_chat(conversation_history, model="Pro/deepseek-ai/DeepSeek-V3", temperature=0.7, max_tokens=512, stream=False, stream_callback=None)`: 多轮对话接口，提供完整的对话历史
- `function_calling_chat(query, tools, system_prompt=None, model="Pro/deepseek-ai/DeepSeek-V3", temperature=0.7, max_tokens=512)`: 函数调用聊天接口，支持工具使用
- `extract_response_content(response)`: 从API响应中提取内容

## 注意事项

- 请确保已获取有效的硅基流动API密钥
- 流式输出需要提供回调函数来处理实时输出
- 函数调用需要正确定义工具参数
- 不同模型可能支持的参数有所不同，请参考硅基流动API文档

## 许可证

MIT 