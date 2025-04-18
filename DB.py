import aiosqlite
import random
from pass_restore import send_restore_email
from datetime import datetime, timedelta

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
                