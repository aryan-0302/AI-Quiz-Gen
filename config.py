"""
Configuration file for the Quiz Generator
"""

import os
from typing import List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "750"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "100"))

DEFAULT_TOPICS = [
    "GMP", "Device Classification", "Clinical Trials", "Licensing", 
    "Quality Assurance", "General", "Documentation",
    "Risk Management", "Validation", "Audit"
]

DEFAULT_DIFFICULTIES = ["Beginner", "Intermediate", "Expert"]

SUPPORTED_FORMATS = [".pdf", ".docx", ".md", ".markdown"]
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))

DEFAULT_OUTPUT_DIR = os.getenv("DEFAULT_OUTPUT_DIR", "quiz_exports")
EXPORT_FORMATS = ["json", "markdown", "package"]

MIN_QUIZ_QUESTIONS = 2
MAX_QUIZ_QUESTIONS = 5

BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
