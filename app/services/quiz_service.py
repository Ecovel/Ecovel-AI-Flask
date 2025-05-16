import google.generativeai as genai
import re

def generate_quiz():
    prompt = (
        "Create ONE simple true/false (O/X) quiz about environmental sustainability.\n"
        "Only return one quiz question.\n"
        "Format exactly as below:\n"
        "Question: ...\n"
        "Answer: true/false\n"
        "Explanation: ...\n"
        "Do not include numbering or markdown formatting. No ** or # or any extra formatting.\n"
        "Example:\n"
        "Question: Recycling helps reduce waste.\n"
        "Answer: true\n"
        "Explanation: Recycling reduces landfill waste.\n"
    )

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    
    # Extract response text
    text = response.text.strip()
    print("Gemini raw response:\n", text)

    # Safely parse using regex
    match_q = re.search(r"Question:\s*(.+)", text)
    match_a = re.search(r"Answer:\s*(true|false)", text, re.IGNORECASE)
    match_e = re.search(r"Explanation:\s*(.+)", text)

    data = {}
    if match_q: data["question"] = match_q.group(1).strip()
    if match_a: data["answer"] = match_a.group(1).strip().lower()
    if match_e: data["explanation"] = match_e.group(1).strip()

    return data

def get_today_quiz():
    quiz = generate_quiz()
    print("Quiz content:", quiz)

    if not all(k in quiz for k in ("question", "answer", "explanation")):
        print("Missing keys in Gemini response:", quiz)
        quiz = {
            "question": "Failed to load quiz.",
            "answer": "true",
            "explanation": "Gemini response parsing failed."
        }

    return quiz
