import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from bs4 import BeautifulSoup
from GmailAuth.settings import BASE_DIR

# Path to the downloaded credentials JSON file
credentials_path = '/Users/amutharia/GmailAuth/client_secret_1075859946837-9n64lr7o5s9j4kja2a04qbl7br2ubkbt.apps.googleusercontent.com (1).json'
# Scopes required to access Gmail

def authorize():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    flow = InstalledAppFlow.from_client_secrets_file(os.path.join(BASE_DIR,"client_secret_1075859946837-9n64lr7o5s9j4kja2a04qbl7br2ubkbt.apps.googleusercontent.com (1).json"),SCOPES)
    creds = flow.run_local_server(port=8000)
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        return None