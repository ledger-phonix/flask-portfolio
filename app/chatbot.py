import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
# 1. Fetch the environment variable explicitly from the OS layer
api_key = os.environ.get("GEMINI_API_KEY")

# 2. Add a graceful fallback so it doesn't crash your entire server on boot
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable is missing!")
    client = None
else:
    # Pass the key directly into the client initialization constructor
    client = genai.Client(api_key=api_key)


def get_bot_response(user_question):
    # If the client failed to initialize, exit gracefully instead of crashing
    if not client:
        return "Chatbot is currently offline (API configuration missing)."

    try:
        with open("app/static/bio.txt", "r", encoding="utf-8") as file:
            context_data = file.read()
    except FileNotFoundError:
        return "System Error: Missing profile database."

    system_instruction = (
        "You are Talha's personal AI portfolio helper. "
        "You must ONLY answer questions based on the provided context document below. "
        "If the user asks an irrelevant question or anything outside of Talha's skills, "
        "projects, or education, politely answer: 'I am only trained to answer questions about Talha's portfolio.' "
        "Keep responses brief, conversational, and direct.\n\n"
        f"CONTEXT DOCUMENT:\n{context_data}"
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_question,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"Sorry, I am having trouble connecting right now."