import google.generativeai as genai
import os

# Настройка API ключа
API_KEY = "AIzaSyDMFOcxPS0mkw_uM5QEZV1jE8-dXVlKFkg"
genai.configure(api_key=API_KEY)

# Настройка прокси
proxies = {
    "http": "http://FJnRFN:o3wguh@94.131.54.28:9058/",
    "https": "http://FJnRFN:o3wguh@94.131.54.28:9058/",
}
os.environ['HTTP_PROXY'] = proxies['http']
os.environ['HTTPS_PROXY'] = proxies['https']

# Инициализация модели
model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')





def generate_bpmn_from_text(transcription, example_bpmn):

    prompt = f"""
    Ты — эксперт по BPMN. У тебя есть пример BPMN-схемы:
    {example_bpmn}
    
    На основе этого примера создай новую BPMN-схему для следующего описания:
    {transcription}
    
    Выведи BPMN-схему в формате XML.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Ошибка при генерации BPMN: {e}")
        return None


def update_bpmn_with_task(existing_bpmn, task_transcription):

    prompt = f"""
    Ты — эксперт по BPMN. У тебя есть существующая BPMN-схема:
    {existing_bpmn}
    
    Добавь или модифицируй элементы в этой схеме на основе следующей задачи:
    {task_transcription}
    
    Выведи обновленную BPMN-схему в формате XML.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Ошибка при обновлении BPMN: {e}")
        return None