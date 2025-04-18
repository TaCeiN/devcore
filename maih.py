import requests
import json
import sys

def transribed_text_kratko(transcribed_text):
  sys.stdout.reconfigure(encoding='utf-8')

  proxies = {
      'http': 'http://FJnRFN:o3wguh@94.131.54.28:9058/',
      'https': 'http://FJnRFN:o3wguh@94.131.54.28:9058/'
  }

  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": "Bearer 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",
      "Content-Type": "application/json",
    },
    data=json.dumps({
      "model": "google/gemini-flash-1.5-8b-exp",
      "messages": [
        {
          "role": "system",
          "content": "Я тебе даю текст, ты должен выделить из него главное и составить краткое резюме. А также еще раз повторить этот текст"
        },
        {
          "role": "user",
          "content": transcribed_text
        }
      ],
    }, ensure_ascii=False),  # Отключаем escape-последовательности для не-ASCII символов
    proxies=proxies
  )

  response_json = response.json()
  # Извлекаем только контент
  content = response_json


  return content

