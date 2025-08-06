from fastapi import FastAPI
import feedparser
import openai
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")
RSS_FEEDS = [
  "https://news.google.com/rss/search?q=formula+1&hl=en-US&gl=US&ceid=US:en",
  "https://www.motorsport.com/rss/f1/news/",
  "https://www.autosport.com/rss/f1/all.xml",
  "https://www.racingnews365.com/rss",
  "https://www.planetf1.com/feed",
  "https://www.skysports.com/rss/12040"
]

def fetch_f1_news():
    headlines = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for ent in feed.entries[:3]:
            headlines.append(ent.title)
    return headlines[:10]

def summarize_with_gpt(headlines):
    prompt = (
      "Summarize the top 10 trending F1 topics from these headlines:\n\n"
      + "\n".join(f"- {hl}" for hl in headlines)
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7, max_tokens=600
    )
    return resp.choices[0].message['content']

@app.get("/f1-topics")
def endpoint():
    return {"summary": summarize_with_gpt(fetch_f1_news())}
