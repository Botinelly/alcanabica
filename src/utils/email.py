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

def send_order_email(to_email: str, items: list, link: str, order_code: str):
    smtp_server = os.getenv("EMAIL_HOST")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")
    from_name = os.getenv("EMAIL_FROM")

    subject = f"Resumo do Pedido - Alcanabica - Pedido {order_code}"
    body = f"<h3>Resumo do Pedido {order_code} </h3><ul>"
    for item in items:
        body += f"<li>{item['quantity']}x {item['title']} - R$ {item['unit_price']:.2f} cada</li>"
    body += f"</ul><p><a href='{link}'>Clique aqui para finalizar o pagamento</a></p>"

    message = MIMEMultipart("alternative")
    message["From"] = from_name
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, message.as_string())