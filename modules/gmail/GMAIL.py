from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class GMAIL :
    def __init__(self,sender_email,receiver_email,password) -> None:
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = password
    
    def send_email(self,mail_subject,mail_body):
        # Email configurations
        sender_email = self.sender_email
        receiver_email = self.receiver_email
        password = self.password

        subject = mail_subject
        body = mail_body
        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())