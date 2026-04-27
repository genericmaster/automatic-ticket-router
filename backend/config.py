import os
OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL_NAME= 'qwen2.5:3b'
STREAM=False
THINK=False
CONFIDENCE_THRESHOLD = 60

ADMINS = os.environ.get("ADMINS", "").split(",")


