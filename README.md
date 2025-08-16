# Quiz Generator from Documents

A comprehensive backend tool that converts any type of document content into interactive quizzes and educational games for training and engagement.

## 🎯 Features

- **Multi-format Document Support**: PDF, DOCX, and Markdown files
- **AI-Powered Quiz Generation**: Multiple question types (MCQ, True/False, Matching, Fill-in-blank)
- **Smart Topic Tagging**: Automatic topic identification from content
- **Difficulty Assessment**: Beginner, Intermediate, Expert classification
- **Multiple Export Formats**: JSON, Markdown, and complete packages for LMS integration
- **Quiz Validation & Scoring**: Built-in quality checks and scoring system

## 🚀 Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

2. **Set up OpenAI API key**
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📖 Usage

```python
from app.file_parser import extract_text_from_file
from app.chunker import chunk_text
from app.quiz_generator import generate_quiz_batch

# Process document and generate quizzes
text = extract_text_from_file("document.pdf")
chunks = chunk_text(text)
quizzes = generate_quiz_batch(chunks)
```

## 🏗️ Architecture

- **File Parser**: Multi-format text extraction
- **Chunker**: Intelligent text segmentation with AI tagging
- **Quiz Generator**: AI-driven question generation
- **Utils**: Validation, scoring, and export functions

## 📊 Output

Generates structured quizzes with:
- Multiple choice questions
- True/False statements  
- Matching exercises
- Fill-in-the-blank questions
- Topic and difficulty tags
- Explanations for answers

## 🎓 Use Cases

- Internal training programs
- Certification exams
- Educational content
- LMS integration
- Client training materials

## 🔧 Configuration

Customize chunk sizes, question types, and export formats through the configuration options in each module.
