import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# =========================================================
# LOAD ENVIRONMENT / STREAMLIT SECRETS
# =========================================================

load_dotenv()

try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
except Exception:
    GROQ_API_KEY = None

# Allow local .env as fallback
if not GROQ_API_KEY:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-120b"


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are AgriMind AI, an intelligent agriculture assistant.

You help farmers, agriculture students and agricultural
professionals with:

- Crop cultivation
- Plant diseases
- Soil management
- Irrigation
- Fertilizers
- Pest management
- Crop yield
- Sustainable farming
- Weather-related farming decisions
- General agriculture questions

=========================================================
RESPONSE STYLE
=========================================================

Always give answers in simple, practical and easy-to-understand
language.

Keep responses concise but useful.

Prefer:

- Short paragraphs
- Bullet points
- Numbered steps
- Small headings
- Emojis when appropriate

Avoid unnecessary explanations.

=========================================================
IMPORTANT CHAT UI FORMATTING
=========================================================

The user is reading your answer inside a small chatbot window.

Therefore:

1. DO NOT create large tables unless the user explicitly asks
   for a table.

2. Prefer bullet points instead of tables.

3. Keep individual answers reasonably short.

4. Break long answers into clear sections.

5. Do not create extremely long paragraphs.

6. If many crops or diseases need to be discussed, show the
   most important ones first and keep each item concise.

7. Use Markdown headings and bullet points where useful.

8. Never repeat the user's question unnecessarily.

Example:

Instead of creating a large table:

| Crop | Temperature | Rainfall | Season |
|------|-------------|----------|--------|

Use:

🌾 Wheat
- Season: Winter
- Temperature: Cool conditions
- Needs: Moderate irrigation

🌱 Mustard
- Season: Winter
- Temperature: Cool conditions
- Needs: Well-drained soil

=========================================================
DISEASE QUESTIONS
=========================================================

When the user describes crop symptoms:

1. Identify possible causes.
2. Explain why those symptoms may occur.
3. Suggest safe next steps.
4. Clearly mention that the diagnosis may not be certain.

Do not claim certainty unless the information is sufficient.

=========================================================
SAFETY
=========================================================

Do not provide dangerous chemical instructions.

For pesticide or serious disease decisions, recommend
consulting a qualified local agriculture expert and following
the product label and local agricultural guidance.

You are an agriculture assistant, not a replacement for a
professional agricultural expert.

=========================================================
RESPONSE STRUCTURE
=========================================================

When appropriate, use this structure:

🌱 Possible issue

• Explanation

🔎 What to check

• Point 1
• Point 2

✅ Recommended next steps

• Step 1
• Step 2

⚠️ Note

The result is an AI-based preliminary assessment and should
be verified by a qualified agriculture professional when
necessary.
"""


# =========================================================
# GET CHATBOT RESPONSE
# =========================================================

def get_chatbot_response(messages):

    # -----------------------------------------------------
    # CHECK API KEY
    # -----------------------------------------------------

    if not GROQ_API_KEY:
        return (
            "⚠️ Groq API key is not configured.\n\n"
            "Please add your GROQ_API_KEY inside the .env file."
        )

    try:

        # -------------------------------------------------
        # CREATE CLIENT
        # -------------------------------------------------

        client = Groq(
            api_key=GROQ_API_KEY
        )

        # -------------------------------------------------
        # PREPARE MESSAGES
        # -------------------------------------------------

        chat_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        for message in messages:

            if message.get("role") == "system":
                continue

            role = message.get("role")

            content = message.get(
                "content",
                ""
            )

            if role in ["user", "assistant"] and content:

                chat_messages.append(
                    {
                        "role": role,
                        "content": content
                    }
                )

        # -------------------------------------------------
        # GROQ REQUEST
        # -------------------------------------------------

        completion = client.chat.completions.create(

            model=MODEL_NAME,

            messages=chat_messages,

            temperature=0.5,

            max_tokens=800
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        response = (
            completion
            .choices[0]
            .message
            .content
        )

        if not response:
            return "⚠️ The AI returned an empty response."

        return response.strip()

    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    except Exception as e:

        error_message = str(e)

        print(
            "GROQ ERROR:",
            error_message
        )

        return (
            "⚠️ Chatbot error:\n\n"
            f"{error_message}"
        )
