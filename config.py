import os
from dotenv import load_dotenv

load_dotenv()
disPoken = os.getenv("disPoken")
gemtopen = os.getenv("gemtopen")

MODMAIL_CHANNEL_NAME = "⌈💬⌋chat-tào-lao"
MEMORY_DIR = "MemoryBank"
MEMORY_LIMIT = 100

os.makedirs(MEMORY_DIR, exist_ok=True)
