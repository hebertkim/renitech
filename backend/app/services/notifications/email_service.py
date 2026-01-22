# app/services/notifications/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:

    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        """
        Envia um e-mail simples via SMTP Gmail.

        Args:
            to_email (str): Destinatário
            subject (str): Relatório Finzia
            body (str): Corpo do e-mail
        """
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_user = "m.hebertsouza@gmail.com"   # troque para um e-mail real
        smtp_pass = "otgp flpp vobe sxvd"   # senha de app Gmail

        # Monta a mensagem
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            print(f"📧 E-mail enviado com sucesso para {to_email}")
        except Exception as e:
            print(f"❌ Falha ao enviar e-mail para {to_email}: {e}")
