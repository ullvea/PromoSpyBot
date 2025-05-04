from app.config import APIKEY_AI

# https://openrouter.ai/deepseek/deepseek-chat/api

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=APIKEY_AI,
)

completion = client.chat.completions.create( # Делаем запрос на создание
  model="deepseek/deepseek-chat", # через модель
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?" # content=вопрос
    }
  ]
)
print(completion)