import os
import feedparser
import smtplib
import google.generativeai as genai
from email.mime.text import MIMEText


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OUTLOOK_EMAIL = os.getenv("OUTLOOK_EMAIL")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")


genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

RSS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.moneycontrol.com/rss/business.xml"
]

news_text = ""

for feed_url in RSS_FEEDS:

    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:15]:

        title = getattr(entry, "title", "")
        link = getattr(entry, "link", "")

        news_text += f"""
Title: {title}
Link: {link}

"""

prompt = f"""
You are a professional Indian stock market analyst.

Analyze all news and provide:

1. Overall Market Sentiment
2. Market Risk Score (0-100)
3. Top 10 Negative News
4. Top 5 Positive News
5. Sectors At Risk
6. Stocks To Watch
7. Global Events Affecting India
8. Include source links

Focus ONLY on information likely to impact
Indian stock markets today.

News:

{news_text}
"""

response = model.generate_content(prompt)

report = response.text

msg = MIMEText(report, "plain", "utf-8")

msg["Subject"] = "Daily India Market Risk Report"
msg["From"] = OUTLOOK_EMAIL
msg["To"] = RECIPIENT_EMAIL

with smtplib.SMTP("smtp.office365.com", 587) as server:
    server.starttls()

    server.login(
        OUTLOOK_EMAIL,
        OUTLOOK_PASSWORD
    )

    server.send_message(msg)

print("Email sent successfully")
