import google.generativeai as genai
from config import gemtopen

model = None
genai_configured = False

def init_gemini():
    global model, genai_configured
    if not gemtopen:
        print("Biến gemtopen chưa có")
    else:
        try:
            genai.configure(api_key=gemtopen)
            model = genai.GenerativeModel('gemini-2.0-flash')
            genai_configured = True
        except Exception as e:
            print(f"Lỗi khi khởi tạo Gemini: {e}")
    return genai_configured, model
