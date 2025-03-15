# 火山引擎API调用工具

这个项目提供了一个通用的火山引擎API调用类，可以被其他程序方便地调用。支持模型对话、参数自定义、流式输出等功能。

## 功能特点

- 简单对话：快速进行单轮对话
- 多轮对话：支持完整的对话历史
- 流式输出：实时获取模型生成内容
- 参数自定义：灵活配置模型参数
- 错误处理：完善的异常处理机制

## 安装

### 前提条件

- Python 3.7+
- OpenAI Python 客户端库

### 安装依赖

```bash
pip install openai
```

## 使用方法

### 基本用法

1. 首先，设置火山引擎API密钥：

```python
import os
os.environ["VOLCANO_API_KEY"] = "你的API密钥"
```

或者在初始化时直接传入：

```python
from volcano_engine_api import VolcanoEngineAPI
api = VolcanoEngineAPI(api_key="你的API密钥")
```

2. 简单对话：

```python
response = api.simple_chat(
    query="请介绍一下火山引擎的主要功能",
    system_prompt="你是一位专业的技术顾问"
)
print(api.extract_response_content(response))
```

### 多轮对话

```python
conversation = [
    {"role": "system", "content": "你是一位专业的科学顾问，擅长解释科学概念"},
    {"role": "user", "content": "什么是量子计算？"},
    {"role": "assistant", "content": "量子计算是一种利用量子力学现象进行计算的技术..."},
    {"role": "user", "content": "量子计算机与传统计算机相比有什么优势？"}
]
response = api.multi_turn_chat(conversation)
print(api.extract_response_content(response))
```

### 流式输出

```python
def stream_callback(content):
    print(content, end="", flush=True)

stream = api.simple_chat(
    query="请简要介绍一下深度学习的基本原理",
    system_prompt="你是一位AI研究专家",
    stream=True,
    stream_callback=stream_callback
)

# 消耗生成器
for _ in stream:
    pass
```

### 自定义参数

```python
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
print(api.extract_response_content(response))
```

## 完整示例

请参考 `volcano_engine_api_example.py` 文件，其中包含了多个使用示例。

## API参考

### VolcanoEngineAPI类

#### 初始化

```python
VolcanoEngineAPI(api_key=None, base_url="https://ark.cn-beijing.volces.com/api/v3")
```

- `api_key`: 火山引擎API密钥，如果为None，则尝试从环境变量VOLCANO_API_KEY获取
- `base_url`: 火山引擎API的基础URL

#### 方法

- `chat_completion(messages, model="deepseek-r1-250120", stream=False, temperature=None, max_tokens=None, top_p=None, frequency_penalty=None, presence_penalty=None, stop=None, stream_callback=None)`: 调用火山引擎的聊天完成API
- `simple_chat(query, system_prompt="你是人工智能助手", model="deepseek-r1-250120", stream=False, temperature=None, max_tokens=None, stream_callback=None)`: 简单的聊天接口，只需提供查询内容
- `multi_turn_chat(conversation_history, model="deepseek-r1-250120", stream=False, temperature=None, max_tokens=None, stream_callback=None)`: 多轮对话接口，提供完整的对话历史
- `extract_response_content(response)`: 从API响应中提取内容
- `extract_streaming_content(stream)`: 从流式响应中提取完整内容

## 注意事项

- 请确保已获取有效的火山引擎API密钥
- 火山引擎API使用OpenAI兼容接口，因此可以使用OpenAI Python客户端库进行调用
- 不同模型可能支持的参数有所不同，请参考火山引擎API文档
- 流式输出需要提供回调函数来处理实时输出

## 许可证

MIT 