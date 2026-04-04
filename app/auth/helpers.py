import  smtplib
from app.config import Config
from email.message import EmailMessage


def send_email(to_email, link):
    msg = EmailMessage()
    msg.set_content(f"Please verify your email by clicking this link: {link}")
    msg["Subject"] = "Verify your email"
    msg["From"] = "lostnfound7985@gmail.com"
    msg["To"] = to_email

    with smtplib.SMTP_SSL(Config.EMAIL_HOST, Config.EMAIL_PORT) as smtp:
        smtp.login(Config.EMAIL_USERNAME, Config.EMAIL_PASSWORD)
        smtp.send_message(msg)