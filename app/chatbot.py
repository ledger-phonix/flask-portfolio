import os
from google import genai
from google.genai import types

# 1. Initialize the client (It automatically picks up the GEMINI_API_KEY environment variable)
client = genai.Client()

def get_bot_response(user_question):
    # 2. Read your bio.txt file safely
    try:
        with open("app/static/bio.txt", "r", encoding="utf-8") as file:
            context_data = file.read()
    except FileNotFoundError:
        return "System Error: Missing profile database."

    # 3. Create strict rules forcing Gemini to ONLY talk about your bio.txt
    system_instruction = (
        "You are Talha's personal AI portfolio helper. "
        "You must ONLY answer questions based on the provided context document below. "
        "If the user asks an irrelevant question or anything outside of Talha's skills, "
        "projects, or education, politely answer: 'I am only trained to answer questions about Talha's portfolio.' "
        "Keep responses brief, conversational, and direct.\n\n"
        f"CONTEXT DOCUMENT:\n{context_data}"
    )

    try:
        # 4. Request a response from the fast, free gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_question,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3 # Low temperature makes the AI strict and factual
            )
        )
        return response.text
    except Exception as e:
        return f"Sorry, I am having trouble connecting right now."