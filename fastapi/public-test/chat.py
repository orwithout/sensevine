import sys
import openai
import os


# 初始化 OpenAI GPT-3.5 Turbo 模型  在系统中执行：export OPENAI_API_KEY=sk-xxxx…… 以设置 API 密钥
openai.api_key = "sk-xxxx"

# 从命令行参数获取聊天信息
chat_input = " ".join(sys.argv[1:])

# 如果没有提供聊天信息，退出程序
if not chat_input:
    print("请提供聊天信息作为命令行参数。")
    sys.exit(1)

# 发送聊天信息给 GPT-3.5 Turbo
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "你是一位汉语文学大师."},
        {"role": "user", "content": chat_input}
    ]
)

# 获取并打印模型的回复
chat_output = response['choices'][0]['message']['content']
print(f"GPT-3.5 Turbo 回复: {chat_output}")

