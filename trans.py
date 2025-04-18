import whisper
import os

model = whisper.load_model("medium")

def transcribe_from_file(file_path):
    print(f"[*] Начинаю расшифровку файла: {file_path}...")
    
    # Используем file_path напрямую без создания временного файла
    result = model.transcribe(file_path, language="ru")
    transcribed_text = result['text']
    
    return transcribed_text


