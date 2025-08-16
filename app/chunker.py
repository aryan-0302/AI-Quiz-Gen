from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text, chunk_size=750, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "],
    )
    return splitter.split_text(text)



import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def tag_chunk(chunk):
    system_prompt = (
        "You are a content analysis expert. "
        "Given a text chunk from any document, output:\n"
        "1. Topic tag (identify the main subject or theme)\n"
        "2. Difficulty level (Beginner, Intermediate, Expert)"
    )

    user_prompt = f"Text:\n{chunk}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )

    return response["choices"][0]["message"]["content"]
