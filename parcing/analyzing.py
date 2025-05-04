from app.config import APIKEY_AI

# https://openrouter.ai/deepseek/deepseek-chat/api
# python -m venv .venv
# .venv\Scripts\activate
# https://github.com/openai/openai-agents-python - аля документация

from openai import OpenAI


def generate_answer(mes):
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=APIKEY_AI,
  )

  completion = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[
      {
        "role": "user",
        "content":"Поменялась ли цена на данный товар? Если да, то в какую сторону? "
                  "Если нет, то дай чёткий ответ НЕТ. Ответь односложно."
      }
    ]
  )
  return completion.choices[0].message.content