#!/usr/bin/env python3
"""
Demonstration Script for Quiz Generator
This script showcases all the features and capabilities of the system
"""

import os
import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "app"))

from app.file_parser import extract_text_from_file
from app.chunker import chunk_text
from app.quiz_generator import generate_quiz_questions, generate_quiz_batch
from app.utils import validate_quiz_structure, calculate_quiz_score, create_quiz_package

def demo_document_processing():
    """Demonstrate document processing capabilities"""
    print(" Document Processing Demo")
    print("=" * 50)
    
    sample_file = "samples/sample_doc.pdf"
    if not os.path.exists(sample_file):
        print(f" Sample file not found: {sample_file}")
        return False
    
    try:
        print(" Extracting text from PDF...")
        text = extract_text_from_file(sample_file)
        print(f"Extracted {len(text):,} characters")
        
        print("\n Creating text chunks...")
        chunks = chunk_text(text, chunk_size=600, chunk_overlap=100)
        print(f" Created {len(chunks)} chunks")
        
        print("\n Chunk Previews:")
        for i, chunk in enumerate(chunks[:3]):
            preview = chunk[:100].replace('\n', ' ').strip()
            print(f"Chunk {i+1}: {preview}...")
        
        return True, chunks
        
    except Exception as e:
        print(f" Error in document processing: {e}")
        return False, None

def demo_quiz_generation(chunks):
    """Demonstrate quiz generation capabilities"""
    print("\n Quiz Generation Demo")
    print("=" * 50)
    
    try:
        print(" Generating single quiz...")
        quiz = generate_quiz_questions(chunks[0], "General", "Intermediate")
        
        validation = validate_quiz_structure(quiz)
        print(f" Quiz validation: {'Passed' if validation['is_valid'] else 'Failed'}")
        
        if validation['warnings']:
            print(f"  Warnings: {validation['warnings']}")
        
        print(f"\n Quiz Details:")
        print(f"   Topic: {quiz.get('topic', 'N/A')}")
        print(f"   Difficulty: {quiz.get('difficulty', 'N/A')}")
        
        question_types = []
        for q_type in ['mcq', 'true_false', 'matching', 'fill_blank']:
            if q_type in quiz:
                question_types.append(q_type)
        
        print(f"   Question Types: {', '.join(question_types)}")
        
        return True, [quiz]
        
    except Exception as e:
        print(f" Error in quiz generation: {e}")
        return False, None

def demo_batch_processing(chunks):
    """Demonstrate batch processing capabilities"""
    print("\n Batch Processing Demo")
    print("=" * 50)
    
    try:
        print(" Generating quizzes for multiple chunks...")
        quizzes = generate_quiz_batch(chunks[:3]) 
        
        print(f" Generated {len(quizzes)} quizzes")
        
        valid_quizzes = []
        for i, quiz in enumerate(quizzes):
            validation = validate_quiz_structure(quiz)
            if validation["is_valid"]:
                valid_quizzes.append(quiz)
                print(f" Quiz {i+1}: Valid")
            else:
                print(f" Quiz {i+1}: Invalid - {validation['errors']}")
        
        topics = {}
        difficulties = {}
        for quiz in valid_quizzes:
            topic = quiz.get('topic', 'Unknown')
            difficulty = quiz.get('difficulty', 'Unknown')
            topics[topic] = topics.get(topic, 0) + 1
            difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
        
        print(f"\n Quiz Statistics:")
        print(f"   Topics: {topics}")
        print(f"   Difficulties: {difficulties}")
        
        return True, valid_quizzes
        
    except Exception as e:
        print(f" Error in batch processing: {e}")
        return False, None

def demo_quiz_scoring(quizzes):
    """Demonstrate quiz scoring capabilities"""
    print("\n Quiz Scoring Demo")
    print("=" * 50)
    
    if not quizzes:
        print(" No quizzes available for scoring")
        return
    
    try:
        quiz = quizzes[0]
        print(f"Scoring quiz: {quiz.get('topic', 'N/A')}")
        
        simulated_answers = {
            "mcq": "a", 
            "true_false": "True",  
            "matching": {"term1": "definition1"}, 
            "fill_blank": "sample answer" 
        }
        
        score_result = calculate_quiz_score(simulated_answers, quiz)
        
        print(f"\n Score Results:")
        print(f"   Total Questions: {score_result['total_questions']}")
        print(f"   Correct Answers: {score_result['correct_answers']}")
        print(f"   Score Percentage: {score_result['score_percentage']:.1f}%")
        
        print(f"\n Feedback:")
        for feedback in score_result['feedback']:
            print(f"   - {feedback}")
        
        print(f"\n Detailed Results:")
        for q_type, result in score_result['detailed_results'].items():
            status = " Correct" if result['correct'] else " Incorrect"
            print(f"   {q_type}: {status} - {result['feedback']}")
        
    except Exception as e:
        print(f" Error in quiz scoring: {e}")

def demo_export_functionality(quizzes):
    """Demonstrate export capabilities"""
    print("\n Export Functionality Demo")
    print("=" * 50)
    
    if not quizzes:
        print(" No quizzes available for export")
        return
    
    try:
        print(" Creating quiz package...")
        output_dir = create_quiz_package(quizzes, "demo_exports")
        print(f" Quiz package created in: {output_dir}")
        
        print(f"\n Exported Files:")
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"   {file} ({file_size:,} bytes)")
        
        json_file = os.path.join(output_dir, [f for f in os.listdir(output_dir) if f.endswith('.json')][0])
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        print(f"\n JSON Export Preview:")
        print(f"   Total Quizzes: {len(data)}")
        print(f"   First Quiz Topic: {data[0].get('topic', 'N/A')}")
        print(f"   First Quiz Difficulty: {data[0].get('difficulty', 'N/A')}")
        
    except Exception as e:
        print(f" Error in export functionality: {e}")

def main():
    """Run the complete demonstration"""
    print("Quiz Generator - Complete Feature Demonstration")
    print("=" * 70)
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("  Warning: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY=your_api_key_here")
        print("   Some features may not work without the API key\n")
    
    success, chunks = demo_document_processing()
    if not success:
        print(" Document processing failed. Stopping demonstration.")
        return
    
    success, single_quiz = demo_quiz_generation(chunks)
    if not success:
        print(" Single quiz generation failed. Stopping demonstration.")
        return
    
    success, batch_quizzes = demo_batch_processing(chunks)
    if not success:
        print("Batch processing failed. Stopping demonstration.")
        return
    
    demo_quiz_scoring(batch_quizzes)
    demo_export_functionality(batch_quizzes)
    
    print("\n Demonstration completed successfully!")
    print("Check the 'demo_exports' directory for generated quiz files.")
    print("\n Key Features Demonstrated:")
    print("   Multi-format document processing")
    print("   Intelligent text chunking")
    print("   AI-powered quiz generation")
    print("   Multiple question types")
    print("   Quiz validation and scoring")
    print("   Batch processing")
    print("   Multiple export formats")
    print("   Professional quiz packages")

if __name__ == "__main__":
    main()
