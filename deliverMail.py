import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25 MB


def read_email_details():
    to_emails, bcc_emails, subject, body = [], [], "", []
    try:
        with open('email_details.txt', 'r') as file:
            lines = file.readlines()
            section = None

            for line in lines:
                if line.startswith('Subject:'):
                    section = 'subject'
                    subject = line.replace('Subject: ', '').strip()
                elif line.startswith('Body:'):
                    section = 'body'
                    body.append(line.replace('Body: ', '').strip())
                elif line.startswith('To:'):
                    section = 'to'
                    to_emails = line.replace('To: ', '').strip().split(', ')
                elif line.startswith('Bcc:'):
                    section = 'bcc'
                    bcc_emails = line.replace('Bcc: ', '').strip().split(', ')
                elif section == 'body':
                    body.append(line.strip())
    except FileNotFoundError:
        to_emails, bcc_emails, subject, body = [], [], "", []

    body = "\n".join(body)
    return to_emails, bcc_emails, subject, body


def write_email_details(to_emails, bcc_emails, subject, body):
    with open('email_details.txt', 'w') as file:
        file.write(f"To: {', '.join(to_emails)}\n")
        file.write(f"Bcc: {', '.join(bcc_emails)}\n")
        file.write("\n")
        file.write(f"Subject: {subject}\n")
        file.write("\n")
        file.write(f"Body: {body}\n")


def send_email(attachments):
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')

    to_emails, bcc_emails, subject, body = read_email_details()

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = smtp_user

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)
    msg['Bcc'] = ', '.join(bcc_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    total_attachment_size = 0

    for attachment in attachments:
        file_size = len(attachment.getvalue())
        if total_attachment_size + file_size > MAX_ATTACHMENT_SIZE:
            return f'Attachment size exceeds the maximum limit of {MAX_ATTACHMENT_SIZE / (1024 * 1024)} MB'

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment.name}")
        msg.attach(part)
        total_attachment_size += file_size

    all_recipients = to_emails + bcc_emails

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, all_recipients, msg.as_string())
        return 'Email sent successfully!'
    except Exception as e:
        return f'Failed to send email: {e}'