import requests
from config import SERPAPI_API_KEY

def research_topic(topic, fetch_limit=5):
    """Fetch Google search results using SerpAPI."""
    url = "https://serpapi.com/search.json"
    params = {
        "q": topic,
        "api_key": SERPAPI_API_KEY,
        "num": fetch_limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("organic_results", []):
        results.append({
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "link": item.get("link", "")
        })
    return results
