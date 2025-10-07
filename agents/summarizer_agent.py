import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def summarizer_agent(state: dict) -> dict:
    """Summarize the research content into LinkedIn-style bullet points."""
    research_text = state.get("research", "")
    if not research_text:
        return {"summary": "No research data provided for summarization."}

    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")

        prompt = f"""
        You are a professional content summarizer for LinkedIn posts.

        Convert the following research data into 6–8 concise, engaging bullet points.
        Each point should:
        - Highlight a key insight, trend, or finding
        - Be written in a LinkedIn-appropriate tone (professional + approachable)
        - Avoid redundancy and unnecessary jargon
        - Use emojis sparingly if they improve readability

        Research data:
        {research_text}

        Output format:
        • Point 1
        • Point 2
        • ...
        """

        response = model.generate_content(prompt)
        summary_text = response.text.strip() if response.text else "No summary generated."

        return {"summary": summary_text}

    except Exception as e:
        return {"summary": f"Summarization failed: {str(e)}"}
