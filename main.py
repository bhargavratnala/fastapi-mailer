import dotenv
from fastapi import FastAPI, Form
import smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel
import os

if not dotenv.load_dotenv(".env"):
    raise ValueError("Failed to load environment variables")

class MAILRequest(BaseModel):
    subject: str
    body: str
    mail: str

def get_key(env_var: str):
    return os.getenv(env_var) or dotenv.get_key(".env", env_var)

app = FastAPI()

SENDER_MAIL = get_key("MAIL")
RECEIVER_MAIL = get_key("MAIL")
PASSWORD = get_key("PASSWORD")
MAIL_SERVER = get_key("MAIL_SERVER")
MAIL_PORT = get_key("MAIL_PORT")
REPLY = get_key("REPLY")

if not all([SENDER_MAIL, RECEIVER_MAIL, PASSWORD, MAIL_SERVER, MAIL_PORT, REPLY]):
    raise ValueError("Missing required environment variables")

reply_msg = MIMEText(REPLY)
reply_msg["Subject"] = "Thank you for contacting us!"
reply_msg["From"] = RECEIVER_MAIL

@app.post("/send_mail")
def send_mail(mail: MAILRequest):
    msg = MIMEText(mail.body)
    msg["Subject"] = mail.subject
    msg["From"] = SENDER_MAIL
    msg["To"] = RECEIVER_MAIL

    try:
        with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT) as smtp:
            smtp.login(SENDER_MAIL, PASSWORD)
            smtp.send_message(msg)

            reply_msg["To"] = mail.mail
            smtp.send_message(reply_msg)
        return {"message": "mail sent successfully!"}
    except Exception as e:
        return {"error": f"Error sending mail: {e}"}