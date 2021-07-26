from rest_api_backend_va_project.celery import app
from utils.send_letter_on_email.send_letter_on_email import SendEmail

@app.task
def send_letter_to_email(to_email, email_subject, email_body):
    send_letter = SendEmail(to_email, email_subject, email_body)
    send_letter.send()
