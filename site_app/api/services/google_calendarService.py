from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import logging

class GoogleCalendarService:
    def __init__(self, credentials_path='token.json'):
        self.credentials_path = credentials_path
        self.service = self.get_calendar_service()

    def get_calendar_service(self):
        creds = None
        try:
            creds = Credentials.from_authorized_user_file(self.credentials_path)
        except FileNotFoundError:
            logging.error("Archivo de credenciales no encontrado.")
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logging.error(f"Error al actualizar credenciales: {e}")
            else:
                logging.error("Credenciales inválidas o expiradas. Se requiere autenticación.")
                return None

        return build('calendar', 'v3', credentials=creds)

    def fetch_events(self, calendar_id='primary', max_results=10):
        if not self.service:
            return []
        
        now = datetime.datetime.utcnow().isoformat() + 'Z' 
        try:
            events_result = self.service.events().list(
                calendarId=calendar_id, timeMin=now, maxResults=max_results, 
                singleEvents=True, orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except Exception as e:
            logging.error(f"Error al obtener eventos: {e}")
            return []

    #