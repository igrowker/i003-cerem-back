from django.http import HttpResponse
from django.shortcuts import render
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
from ..models import Event  # Asegúrate de tener este modelo definido

def fetch_events(request):
    try:
        # Autenticación con la API de Google Calendar
        creds = Credentials.from_authorized_user_file('token.json')  # Ruta a tu archivo de token
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Construir el servicio de Google Calendar API
        service = build('calendar', 'v3', credentials=creds)

        # Recuperar eventos del calendario de Google
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indica tiempo UTC
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events_data = events_result.get('items', [])

        # Guardar eventos en la base de datos
        for event_data in events_data:
            start_time = event_data['start'].get('dateTime', event_data['start'].get('date'))
            end_time = event_data['end'].get('dateTime', event_data['end'].get('date'))
            start_time = datetime.datetime.fromisoformat(start_time)
            end_time = datetime.datetime.fromisoformat(end_time)
            Event.objects.create(
                summary=event_data.get('summary', ''),
                start_time=start_time,
                end_time=end_time
            )

        # Recuperar eventos de la base de datos y mostrarlos
        events = Event.objects.all()
        context = {'events': events}
        return render(request, 'calendar_integration/calendar_events.html', context)

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
