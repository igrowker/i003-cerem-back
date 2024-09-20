from datetime import timedelta
from ..models import Campana, EstadisticaCampana
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import google.auth
from googleapiclient.discovery import build
import os


class CampanaRepository:
    def crear_campana(self, nombre, descripcion, usuario, fecha_inicio, nota_keep=None):
        campana = Campana(nombre=nombre, descripcion=descripcion, usuario=usuario, fecha_inicio=fecha_inicio)
        campana.save()

        # Crear evento en Google Calendar
        event = {
            'summary': nombre,
            'description': descripcion,
            'start': {
                'dateTime': fecha_inicio.isoformat() + 'Z',
                'timeZone': 'America/Argentina/Buenos_Aires'  # Ajusta la zona horaria según sea necesario
            },
            'end': {
                'dateTime': (fecha_inicio + timedelta(days=1)).isoformat() + 'Z',
                'timeZone': 'America/Argentina/Buenos_Aires'
            },
        }
        service_calendar = build('calendar', 'v3', credentials=self.get_credentials())
        event = service_calendar.events().insert(calendarId='primary', body=event).execute()
        campana.google_calendar_event_id = event['id']

        # Crear nota en Google Keep
        if nota_keep:
            note = {
                'title': nota_keep.get('title', nombre),
                'text': nota_keep.get('text', descripcion),
                'labels': nota_keep.get('labels', ['campañas'])
            }
            service_keep = build('keep', 'v1', credentials=self.get_credentials())
            note = service_keep.notes().insert(body=note).execute()
            campana.google_keep_note_id = note['id']

        campana.save()

        return campana
    
# Función para obtener las credenciales de Google Calendar
def get_credentials():
        """
        Obtiene las credenciales de Google Cloud Platform desde un archivo JSON.
        """

        # Ruta al archivo JSON de credenciales
        CREDENTIALS_FILE = '/Users/macbookpro/Downloads/cerem-435413-9997c811627d.json'

        # Comprueba si las credenciales están en el entorno
        if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS_FILE

        creds = None
        if os.path.exists(CREDENTIALS_FILE):
            creds = Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/calendar',
                                        'https://www.googleapis.com/auth/keep','https://www.googleapis.com/auth/keep'])

        return creds

def obtener_campanas(self, usuario=None, **kwargs):
        query = Campana.objects.all()
        if usuario:
            query = query.filter(usuario=usuario)
        return query.filter(**kwargs)

def obtener_campana_por_id(self, campana_id):
        try:
            return Campana.objects.get(pk=campana_id)
        except Campana.DoesNotExist:
            return None
def actualizar_campana(self, campana, **kwargs):
        for atributo, valor in kwargs.items():
            setattr(campana, atributo, valor)
        campana.save()
        return campana

def eliminar_campana(self, campana_id):
        try:
            campana = Campana.objects.get(pk=campana_id)
            campana.delete()
            return True
        except Campana.DoesNotExist:
            return False