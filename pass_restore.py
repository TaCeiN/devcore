import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def send_restore_email(email, code):
    # Настройки почты
    sender_email = "nikolay.krutykh.sss@gmail.com"  # Замените на вашу почту
    sender_password = "ndkxstspvfsvsogl"   # Замените на ваш пароль приложения
    
    # Создаем сообщение
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Восстановление пароля"
    
    # Текст письма
    body = f"Ваш код для восстановления пароля: {code}"
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Подключаемся к серверу Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        # Входим в аккаунт
        server.login(sender_email, sender_password)
        
        # Отправляем письмо
        text = message.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        return False

