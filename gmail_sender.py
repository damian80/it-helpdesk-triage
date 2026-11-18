import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope — send only
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None
    
    # Load existing token if available
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If no valid credentials, ask user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for next time
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)

def send_email(to_address, subject, body):
    """Send an email via Gmail API."""
    service = get_gmail_service()
    
    message = MIMEText(body)
    message["to"] = to_address
    message["subject"] = subject
    
    # Encode message for Gmail API
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    result = service.users().messages().send(
        userId="me",
        body={"raw": encoded}
    ).execute()
    
    return result["id"]