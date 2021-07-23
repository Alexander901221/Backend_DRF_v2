from django.core.mail import EmailMessage


class SendEmail:
    """Send letter to email"""
    __from_email = 'alexnovpac@gmail.com'

    def __init__(self, to_email, email_subject, body):
        self.__to_email = to_email
        self.__email_subject = email_subject
        self.__body = body

    def send(self):
        email = EmailMessage(
            subject=self.__email_subject,
            body=self.__body,
            to=[self.__to_email],
            from_email=self.__from_email
        )
        email.send()
