# starting the server using following command - "python generate_token.py"
import os
import django
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.conf import settings
from httplib2 import Credentials

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Scopes required for accessing Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None

    # Check if token file exists
    if os.path.exists(settings.GOOGLE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            settings.GOOGLE_TOKEN_FILE)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  
            creds = flow.run_local_server(port=8000)

        # Save the credentials for the next run
        with open(settings.GOOGLE_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

if __name__ == '__main__':
    main()