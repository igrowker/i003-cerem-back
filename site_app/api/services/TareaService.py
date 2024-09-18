from models import Tarea
from repositories import TareaRepository
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

class TareaService:
    def __init__(self, credentials):
        self.credentials = credentials
        self.service_calendar = build('calendar', 'v3', credentials=self.credentials)
        self.service_keep = build('keep', 'v1', credentials=self.credentials)
        self.tarea_repository = TareaRepository()

    def crear_tarea(self, data):
        tarea = self.tarea_repository.create(data)

        # Crear evento en Google Calendar
        event = {
            'summary': tarea.titulo,
            'description': tarea.descripcion,
            'start': {
                'dateTime': tarea.fecha_inicio.isoformat() + 'Z',
                'timeZone': 'America/Los_Angeles'  # Ajusta la zona horaria según sea necesario
            },
            # ... otros detalles
        }
        event = self.service_calendar.events().insert(calendarId='primary', body=event).execute()
        tarea.google_calendar_event_id = event['id']

        # Crear nota en Google Keep
        note = {
            'title': tarea.titulo,
            'text': tarea.descripcion,
            # ... otros detalles
        }
        note = self.service_keep.notes().create(body=note).execute()
        tarea.google_keep_note_id = note['id']

        self.tarea_repository.save(tarea)
        return tarea

    def actualizar_tarea(self, tarea_id, data):
        tarea = self.tarea_repository.get(tarea_id)

        # Actualizar en la base de datos
        self.tarea_repository.update(tarea_id, data)

        # Actualizar en Google Calendar
        event = self.service_calendar.events().get(calendarId='primary', eventId=tarea.google_calendar_event_id).execute()
        event['summary'] = tarea.titulo
        event['description'] = tarea.descripcion
        # ... otros cambios
        updated_event = self.service_calendar.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

        # Actualizar en Google Keep
        # ... (similar a actualizar en Calendar)

    def eliminar_tarea(self, tarea_id):
        tarea = self.tarea_repository.get(tarea_id)

        # Eliminar de la base de datos
        self.tarea_repository.delete(tarea_id)

        # Eliminar de Google Calendar
        self.service_calendar.events().delete(calendarId='primary', eventId=tarea.google_calendar_event_id).execute()

        # Eliminar de Google Keep
        self.service_keep.notes().delete(noteId=tarea.google_keep_note_id).execute()

    def sincronizar(self):
        # Obtener todas las tareas de la base de datos
        tareas = self.tarea_repository.all()

        # Iterar sobre las tareas y comparar con Google Calendar y Google Keep
        # ... (lógica de sincronización)