#!/usr/bin/env python3
"""
Example usage of the Quiz Generator
This script demonstrates how to use the API programmatically
"""

import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent / "app"))

from app.file_parser import extract_text_from_file
from app.chunker import chunk_text
from app.quiz_generator import generate_quiz_questions, generate_quiz_batch
from app.utils import validate_quiz_structure, create_quiz_package

def example_basic_usage():
    """Basic example of processing a document and generating quizzes"""
    print("🔍 Example: Basic Usage")
    print("=" * 50)
    
    # Check if sample file exists
    sample_file = "samples/sample_doc.pdf"
    if not os.path.exists(sample_file):
        print(f"Sample file not found: {sample_file}")
        print("Please ensure you have a sample document in the samples/ directory")
        return
    
    try:
        # Step 1: Extract text from document
        print("Step 1: Extracting text from document...")
        text = extract_text_from_file(sample_file)
        print(f" Extracted {len(text)} characters")
        
        print("\n Step 2: Creating text chunks...")
        chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)
        print(f" Created {len(chunks)} chunks")
        
        print("\n Step 3: Generating quiz for first chunk...")
        if chunks:
            quiz = generate_quiz_questions(chunks[0], "General", "Intermediate")
            
            validation = validate_quiz_structure(quiz)
            print(f"Quiz validation: {'Passed' if validation['is_valid'] else 'Failed'}")
            
            if validation['warnings']:
                print(f"  Warnings: {validation['warnings']}")
            
            print("\n Generated Quiz Preview:")
            print(f"Topic: {quiz.get('topic', 'N/A')}")
            print(f"Difficulty: {quiz.get('difficulty', 'N/A')}")
            
            if 'mcq' in quiz:
                mcq = quiz['mcq']
                print(f"\n🔹 MCQ: {mcq.get('question', 'N/A')}")
                for i, option in enumerate(mcq.get('options', [])):
                    print(f"   {chr(97+i)}) {option}")
                print(f"   Answer: {mcq.get('correct_answer', 'N/A')}")
        
        print("\n Basic usage example completed!")
        
    except Exception as e:
        print(f" Error in basic usage example: {e}")

def example_batch_processing():
    """Example of batch processing multiple chunks"""
    print("\n Example: Batch Processing")
    print("=" * 50)
    
    sample_file = "samples/sample_doc.pdf"
    if not os.path.exists(sample_file):
        print(f" Sample file not found: {sample_file}")
        return
    
    try:
        text = extract_text_from_file(sample_file)
        chunks = chunk_text(text, chunk_size=600, chunk_overlap=100)
        
        chunks_to_process = chunks[:2]
        print(f" Processing {len(chunks_to_process)} chunks...")
        
        quizzes = generate_quiz_batch(chunks_to_process)
        print(f" Generated {len(quizzes)} quizzes")
        
        valid_quizzes = []
        for i, quiz in enumerate(quizzes):
            validation = validate_quiz_structure(quiz)
            if validation["is_valid"]:
                valid_quizzes.append(quiz)
                print(f" Quiz {i+1}: Valid")
            else:
                print(f" Quiz {i+1}: Invalid - {validation['errors']}")
        
        # Export quiz package
        if valid_quizzes:
            print(f"\n Exporting {len(valid_quizzes)} valid quizzes...")
            output_dir = create_quiz_package(valid_quizzes, "example_exports")
            print(f" Exported to: {output_dir}")
        
        print("\n Batch processing example completed!")
        
    except Exception as e:
        print(f" Error in batch processing example: {e}")

def example_custom_topics():
    """Example with custom topic and difficulty settings"""
    print("\n Example: Custom Topics and Difficulties")
    print("=" * 50)
    
    sample_file = "samples/sample_doc.pdf"
    if not os.path.exists(sample_file):
        print(f" Sample file not found: {sample_file}")
        return
    
    try:
        text = extract_text_from_file(sample_file)
        chunks = chunk_text(text, chunk_size=700, chunk_overlap=150)
        
        custom_topics = ["General", "Quality Assurance", "Documentation"]
        custom_difficulties = ["Intermediate", "Expert"]
        
        print(f" Using custom topics: {custom_topics}")
        print(f" Using custom difficulties: {custom_difficulties}")
        
        quizzes = generate_quiz_batch(
            chunks[:2], 
            topics=custom_topics,
            difficulties=custom_difficulties
        )
        
        print(f" Generated {len(quizzes)} quizzes with custom settings")
        
        for i, quiz in enumerate(quizzes):
            print(f"Quiz {i+1}: {quiz.get('topic', 'N/A')} - {quiz.get('difficulty', 'N/A')}")
        
        print("\n Custom topics example completed!")
        
    except Exception as e:
        print(f" Error in custom topics example: {e}")

def main():
    """Run all examples"""
    print(" Quiz Generator - Example Usage")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("  Warning: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY=your_api_key_here")
        print("   Some examples may not work without the API key\n")
    
    example_basic_usage()
    example_batch_processing()
    example_custom_topics()
    
    print("\n All examples completed!")
    print("Check the 'example_exports' directory for generated quiz files.")

if __name__ == "__main__":
    main()
