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
    prompt = f"Я даю тебе текст, ты должен его обработать и сказать, что там происходит. Вот текст: {transcribed_text}"

    try:
        # Генерация ответа
        response = model.generate_content(prompt)
        print("Ответ модели:")
        return response.text

    except Exception as e:
        print(f"Ошибка при обращении к API: {e}")


def process_content(content, text):
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

    system_prompt = """Adhere to Correct BPMN Tag Syntax:
When working with BPMN diagrams, always strictly follow the tag format as defined in the BPMN 2.0 specification. Errors in tag names, such as BNPNLabel instead of BPMNLabel or other typos, can lead to parsing errors and make the file invalid. Always use the correct tag names:
bpmndi:BPMNLabel
bpmndi:BPMNShape
bpmndi:BPMNEdge
etc.

Ensure Matching Opening and Closing Tags:
Make sure that each opening tag has a corresponding closing tag, and that they match in both name and case. Mismatched tags (e.g., </bpmndi:BNPNLabel> instead of </bpmndi:BPMNLabel>) will result in syntax errors and may corrupt the XML structure.

Avoid Using Non-standard or Erroneous Tags:
Some tags like BNPNLabel or similar do not exist in the BPMN 2.0 specification. Always ensure that you are using only tags defined in the specification (e.g., bpmn:task, bpmn:sequenceFlow, bpmn:startEvent, etc.).

Maintain BPMN Diagram Structure:
Follow the standard structure for BPMN files as outlined in BPMN 2.0. If modifying or adding elements, ensure proper placement of tags and do not disrupt the logical flow of the diagram. Always retain the file's structure and flow, based on the user's request.

Thoroughly Check the Code:
Always verify the generated or modified BPMN files for syntax errors, such as incorrect closing tags, incorrect attributes, or invalid values. You can use BPMN validators or other XML validation tools to check the file integrity.

Provide Output in Clean, Raw XML Format:
The output must be a clean XML document that conforms to all BPMN 2.0 standards. Do not add any extra tags, comments, or formatting like backticks (`) or code blocks. Provide the output in plain XML format, as a pure code snippet without any enclosing syntax highlighting.

Proper XML Formatting:
Always ensure proper formatting of XML documents by maintaining correct indentation of tags and attributes, making the code more readable and easier to analyze. The XML content must adhere to XML specification rules and be easy to modify.

Maximize Task Execution:
You are an expert in BPMN diagram analysis. Your goal is to analyze and modify BPMN files in accordance with the user’s request. Always aim to fulfill the task to the highest extent possible. If you lack the necessary information to fulfill the request, respond with "No information available."

Refine and Improve:
If you believe the task has not been executed well, review and improve the changes. Strive to do better each time.

Adjust if Errors Are Found:
If the user points out errors in your work, correct them immediately and make the necessary improvements.

Follow User Request While Maintaining Structure:
Always modify the file as requested by the user, respecting the previous file structure and adhering to BPMN 2.0 principles as implemented in BPMN.js. Do not add HTML tags or any extraneous modifications that are not part of the BPMN standard.

Ensure Correct Structure for Definitions:
The second line of the file should be:
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" id="Definitions_1" targetNamespace="http://bpmn.io/schema/bpmn">

Be the Best in Your Field:
Always strive to be the best at what you do. Make sure the BPMN files you generate are clean, correct, and well-formed."""

    prompt = f"""{system_prompt}\n\n{text}. Вот тебе BPMN файл: {content}. Ответ должен быть в формате Ответ пользователю: <ответ> , Ответ нейросети: <чистый xml код>"""

    try:
        response = model.generate_content(prompt)
        full_text = response.text

        xml_start = full_text.find("Ответ нейросети:")
        if xml_start == -1:
            return full_text

        xml_raw = full_text[xml_start + len("Ответ нейросети:"):].strip()

        # Убираем обрамление ```xml или ```
        xml_clean = re.sub(r"^```xml\s*|```$", "", xml_raw).strip()

        try:
            dom = xml.dom.minidom.parseString(xml_clean)
            return dom.toprettyxml(indent="  ")
        except Exception:
            return xml_clean

    except Exception as e:
        return f"Error: {e}"