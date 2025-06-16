import os
import smtplib

from celery import shared_task
from dotenv import load_dotenv

load_dotenv()


SMTP_SERVER = os.getenv("SMTP_SERVER")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")


@shared_task
def send_welcome_email(user_email):
    try:
        subject = "Hello From Aman Develops"
        body = "This is a test email."
        message = f"Subject: {subject}\n\n{body}"
        with smtplib.SMTP(SMTP_SERVER, 587) as server:
            server.starttls()
            server.login(USER_EMAIL, USER_PASSWORD)
            server.sendmail(USER_EMAIL, user_email, message)
        return f"Email sent to {user_email}"
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        print(error_msg)
        return error_msg
