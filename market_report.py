	
import smtplib
from email.mime.text import MIMEText

EMAIL_USER = "oracle1240@outlook.com"
EMAIL_PASSWORD = "mlhowkpanvnntsyl"
RECIPIENT = "oracle1240@outlook.com"

msg = MIMEText("Text message")
msg["Subject"] = "Daily Market Report"
msg["From"] = EMAIL_USER
msg["To"] = RECIPIENT

with smtplib.SMTP("smtp.office365.com", 587, timeout=30) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.send_message(msg)
