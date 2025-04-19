import requests
import os
import base64

API_KEY = "AIzaSyDMFOcxPS0mkw_uM5QEZV1jE8-dXVlKFkg"  # Подставь свой API ключ
FILE_PATH = "test.bpmn"

proxies = {
    "http": "http://FJnRFN:o3wguh@94.131.54.28:9058/",
    "https": "http://FJnRFN:o3wguh@94.131.54.28:9058/",
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Читаем XML как обычный текст
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        xml_content = f.read()
else:
    xml_content = "<example><error>Файл не найден</error></example>"

# Формируем текст запроса
prompt_text = f"Вот XML-документ:\n\n{xml_content}\n\n Ты можешь прочитать этот файл?. Ессли да, то обьяссни простыми словами что там происходит, без тегов и подобного. Просто Название процесса->нект процесс"

payload = {
    "contents": [{
        "role": "user",
        "parts": [{"text": prompt_text}]
    }]
}

headers = {
    "Content-Type": "application/json"
}

# Отправляем запрос
try:
    response = requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=15)
    response.raise_for_status()
    data = response.json()

    # Извлекаем текст ответа
    result_text = data["candidates"][0]["content"]["parts"][0]["text"]
    print(result_text)

except requests.exceptions.RequestException as e:
    print("Ошибка при запросе:", e)
except (KeyError, IndexError) as e:
    print("Ошибка обработки ответа:", e)

