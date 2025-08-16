#!/usr/bin/env python3
"""
Quiz Generator from Documents
A comprehensive tool for generating interactive quizzes from any type of content.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any

sys.path.append(str(Path(__file__).parent / "app"))

from app.file_parser import extract_text_from_file
from app.chunker import chunk_text
from app.quiz_generator import generate_quiz_batch, export_quiz_to_json, export_quiz_to_markdown
from app.utils import validate_quiz_structure, create_quiz_package, generate_quiz_summary

class QuizGenerator:
    """Main class for the Quiz Generator application"""
    
    def __init__(self):
        self.quizzes = []
        self.current_file = None
        self.chunks = []
        
    def process_document(self, file_path: str, chunk_size: int = 750, chunk_overlap: int = 100) -> bool:
        """Process a document and extract text chunks"""
        try:
            print(f"Processing document: {file_path}")
            
            text = extract_text_from_file(file_path)
            if not text:
                print("Failed to extract text from document")
                return False
            
            print(f"Extracted {len(text)} characters of text")
            
            self.chunks = chunk_text(text, chunk_size, chunk_overlap)
            print(f"Created {len(self.chunks)} text chunks")
            
            self.current_file = file_path
            return True
            
        except Exception as e:
            print(f"Error processing document: {e}")
            return False
    
    def generate_quizzes(self, max_chunks: int = None, topics: List[str] = None, difficulties: List[str] = None) -> bool:
        """Generate quizzes from the processed chunks"""
        if not self.chunks:
            print("No chunks available. Please process a document first.")
            return False
        
        if max_chunks:
            chunks_to_process = self.chunks[:max_chunks]
        else:
            chunks_to_process = self.chunks
        
        print(f"Generating quizzes for {len(chunks_to_process)} chunks...")
        
        try:
            self.quizzes = generate_quiz_batch(chunks_to_process, topics, difficulties)
            
            valid_quizzes = []
            for i, quiz in enumerate(self.quizzes):
                validation = validate_quiz_structure(quiz)
                if validation["is_valid"]:
                    valid_quizzes.append(quiz)
                else:
                    print(f"Quiz {i+1} validation warnings: {validation['warnings']}")
            
            self.quizzes = valid_quizzes
            print(f"Successfully generated {len(self.quizzes)} valid quizzes")
            return True
            
        except Exception as e:
            print(f"Error generating quizzes: {e}")
            return False
    
    def display_quiz_preview(self, quiz_index: int = 0):
        """Display a preview of a specific quiz"""
        if not self.quizzes or quiz_index >= len(self.quizzes):
            print("No quizzes available or invalid index")
            return
        
        quiz = self.quizzes[quiz_index]
        print(f"\n Quiz {quiz_index + 1} Preview")
        print("=" * 50)
        print(f"Topic: {quiz.get('topic', 'N/A')}")
        print(f"Difficulty: {quiz.get('difficulty', 'N/A')}")
        print(f"Chunk Preview: {quiz.get('chunk_preview', 'N/A')[:100]}...")
        
        if 'mcq' in quiz:
            mcq = quiz['mcq']
            print(f"\n🔹 Multiple Choice Question:")
            print(f"   {mcq.get('question', 'N/A')}")
            for j, option in enumerate(mcq.get('options', [])):
                print(f"   {chr(97+j)}) {option}")
            print(f"   Correct Answer: {mcq.get('correct_answer', 'N/A')}")
        
        if 'true_false' in quiz:
            tf = quiz['true_false']
            print(f"\n🔹 True/False Question:")
            print(f"   {tf.get('question', 'N/A')}")
            print(f"   Correct Answer: {tf.get('correct_answer', 'N/A')}")
        
        if 'matching' in quiz:
            matching = quiz['matching']
            print(f"\n🔹 Matching Question:")
            print(f"   {matching.get('question', 'N/A')}")
            pairs = matching.get('pairs', [])
            for pair in pairs[:3]: 
                print(f"   - {pair.get('term', 'N/A')} → {pair.get('definition', 'N/A')}")
            if len(pairs) > 3:
                print(f"   ... and {len(pairs) - 3} more pairs")
        
        print("=" * 50)
    
    def export_quizzes(self, output_format: str = "json", output_dir: str = "quiz_exports"):
        """Export quizzes in specified format"""
        if not self.quizzes:
            print("No quizzes to export")
            return False
        
        try:
            if output_format.lower() == "json":
                filename = os.path.join(output_dir, "generated_quizzes.json")
                success = export_quiz_to_json(self.quizzes, filename)
                if success:
                    print(f"Exported quizzes to {filename}")
                    return True
            
            elif output_format.lower() == "markdown":
                filename = os.path.join(output_dir, "generated_quizzes.md")
                success = export_quiz_to_markdown(self.quizzes, filename)
                if success:
                    print(f"Exported quizzes to {filename}")
                    return True
            
            elif output_format.lower() == "package":
                output_path = create_quiz_package(self.quizzes, output_dir)
                print(f"Created quiz package in {output_path}")
                return True
            
            else:
                print(f"Unsupported export format: {output_format}")
                return False
                
        except Exception as e:
            print(f"Error exporting quizzes: {e}")
            return False
    
    def show_summary(self):
        """Display summary of generated quizzes"""
        if not self.quizzes:
            print("No quizzes available")
            return
        
        summary = generate_quiz_summary(self.quizzes)
        
        print("\n Quiz Generation Summary")
        print("=" * 50)
        print(f"Total Quizzes: {summary['total_quizzes']}")
        print(f"Generated: {summary['generation_timestamp']}")
        
        print(f"\n Topics:")
        for topic, count in summary['topics'].items():
            print(f"   {topic}: {count}")
        
        print(f"\n Difficulties:")
        for difficulty, count in summary['difficulties'].items():
            print(f"   {difficulty}: {count}")
        
        print(f"\n Question Types:")
        for q_type, count in summary['question_types'].items():
            print(f"   {q_type}: {count}")
        
        print("=" * 50)

def main():
    """Main application entry point"""
    print("Quiz Generator from Documents")
    
    generator = QuizGenerator()
    
    sample_file = "samples/sample_doc.pdf"
    if not os.path.exists(sample_file):
        print(f" Sample file not found: {sample_file}")
        print("Please ensure you have a sample document in the samples/ directory")
        return
    
    print(f"Using sample document: {sample_file}")
    if not generator.process_document(sample_file):
        print("Failed to process sample document")
        return
    
    print("\n Generating quizzes...")
    if not generator.generate_quizzes(max_chunks=3):
        print("Failed to generate quizzes")
        return
    
    generator.show_summary()
    
    print("\n Preview of first quiz:")
    generator.display_quiz_preview(0)
    
    print("\n Exporting quizzes...")
    generator.export_quizzes("package", "quiz_exports")
    
    print("\n Quiz generation complete!")
    print("Check the 'quiz_exports' directory for your generated quizzes.")

if __name__ == "__main__":
    main()
