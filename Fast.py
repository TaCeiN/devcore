from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from trans import transcribe_from_file 
from maih import transribed_text_kratko
from DB import first_register, login, restore_password_check_db, restore_password_check_code, restore_password_change_password  
import os 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
async def hello(name: str = "гость"):
    return {"message": f"Привет, {name}!"}

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

    resume = transribed_text_kratko(transcribed_text)

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
    

app.mount("/", StaticFiles(directory="static", html=True), name="static")

