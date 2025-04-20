from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from trans import transcribe_from_file 
from DB import *
from NLM import *
import os 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/api/audio_transcription")
async def audio(file: UploadFile = File(...)):
    filename = file.filename
    
    # Указываем путь к папке temp в вашем проекте
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)  # Создаем временную директорию, если она не существует
    
    # Сохраняем файл на сервере
    file_location = os.path.join(temp_dir, filename)  # Путь для временного хранения файла
    with open(file_location, "wb") as f:
        f.write(await file.read())  # Читаем содержимое файла и записываем его

    # Выполняем транскрипцию
    transcribed_text = transcribe_from_file(file_location)

    # Удаляем файл после обработки
    os.remove(file_location)

    resume = nlm_process(transcribed_text)

    return {"filename": filename, "transcribed_text": transcribed_text, "resume": resume}


@app.post("/api/register")
async def register(email: str, password: str):
    if await first_register(email, password) == True:
        return {"register": True}
    else:
        return {"register": False}


@app.get("/api/login")
async def alogin(email: str, password: str):
    if await login(email, password) == True:
        return {"login": True}
    else:
        return {"login": False}

@app.get("/api/restore_password_1")
async def restore_password_1(email: str):
    if await restore_password_check_db(email) == True:
        return {"restore_password_1": True}
    else:
        return {"restore_password_1": False}

@app.get("/api/restore_password_2")
async def restore_password_2(email: str, email_restore_code: str):
    if await restore_password_check_code(email, email_restore_code):
        return {"restore_password_2": True}
    else:
        return {"restore_password_2": False}
    
@app.post("/api/restore_password_3")
async def restore_password_3(email: str, password: str):
    if await restore_password_change_password(email, password) == True:
        return {"restore_password_3": True}
    else:
        return {"restore_password_3": False}
    

@app.post("/api/first_upload")
async def first_upload(email: str, filename: str):

    # Сохраняем информацию о загрузке в базу данных
    await save_first_upload(email, filename)

    return {"filename": filename, "message": "File uploaded successfully."}

@app.get("/api/get_file")
async def get_file(email: str, filename: str):
    result = await get_upload_file(email, filename)
    if result:
        return result
    return {"error": "No files found"}


@app.post("/api/process_file")
async def process_file(email: str, filename: str, text: str):
    # Получаем файл из базы данных
    result = await get_upload_file(email, filename)
    if result:
        # Извлекаем имя файла и его содержимое
        file_name, content = result[0]  # Изменено порядок извлечения
        
        # Вызываем вашу функцию нейросети
        user_response, xml_response = process_content(content, text)
        
        if user_response == "No user response found." or xml_response == "No XML response found.":
            return {"filename": file_name, "user_response": "Unable to process content", "xml": ""}
        
        # Обновляем reasoning в базе данных
        await update_reasoning_in_db(email, file_name,xml_response)  # Save user response (if needed)
        
        return {
            "filename": file_name,
            "user_response": user_response,
            "xml": xml_response,
        }
    
    return {"error": "Файл не найден"}


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content="<h1>Ошибка: доступ запрещен</h1>", status_code=403)

