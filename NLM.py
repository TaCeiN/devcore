import google.generativeai as genai
import os
import xml.dom.minidom 
import re

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
    prompt = f"""Ты — пунктуационный корректор. На вход ты получаешь текст, полученный из голосовой транскрибации. Этот текст:

написан слитно, без запятых и точек,

может содержать разговорные и неполные конструкции,

должен быть сохранён без изменений слов, без перефразирования.

Твоя задача — расставить только знаки препинания: точки, запятые, двоеточия, тире, кавычки и т.п., где это необходимо для понимания.
Не добавляй или не изменяй слова. Не структурируй текст абзацами. Просто поставь знаки препинания в нужных местах.

Пример входа:
после получения заявки я открываю письмо затем проверяю вложения если все в порядке продолжаю
Пример выхода:
После получения заявки я открываю письмо, затем проверяю вложения. Если всё в порядке — продолжаю.

 Вот текст: {transcribed_text}"""

    try:
        # Генерация ответа
        response = model.generate_content(prompt)
        print("Ответ модели:")
        return response.text

    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")


import re
import xml.dom.minidom
import google.generativeai as genai

def process_content(content, text):
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

    system_prompt = """Adhere to Correct BPMN Tag Syntax:
When working with BPMN diagrams, always strictly follow the tag format as defined in the BPMN 2.0 specification. Errors in tag names, such as BNPNLabel instead of BPMNLabel or other typos, can lead to parsing errors and make the file invalid. Always use the correct tag names:
bpmndi:BPMNLabel
bpmndi:BPMNShape
bpmndi:BPMNEdge
etc.

Ensure Correct Spelling of "BPMN":
Always verify that the term "BPMN" is written exactly as "BPMN" — in that exact order and casing. Any deviation is invalid. Pay special attention to frequent and subtle typos including (but not limited to):

BPNM

BMPN

BNPM

BPM

BP

BMN

BNM

BMMN

BPMNN

BBPMN

BPMM

BPMX

BPRMN

BPMRN

All such variants must be identified and replaced with the correct "BPMN" spelling. When reviewing or generating text, perform thorough visual and automated checks (using regex or keyword validation) to ensure the strict correctness of this term across all tags and values.

Additionally, ensure that all BPMN elements such as tasks, events, gateways, and sequence flows have clear and meaningful names. Use Russian for all diagram labels and descriptions to provide full localization for Russian-speaking users. Maintain semantic clarity and business logic consistency when naming and structuring diagram elements.

When generating or editing diagrams, always ensure:

All labels (bpmndi:BPMNLabel) are in Russian.

Activity and gateway names reflect business context clearly.

Event names are concise but expressive.

Output must remain valid BPMN XML and maintain full compatibility with BPMN 2.0 tools.
"""

    prompt = f"""{system_prompt}\n\n{text}. Вот тебе BPMN файл: {content}. Ответ должен быть в формате Ответ пользователю: <ответ> , Ответ нейросети: <чистый xml код>"""

    try:
        response = model.generate_content(prompt)
        full_text = response.text

        user_response_start = full_text.find("Ответ пользователю:")
        xml_start = full_text.find("Ответ нейросети:")

        if user_response_start != -1:
            user_response = full_text[user_response_start + len("Ответ пользователю:"):xml_start].strip()
        else:
            user_response = "No user response found."

        if xml_start != -1:
            xml_raw = full_text[xml_start + len("Ответ нейросети:"):].strip()
            xml_clean = re.sub(r"^```xml\s*|```$", "", xml_raw).strip()

            # 1. Автозамена всех некорректных написаний "BPMN"
            bpmn_typos = [
                r'\bBPNM\b', r'\bBMPN\b', r'\bBNPM\b', r'\bBPM\b', r'\bBP\b',
                r'\bBMN\b', r'\bBNM\b', r'\bBMMN\b', r'\bBPMNN\b', r'\bBBPMN\b',
                r'\bBPMM\b', r'\bBPMX\b', r'\bBPRMN\b', r'\bBPMRN\b'
            ]
            for typo in bpmn_typos:
                xml_clean = re.sub(typo, 'BPMN', xml_clean, flags=re.IGNORECASE)

            # 2. Автозамена ошибочных тегов
            tag_corrections = {
                "bpmndi:BNShape": "bpmndi:BPMNShape",
                "bpmndi:BNPNLabel": "bpmndi:BPMNLabel",
                "bpmndi:BPMNNLabel": "bpmndi:BPMNLabel",
                "bpmndi:BPMMShape": "bpmndi:BPMNShape",
                "bpmndi:BPMMEdge": "bpmndi:BPMNEdge",
                "bpmndi:BNPNEdge": "bpmndi:BPMNEdge",
                "bpmndi:BPMNShapee": "bpmndi:BPMNShape",
                "bpmndi:BNPMLabel": "bpmndi:BPMNLabel"
            }
            for wrong_tag, correct_tag in tag_corrections.items():
                xml_clean = xml_clean.replace(f"<{wrong_tag}", f"<{correct_tag}")
                xml_clean = xml_clean.replace(f"</{wrong_tag}>", f"</{correct_tag}>")

            # 3. Финальная проверка и форматирование
            try:
                dom = xml.dom.minidom.parseString(xml_clean)
                xml_response = dom.toprettyxml(indent="  ")
            except Exception:
                xml_response = xml_clean

            # 4. Отметим пользователю, что были автозамены
            user_response += "\n✅ В файле автоматически исправлены ошибки в написании 'BPMN' и неверные теги. Проверь результат на всякий случай."

        else:
            xml_response = "No XML response found."

        return user_response, xml_response

    except Exception as e:
        return f"Error: {e}", None