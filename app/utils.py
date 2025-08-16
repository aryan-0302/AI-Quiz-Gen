import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

def validate_quiz_structure(quiz_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate quiz data structure and return validation results"""
    validation_result = {
        "is_valid": True,
        "errors": [],
        "warnings": []
    }
    
    required_fields = ["topic", "difficulty"]
    for field in required_fields:
        if field not in quiz_data:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Missing required field: {field}")
    
    question_types = ["mcq", "true_false", "matching", "fill_blank"]
    existing_types = [qt for qt in question_types if qt in quiz_data]
    
    if not existing_types:
        validation_result["is_valid"] = False
        validation_result["errors"].append("No question types found")
    
    if "mcq" in quiz_data:
        mcq = quiz_data["mcq"]
        if not all(key in mcq for key in ["question", "options", "correct_answer"]):
            validation_result["warnings"].append("MCQ missing required fields")
        elif len(mcq.get("options", [])) != 4:
            validation_result["warnings"].append("MCQ should have exactly 4 options")
    
    if "true_false" in quiz_data:
        tf = quiz_data["true_false"]
        if not all(key in tf for key in ["question", "correct_answer"]):
            validation_result["warnings"].append("True/False question missing required fields")
        elif tf.get("correct_answer") not in ["True", "False"]:
            validation_result["warnings"].append("True/False answer should be 'True' or 'False'")
    
    return validation_result

def calculate_quiz_score(answers: Dict[str, str], quiz_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate quiz score based on user answers"""
    score_result = {
        "total_questions": 0,
        "correct_answers": 0,
        "score_percentage": 0,
        "detailed_results": {},
        "feedback": []
    }
    
    # score mcq
    if "mcq" in quiz_data:
        score_result["total_questions"] += 1
        mcq = quiz_data["mcq"]
        user_answer = answers.get("mcq", "")
        correct_answer = mcq.get("correct_answer", "")
        
        if user_answer.lower() == correct_answer.lower():
            score_result["correct_answers"] += 1
            score_result["detailed_results"]["mcq"] = {"correct": True, "feedback": "Correct!"}
        else:
            score_result["detailed_results"]["mcq"] = {
                "correct": False, 
                "feedback": f"Incorrect. The correct answer is {correct_answer}.",
                "explanation": mcq.get("explanation", "")
            }
    
    # score true/fals
    if "true_false" in quiz_data:
        score_result["total_questions"] += 1
        tf = quiz_data["true_false"]
        user_answer = answers.get("true_false", "")
        correct_answer = tf.get("correct_answer", "")
        
        if user_answer.lower() == correct_answer.lower():
            score_result["correct_answers"] += 1
            score_result["detailed_results"]["true_false"] = {"correct": True, "feedback": "Correct!"}
        else:
            score_result["detailed_results"]["true_false"] = {
                "correct": False, 
                "feedback": f"Incorrect. The correct answer is {correct_answer}.",
                "explanation": tf.get("explanation", "")
            }
    
    # score matching
    if "matching" in quiz_data:
        score_result["total_questions"] += 1
        matching = quiz_data["matching"]
        user_answers = answers.get("matching", {})
        pairs = matching.get("pairs", [])
        
        correct_matches = 0
        total_pairs = len(pairs)
        
        for pair in pairs:
            term = pair.get("term", "")
            if user_answers.get(term) == pair.get("definition", ""):
                correct_matches += 1
        
        if correct_matches == total_pairs:
            score_result["correct_answers"] += 1
            score_result["detailed_results"]["matching"] = {"correct": True, "feedback": "Perfect matching!"}
        else:
            score_result["detailed_results"]["matching"] = {
                "correct": False, 
                "feedback": f"Partially correct. You got {correct_matches}/{total_pairs} matches right.",
                "explanation": matching.get("explanation", "")
            }
    
    if "fill_blank" in quiz_data:
        score_result["total_questions"] += 1
        fill = quiz_data["fill_blank"]
        user_answer = answers.get("fill_blank", "")
        correct_answer = fill.get("correct_answer", "")
        
        if user_answer.lower().strip() == correct_answer.lower().strip():
            score_result["correct_answers"] += 1
            score_result["detailed_results"]["fill_blank"] = {"correct": True, "feedback": "Correct!"}
        else:
            score_result["detailed_results"]["fill_blank"] = {
                "correct": False, 
                "feedback": f"Incorrect. The correct answer is '{correct_answer}'.",
                "explanation": fill.get("explanation", "")
            }
    
    # calculate percentage
    if score_result["total_questions"] > 0:
        score_result["score_percentage"] = (score_result["correct_answers"] / score_result["total_questions"]) * 100
    
    # generate overall feedback
    if score_result["score_percentage"] >= 90:
        score_result["feedback"].append("Excellent! You have a strong understanding of this topic.")
    elif score_result["score_percentage"] >= 70:
        score_result["feedback"].append("Good job! You understand most of the concepts.")
    elif score_result["score_percentage"] >= 50:
        score_result["feedback"].append("Fair performance. Consider reviewing the material.")
    else:
        score_result["feedback"].append("You may need to review this topic more thoroughly.")
    
    return score_result

def generate_quiz_summary(quizzes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary statistics for a batch of quizzes"""
    summary = {
        "total_quizzes": len(quizzes),
        "topics": {},
        "difficulties": {},
        "question_types": {},
        "generation_timestamp": datetime.now().isoformat()
    }
    
    for quiz in quizzes:
        topic = quiz.get("topic", "Unknown")
        summary["topics"][topic] = summary["topics"].get(topic, 0) + 1
        
        difficulty = quiz.get("difficulty", "Unknown")
        summary["difficulties"][difficulty] = summary["difficulties"].get(difficulty, 0) + 1
        
    
        for q_type in ["mcq", "true_false", "matching", "fill_blank"]:
            if q_type in quiz:
                summary["question_types"][q_type] = summary["question_types"].get(q_type, 0) + 1
    
    return summary

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    return sanitized

def create_quiz_package(quizzes: List[Dict[str, Any]], output_dir: str = "quiz_exports") -> str:
    """Create a complete quiz package with multiple export formats"""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    json_filename = os.path.join(output_dir, f"generated_quiz_{timestamp}.json")
    from app.quiz_generator import export_quiz_to_json
    export_quiz_to_json(quizzes, json_filename)
    
    md_filename = os.path.join(output_dir, f"generated_quiz_{timestamp}.md")
    from app.quiz_generator import export_quiz_to_markdown
    export_quiz_to_markdown(quizzes, md_filename)
    
    summary = generate_quiz_summary(quizzes)
    summary_filename = os.path.join(output_dir, f"quiz_summary_{timestamp}.json")
    with open(summary_filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    return output_dir
