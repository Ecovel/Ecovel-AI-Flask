import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_quiz():
    prompt = (
        "Create a simple true/false (O/X) quiz about environmental sustainability.\n"
        "The quiz should be short, specific, and not too obvious.\n"
        "Avoid generic statements like 'Water is important' or 'Plastic is bad'.\n"
        "Use basic but factual environmental knowledge that requires a bit of thought.\n"
        "The question must be under 15 words.\n"
        "The explanation must be 1 short sentence only (no more than 15 words).\n"
        "Respond in the following format only:\n"
        "Question: ...\n"
        "Answer: true or false\n"
        "Explanation: ..."
    )

    response = model.generate_content(prompt)
    lines = response.text.strip().split("\n")
    data = {}
    for line in lines:
        if line.startswith("Question:"):
            data["question"] = line.replace("Question:", "").strip()
        elif line.startswith("Answer:"):
            data["answer"] = line.replace("Answer:", "").strip().lower()  # "true" or "false"
        elif line.startswith("Explanation:"):
            data["explanation"] = line.replace("Explanation:", "").strip()
    return data
