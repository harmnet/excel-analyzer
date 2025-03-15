# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-45486734879545b5b2b6f58b275ff320", base_url="https://api.deepseek.com/v1")

response = client.chat.completions.create(
    model='deepseek-reasoner',
    # model='deepseek-chat',
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)