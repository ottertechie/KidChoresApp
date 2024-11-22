# email_utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

SENDER_EMAIL = "hughespj1@gmail.com"
RECEIVER_EMAIL = "hughespj1@gmail.com"
PASSWORD = "smnt ffyz xmwe augu"

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"Email with subject '{subject}' sent successfully!\n")
    except Exception as e:
        print(f"Failed to send email. Error: {e}\n")

def send_at_home_email(user_name):
    subject = f"{user_name} is Now at Home"
    body = f"{user_name} has marked themselves as being at home as of {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
    send_email(subject, body)

def send_electronics_email(user_name, timestamp, action, restricted, duration=None, exceeded=False):
    subject = f"Electronics Time {action.capitalize()} for {user_name}"
    body = f"{user_name} has {'started' if action == 'start' else 'ended'} electronics time at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}.\n"
    if restricted:
        body += "Note: Electronics time is restricted to 1 hour due to grades below a C.\n"
    if duration:
        body += f"Total duration: {duration}\n"
    if exceeded:
        body += "Warning: Electronics time exceeded the 1-hour limit.\n"
    send_email(subject, body)

def send_daily_summary(summary_body):
    subject = "Daily Summary"
    send_email(subject, summary_body)
