import google.generativeai as genai
from bs4 import BeautifulSoup
import requests
from utils.searcher import research_topic
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def clean_text_from_url(url: str) -> str:
    """Fetch and clean text from a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return ""

        soup = BeautifulSoup(resp.content, "html.parser")
        for tag in soup(["script", "style", "header", "footer", "nav", "aside", "form"]):
            tag.decompose()

        paragraphs = [p.get_text().strip() for p in soup.find_all("p") if p.get_text().strip()]
        return " ".join(paragraphs)[:3000]
    except Exception:
        return ""

def research_agent(state: dict) -> dict:
    """Research the topic using SerpAPI and summarize with Gemini."""
    topic = state.get("topic", "")
    if not topic:
        return {"research": "No topic provided."}

    try:
        search_results = research_topic(topic, fetch_limit=4)
    except Exception as e:
        return {"research": f"Research failed: {str(e)}"}

    if not search_results:
        return {"research": "No search results found."}

    collected = []
    for r in search_results:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")
        content = clean_text_from_url(link)
        collected.append(f"🔹 {title}\n{snippet}\n{content}")

    combined_text = "\n\n".join(collected[:4])

    model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")

    prompt = f"""
    You are a senior research analyst.
    Analyze the following web information on "{topic}" and extract **6-8 key insights** that are factual, relevant, and recent.
    
    Data:
    {combined_text}

    Present your findings in clear bullet points, suitable for professional writing.
    """

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip() if response.text else "No research summary generated."
    except Exception as e:
        summary = f"Gemini summarization failed: {str(e)}"

    return {"research": summary}

