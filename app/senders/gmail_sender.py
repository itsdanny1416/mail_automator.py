import base64, os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def send_gmail_html(to_email: str, subject: str, html_content: str) -> None:
    """Send an HTML email using Gmail API."""
    creds = Credentials.from_authorized_user_file(os.environ["GMAIL_CREDENTIALS_PATH"], ["https://www.googleapis.com/auth/gmail.send"])
    service = build("gmail", "v1", credentials=creds)
    
    message = MIMEText(html_content, "html")
    message["to"] = to_email
    message["subject"] = subject
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    message_body = {"raw": raw_message}
    
    service.users().messages().send(userId="me", body={"raw": raw_message}).execute()