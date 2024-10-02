from datetime import timedelta
from ..models import Campana, EstadisticaCampana
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
from google.oauth2 import service_account  # Importa la clase service_account

class CampanaRepository:
    def create(self, nombre, descripcion, usuario, fecha_creacion, nota_keep=None):
        campana = Campana(nombre=nombre, descripcion=descripcion, usuario=usuario, fecha_creacion=fecha_creacion)
        campana.save()

        # Crear evento en Google Calendar
        event = {
            'summary': nombre,
            'description': descripcion,
            'start': {
                'dateTime': fecha_creacion.isoformat(),
                'timeZone': 'America/Argentina/Buenos_Aires'  # Ajusta la zona horaria según sea necesario
            },
            'end': {
                'dateTime': (fecha_creacion + timedelta(days=1)).isoformat(),
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

    def get_credentials(self):
        """
        Obtiene las credenciales de Google Cloud Platform desde un archivo JSON.
        """
        # Ruta al archivo JSON de credenciales (idealmente en una variable de entorno)
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

        if not credentials_path:
            # Manejo de error si la variable de entorno no está definida
            raise ValueError("La variable de entorno 'GOOGLE_APPLICATION_CREDENTIALS' no está definida.")

        # Carga las credenciales utilizando service_account.Credentials
        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/keep']
        )

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