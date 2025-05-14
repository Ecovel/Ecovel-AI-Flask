import google.generativeai as genai
from datetime import date
import os

def generate_quiz():
    prompt = (
    "Create a simple true/false (O/X) quiz about environmental sustainability.\n"
    "Question must be under 15 words.\n"
    "Answer must be “true” or “false”.\n"
    "Explanation must be one complete sentence (under 15 words) that starts with the key concept and clearly states the reason.  \n"
    "  e.g., “Deforestation causes loss of wildlife habitats.”\n"
    "Format:\n"
    "Question: ...\n"
    "Answer: true/false\n"
    "Explanation: ...\n"
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
    quiz = generate_quiz()

    # Check if all required keys exist to avoid KeyError
    if not all(k in quiz for k in ("question", "answer", "explanation")):
        print("Missing keys in Gemini response:", quiz)
        quiz = {
            "question": " Failed to load quiz.",
            "answer": "true",
            "explanation": "Gemini response parsing failed."
        }

    return quiz




