import docx
import fitz 
import os

def extract_text_from_pdf(file_path):
    """Extract text from PDF files using PyMuPDF"""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from DOCX files"""
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""

def extract_text_from_markdown(file_path):
    """Extract text from Markdown files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading Markdown: {e}")
        return ""

def extract_text_from_file(file_path):
    """Main function to extract text from various file formats"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension in ['.md', '.markdown']:
        return extract_text_from_markdown(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
