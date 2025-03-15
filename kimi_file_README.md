# Kimi文件API调用工具

这个项目提供了一个通用的Kimi文件API调用类，可以被其他程序方便地调用。支持上传文件、获取文件内容、基于文件内容进行对话等功能。

## 功能特点

- 文件上传：支持上传PDF、DOC、图片等多种格式文件
- 文件内容获取：自动获取上传文件的文本内容
- 基于文件的对话：使用文件内容作为上下文进行对话
- 灵活的API：支持一站式处理或分步骤操作
- 自定义选项：可自定义系统提示词、模型、温度等参数
- 多轮对话：支持添加额外的消息进行多轮对话

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

1. 首先，设置Moonshot API密钥：

```python
import os
os.environ["MOONSHOT_API_KEY"] = "你的API密钥"
```

或者在初始化时直接传入：

```python
from kimi_file_api import KimiFileAPI
kimi_api = KimiFileAPI(api_key="你的API密钥")
```

2. 一站式处理（上传文件并进行对话）：

```python
response = kimi_api.process_file_and_chat(
    file_path="example.pdf",
    query="请简单介绍这个文件讲了什么"
)
print(response.choices[0].message.content)
```

### 分步骤操作

1. 上传文件：

```python
file_obj = kimi_api.upload_file("example.pdf")
```

2. 获取文件内容：

```python
content = kimi_api.get_file_content(file_obj.id)
```

3. 进行对话：

```python
response = kimi_api.chat_with_file(
    file_content=content,
    query="请总结一下这个文档的主要内容"
)
print(response.choices[0].message.content)
```

### 自定义选项

可以自定义系统提示词、模型、温度等参数：

```python
custom_system_prompt = "你是一位专业的文档分析专家，请用简洁的语言分析文档内容。"
response = kimi_api.process_file_and_chat(
    file_path="example.pdf",
    query="这个文档的创新点是什么？",
    system_prompt=custom_system_prompt,
    model="moonshot-v1-32k",
    temperature=0.2
)
```

### 多轮对话

可以添加额外的消息进行多轮对话：

```python
additional_messages = [
    {"role": "user", "content": "这个文档主要讲了什么？"},
    {"role": "assistant", "content": "这个文档主要介绍了XLNet模型..."},
    {"role": "user", "content": "XLNet与BERT有什么区别？"}
]

response = kimi_api.chat_with_file(
    file_content=content,
    additional_messages=additional_messages
)
```

## 完整示例

请参考 `kimi_file_api_example.py` 文件，其中包含了多个使用示例。

## API参考

### KimiFileAPI类

#### 初始化

```python
KimiFileAPI(api_key=None, base_url="https://api.moonshot.cn/v1")
```

- `api_key`: Moonshot API密钥，如果为None，则尝试从环境变量MOONSHOT_API_KEY获取
- `base_url`: Moonshot API的基础URL

#### 方法

- `upload_file(file_path, purpose="file-extract")`: 上传文件
- `get_file_content(file_id)`: 获取已上传文件的内容
- `chat_with_file(file_id=None, file_content=None, query="", model="moonshot-v1-32k", system_prompt=None, temperature=0.3, max_tokens=None, additional_messages=None)`: 基于文件内容与Kimi进行对话
- `process_file_and_chat(file_path, query, model="moonshot-v1-32k", system_prompt=None, temperature=0.3, max_tokens=None, additional_messages=None)`: 一站式处理：上传文件并基于文件内容进行对话

## 注意事项

- 请确保已获取有效的Moonshot API密钥
- 文件上传大小可能受到API限制，请参考Moonshot API文档
- 对于图片和PDF文件，API提供OCR相关能力

## 许可证

MIT 