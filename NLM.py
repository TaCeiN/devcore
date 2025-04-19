import google.generativeai as genai
import os
API_KEY = "AIzaSyDMFOcxPS0mkw_uM5QEZV1jE8-dXVlKFkg"
genai.configure(api_key=API_KEY)


# Настройка прокси
proxies = {
    "http": "http://FJnRFN:o3wguh@94.131.54.28:9058/",
    "https": "http://FJnRFN:o3wguh@94.131.54.28:9058/",
}
os.environ['HTTP_PROXY'] = proxies['http']
os.environ['HTTPS_PROXY'] = proxies['https']


def nlm_process(transcribed_text):
    # Инициализация модели
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

    # Пример запроса
    prompt = f"Я даю тебе текст, ты должен его обработать и сказать, что там происходит. Вот текст: {transcribed_text}"

    try:
        # Генерация ответа
        response = model.generate_content(prompt)
        print("Ответ модели:")
        return response.text

    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")