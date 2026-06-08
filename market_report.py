import os
import feedparser
import smtplib

from email.mime.text import MIMEText
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OUTLOOK_EMAIL = os.getenv("OUTLOOK_EMAIL")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

client = OpenAI(api_key=OPENAI_API_KEY)

RSS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.moneycontrol.com/rss/business.xml",
    "https://feeds.reuters.com/reuters/businessNews"
]

news_text = ""

for feed_url in RSS_FEEDS:

    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:10]:

        title = getattr(entry, "title", "")
        link = getattr(entry, "link", "")

        news_text += f"""
Title: {title}
Link: {link}

"""

prompt = f"""
You are a professional Indian stock market analyst.

Read all the news.

Return ONLY:

1. Overall Market Sentiment
2. Market Risk Score (0-100)
3. Top 10 Negative News
4. Top 5 Positive News
5. Sectors At Risk
6. Stocks To Watch
7. Important Global Events
8. Include source links

Focus ONLY on information that may impact
Indian stock markets today.

News:

{news_text}
"""

response = client.responses.create(
    model="gpt-5",
    input=prompt
)

report = response.output_text

msg = MIMEText(report)

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
