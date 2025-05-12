import google.generativeai as genai
from datetime import date
import os

quiz_cache = {}  # { "YYYY-MM-DD": {question, answer, explanation} }

def generate_quiz():
    prompt = (
        "Create a simple true/false (O/X) quiz about environmental sustainability.\n"
        "The question must be under 15 words. Explanation under 15 words.\n"
        "Format:\nQuestion: ...\nAnswer: true/false\nExplanation: ..."
    )
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    lines = response.text.strip().split("\n")
    data = {}
    for line in lines:
        if line.startswith("Question:"):
            data["question"] = line.replace("Question:", "").strip()
        elif line.startswith("Answer:"):
            data["answer"] = line.replace("Answer:", "").strip().lower()
        elif line.startswith("Explanation:"):
            data["explanation"] = line.replace("Explanation:", "").strip()
    return data

def get_today_quiz():
    today = str(date.today())
    if today not in quiz_cache:
        quiz_cache[today] = generate_quiz()
    return quiz_cache[today]

def check_answer(user_answer: str):
    quiz = get_today_quiz()
    is_correct = user_answer.strip().lower() == quiz["answer"]
    return {
        "correct": is_correct,
        "explanation": quiz["explanation"]
    }
