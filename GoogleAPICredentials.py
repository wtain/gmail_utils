import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleAPICredentials:

    def __init__(self, scopes, token_file_name = 'token.json', credentials_file_name = 'credentials.json'):
        self.scopes = scopes
        self.token_file_name = token_file_name
        self.credentials_file_name = credentials_file_name
        self.creds = self.get_credentials()

    def get_credentials(self):
        creds = None
        if os.path.exists(self.token_file_name):
            creds = Credentials.from_authorized_user_file(self.token_file_name, self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file_name, self.scopes)
                creds = flow.run_local_server(port=0)
            with open(self.token_file_name, 'w') as token:
                token.write(creds.to_json())
        return creds

    def build_api(self, api_name):
        service = build(api_name, 'v1', credentials=self.creds)
        return service