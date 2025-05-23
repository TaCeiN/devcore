import aiosqlite
import random
from pass_restore import send_restore_email
from datetime import datetime, timedelta
import base64


async def first_register(email, password):
    # Подключаемся к базе данных
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT email FROM Register WHERE email = ?', (email,))
            result = await cursor.fetchall()
            if result:
                print("Запись найдена:", result[0][0], password)
                return False
            else:
                print("Запись не найдена.", email, password)
                await cursor.execute('INSERT INTO Register (email, password) VALUES (?, ?)', (email, password))
                await conn.commit()
                return True


async def login(email, password):
    # Подключаемся к базе данных
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT email FROM Register WHERE email = ? AND password = ?', (email, password))
            result = await cursor.fetchall()  # Получаем все результаты

            print(result, password)
            if result:
                print("Запись найдена:", result[0][0], password)
                return True
            else:
                print("Запись не найдена.", email, password)
                return False
            
async def restore_password_check_db(email):
    # Подключаемся к базе данных
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT email FROM Register WHERE email = ?', (email,))
            result = await cursor.fetchall()
            if result:
                # Генерируем код восстановления
                email_restore_code = random.randint(100000, 999999)
                
                # Сохраняем код в базе данных
                await cursor.execute(
                    'UPDATE Register SET restore_code = ?, restore_code_created_at = ? WHERE email = ?',
                    (email_restore_code, datetime.now(), email)
                )
                await conn.commit()

                # Отправляем код на почту
                await send_restore_email(email, email_restore_code)
                return True
            else:
                return False
            

async def restore_password_check_code(email, email_restore_code_user):
    # Подключаемся к базе данных
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            # Получаем сохраненный код и время его создания
            await cursor.execute(
                'SELECT restore_code, restore_code_created_at FROM Register WHERE email = ?',
                (email,)
            )
            result = await cursor.fetchone()
            print("1")
            if not result:
                return False

            stored_code, created_at = result
            print("2", stored_code, email_restore_code_user)
            # Проверяем, что код совпадает
            if str(stored_code).strip() != str(email_restore_code_user).strip():
                print("6")
                return False
            print("3")
            # Проверяем, что код создан менее часа назад
            if datetime.now() - datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f') > timedelta(hours=1):
                return False
            print("4")
            return True
    

async def restore_password_change_password(email, password):
    # Подключаемся к базе данных
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('UPDATE Register SET password = ? WHERE email = ?', (password, email))
            await conn.commit()
            return True
        
async def save_first_upload(email, file_name):
    # Читаем содержимое template.bpmn
    with open('template.bpmn', 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            # Сохраняем данные в таблицу Upload
            await cursor.execute('INSERT INTO Upload (file_name, email, content) VALUES (?, ?, ?)', (file_name, email, template_content))
            await conn.commit()
            return True


async def get_upload_file(email, filename):
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT content, file_name FROM Upload WHERE email = ? AND file_name = ?', (email, filename))
            result = await cursor.fetchall()
            # Возвращаем содержимое файла и имя файла без кодировки
            return [(file_name, content) for content, file_name in result]
        
async def update_reasoning_in_db(email, filename, reasoning):
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                'UPDATE Upload SET content = ? WHERE email = ? AND file_name = ?',
                (reasoning, email, filename)
            )
            await conn.commit()        

async def get_all_files_by_email(email):
    async with aiosqlite.connect('DataBase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT file_name FROM Upload WHERE email = ?', (email,))
            result = await cursor.fetchall()
            return [row[0] for row in result]

