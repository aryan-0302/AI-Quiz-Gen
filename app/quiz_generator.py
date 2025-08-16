import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_quiz_questions(chunk, topic="General", difficulty="Intermediate"):
    """Generate comprehensive quiz questions from text chunk"""
    
    system_prompt = (
        "You are an expert quiz creator and educator. "
        "Based on the provided text, generate a comprehensive quiz with the following question types:\n\n"
        "1. Multiple Choice Question (MCQ) with 4 options\n"
        "2. True/False question\n"
        "3. Matching question (if applicable)\n"
        "4. Fill-in-the-blank question (if applicable)\n\n"
        "Ensure all questions are relevant to the provided content and appropriate for the specified difficulty level.\n"
        "Respond in valid JSON format with the following structure:\n"
        "{\n"
        '  "topic": "specific topic from the content",\n'
        '  "difficulty": "Beginner/Intermediate/Expert",\n'
        '  "mcq": {\n'
        '    "question": "question text",\n'
        '    "options": ["option a", "option b", "option c", "option d"],\n'
        '    "correct_answer": "option letter (a/b/c/d)",\n'
        '    "explanation": "brief explanation of the correct answer"\n'
        '  },\n'
        '  "true_false": {\n'
        '    "question": "question text",\n'
        '    "correct_answer": "True/False",\n'
        '    "explanation": "brief explanation"\n'
        '  },\n'
        '  "matching": {\n'
        '    "question": "matching instruction",\n'
        '    "pairs": [{"term": "term1", "definition": "definition1"}, ...],\n'
        '    "explanation": "brief explanation"\n'
        '  },\n'
        '  "fill_blank": {\n'
        '    "question": "question with ___ for blank",\n'
        '    "correct_answer": "correct answer",\n'
        '    "explanation": "brief explanation"\n'
        '  }\n'
        "}"
    )

    user_prompt = f"""Text Chunk:
{chunk}

Topic: {topic}
Difficulty: {difficulty}

Generate a comprehensive quiz based on this content. Focus on practical knowledge that would be useful for learners."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        quiz_content = response["choices"][0]["message"]["content"]
        
        try:
            quiz_data = json.loads(quiz_content)
            return quiz_data
        except json.JSONDecodeError:
            return {"raw_content": quiz_content, "error": "Failed to parse JSON"}
            
    except Exception as e:
        return {"error": f"Failed to generate quiz: {str(e)}"}

def generate_quiz_batch(chunks, topics=None, difficulties=None):
    """Generate quizzes for multiple chunks"""
    if topics is None:
        topics = ["General"] * len(chunks)
    if difficulties is None:
        difficulties = ["Intermediate"] * len(chunks)
    
    quizzes = []
    for i, chunk in enumerate(chunks):
        topic = topics[i] if i < len(topics) else "General"
        difficulty = difficulties[i] if i < len(difficulties) else "Intermediate"
        
        quiz = generate_quiz_questions(chunk, topic, difficulty)
        
        # Check if quiz generation failed
        if quiz and isinstance(quiz, dict) and 'error' not in quiz:
            quiz["chunk_index"] = i
            quiz["chunk_preview"] = chunk[:200] + "..." if len(chunk) > 200 else chunk
            quizzes.append(quiz)
        else:
            # Create a placeholder for failed quiz
            failed_quiz = {
                "chunk_index": i,
                "chunk_preview": chunk[:200] + "..." if len(chunk) > 200 else chunk,
                "topic": topic,
                "difficulty": difficulty,
                "error": "Quiz generation failed for this chunk"
            }
            quizzes.append(failed_quiz)
    
    return quizzes

def export_quiz_to_json(quiz_data, filename="quiz_export.json"):
    """Export quiz data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error exporting quiz: {e}")
        return False

def export_quiz_to_markdown(quiz_data, filename="quiz_export.md"):
    """Export quiz data to Markdown format for LMS integration"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Generated Quiz\n\n")
            
            for i, quiz in enumerate(quiz_data):
                # Skip invalid quizzes
                if not quiz or not isinstance(quiz, dict):
                    f.write(f"## Quiz {i+1} - Invalid Quiz\n\n")
                    f.write("**Error:** This quiz could not be generated properly.\n\n")
                    f.write("---\n\n")
                    continue
                
                f.write(f"## Quiz {i+1}\n\n")
                f.write(f"**Topic:** {quiz.get('topic', 'N/A')}\n")
                f.write(f"**Difficulty:** {quiz.get('difficulty', 'N/A')}\n\n")
                
                if 'mcq' in quiz and isinstance(quiz['mcq'], dict):
                    mcq = quiz['mcq']
                    f.write(f"### 1. Multiple Choice Question\n")
                    f.write(f"{mcq.get('question', 'N/A')}\n\n")
                    options = mcq.get('options', [])
                    if isinstance(options, list):
                        for j, option in enumerate(options):
                            f.write(f"{chr(97+j)}) {option}\n")
                    f.write(f"\n**Correct Answer:** {mcq.get('correct_answer', 'N/A')}\n")
                    f.write(f"**Explanation:** {mcq.get('explanation', 'N/A')}\n\n")
                
                if 'true_false' in quiz and isinstance(quiz['true_false'], dict):
                    tf = quiz['true_false']
                    f.write(f"### 2. True/False Question\n")
                    f.write(f"{tf.get('question', 'N/A')}\n\n")
                    f.write(f"**Correct Answer:** {tf.get('correct_answer', 'N/A')}\n")
                    f.write(f"**Explanation:** {tf.get('explanation', 'N/A')}\n\n")
                
                if 'matching' in quiz and isinstance(quiz['matching'], dict):
                    matching = quiz['matching']
                    f.write(f"### 3. Matching Question\n")
                    f.write(f"{matching.get('question', 'N/A')}\n\n")
                    pairs = matching.get('pairs', [])
                    if isinstance(pairs, list):
                        for pair in pairs:
                            if isinstance(pair, dict):
                                f.write(f"- {pair.get('term', 'N/A')} → {pair.get('definition', 'N/A')}\n")
                    f.write(f"\n**Explanation:** {matching.get('explanation', 'N/A')}\n\n")
                
                if 'fill_blank' in quiz and isinstance(quiz['fill_blank'], dict):
                    fill = quiz['fill_blank']
                    f.write(f"### 4. Fill in the Blank\n")
                    f.write(f"{fill.get('question', 'N/A')}\n\n")
                    f.write(f"**Correct Answer:** {fill.get('correct_answer', 'N/A')}\n")
                    f.write(f"**Explanation:** {fill.get('explanation', 'N/A')}\n\n")
                
                f.write("---\n\n")
        
        return True
    except Exception as e:
        print(f"Error exporting to markdown: {e}")
        return False
