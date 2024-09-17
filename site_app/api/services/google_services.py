import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Path al archivo de credenciales
CREDENTIALS_PATH = 'config/credentials/client_secret.json'

# Scopes para Google Calendar y Keep
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    # Agrega otros scopes necesarios
]

def authenticate_google_services():
    creds = None
    token_path = 'token.json'

    # Cargar token si existe
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Si no hay credenciales válidas, iniciar flujo OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardar token para futuras sesiones
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

# Ejemplo de uso para Google Calendar
def get_google_calendar_service():
    creds = authenticate_google_services()
    service = build('calendar', 'v3', credentials=creds)
    return service


# Añade funciones para Google Keep si encuentras un API o servicio adecuado.
