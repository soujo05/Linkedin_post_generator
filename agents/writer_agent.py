import re
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# --- Helper function to make text bold (Unicode bold letters) ---
def to_bold(text: str) -> str:
    bold_map = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘶𝘃𝘄𝘅𝘆𝘇"
    )
    return text.translate(bold_map)


def writer_agent(state: dict) -> dict:
    """Generate a polished LinkedIn post based on the summarized content, tone, and length."""
    summary = state.get("summary", "")
    tone = state.get("tone", "professional")
    length = state.get("length", "medium")

    if not summary:
        return {"post": "No summary provided for post generation."}

    # Define target word counts
    word_target = {
        "short": 120,
        "medium": 200,
        "long": 300
    }.get(length, 200)

    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")

        prompt = f"""
        You are a seasoned LinkedIn content creator.

        Task:
        Write a {tone} LinkedIn post of about {word_target} words based on the following key points:
        {summary}

        Guidelines:
        - Keep it conversational yet insightful.
        - Use storytelling where appropriate.
        - Include 3–5 relevant emojis naturally (not forced).
        - Add 3–5 relevant hashtags at the end.
        - End with a thought-provoking or engaging question to spark discussion.
        - Avoid repetition, fluff, or exaggerated claims.
        - Maintain flow and readability for professional audiences.
        - Use **bold markdown** for key ideas or phrases.

        Output format:
        [Post content only — no extra commentary]
        """

        response = model.generate_content(prompt)
        post = response.text.strip() if response.text else "No post generated."

        # --- Convert **bold markdown** to Unicode bold ---
        post = re.sub(r"\*\*(.*?)\*\*", lambda m: to_bold(m.group(1)), post)

        return {"post": post}

    except Exception as e:
        return {"post": f"Post generation failed: {str(e)}"}
