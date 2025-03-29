import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

def send_email(to_email: str, subject: str, body):
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("EMAIL_HOST")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    from_name = os.getenv("EMAIL_FROM")

    subject = subject
    body = f"O código de acesso para o email ({to_email}) foi solicitado no sistema da Alcanabica. \n {body} \n Se não foi você que solicitou esse acesso, favor desconsiderar. \n Não responda esse e-mail."

    message = MIMEMultipart()
    message["From"] = from_name
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(from_email, from_password)
        server.send_message(message)
