from rest_framework import viewsets, permissions,status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..services import EstadisticasService,CampanaService,ClienteService
from ..models import Tarea, Campana, Cliente, EstadisticaCampana,Usuario, Event
from ..serializers import TareaSerializer, CampanaSerializer, ClienteSerializer, EstadisticaCampanaSerializer, EventSerializer
from ..repositories import TareasRepository,CampanaRepository,ClienteRepository,EstadisticasRepository
from transformers import pipeline
import csv

#IMPORTS GCALENDAR
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from oauth2_provider.views.generic import ProtectedResourceView
from api.models import Event
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
#
from drf_yasg.utils import swagger_auto_schema

# Swagger Schema Configuration
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Mi API de Gestión de Tareas, Campañas y Clientes",
        default_version='v1',
        description="Documentación de la API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),

        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)

# TareaViewSet with Swagger Documentation
class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    # Inyectamos el repositorio de tareas en el constructor
    def __init__(self, *args, **kwargs):
        self.tareas_repo = TareasRepository()
        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Marcar una tarea como completada",
        operation_description="Marca una tarea existente como completada.",
        responses={200: 'Tarea completada', 404: 'Tarea no encontrada'}
    )
    @action(detail=True, methods=['post'])
    def completar_tarea(self, request, pk=None):
        tarea = self.tareas_repo.obtener_tarea_por_id(pk)
        if tarea:
            tarea.completado = True
            tarea.save()
            return Response({'message': 'Tarea completada'})
        else:
            return Response({'error': 'Tarea no encontrada'}, status=status.HTTP_404_NOT_FOUND)

class CampanaViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

    def create(self, request, *args, **kwargs):
      pass
    
# CampanaCrearViewSet with Swagger Documentation
class CampanaCrearViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated]
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer
    def create(self, request, *args, **kwargs):
    @swagger_auto_schema(
        operation_summary="Crear una nueva campaña",
        operation_description="Crea una nueva campaña con contenido generado automáticamente.",
        request_body=CampanaSerializer,
        responses={201: 'Campaña creada', 400: 'Error al crear la campaña'}
    )
    def post(self, request):

        campana_service = CampanaService()
        data = request.data
        try:
            serializer = campana_service.crear_campana_con_contenido(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)       
     

# CampanaEstadisticaViewSet with Swagger Documentation
class CampanaEstadisticaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

    # Inyectamos los repositorios de campañas y estadísticas en el constructor
    def __init__(self, *args, **kwargs):
        self.campanas_repo = CampanaRepository()
        self.estadisticas_repo = EstadisticasRepository()
        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Obtener estadísticas de una campaña",
        operation_description="Obtiene las estadísticas de rendimiento de una campaña específica.",
        responses={200: 'Estadísticas de la campaña', 404: 'Campaña no encontrada'}
    )
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        campana = self.campanas_repo.obtener_por_id(pk)
        if campana:
            estadisticas = self.estadisticas_repo.calcular_estadisticas(campana)
            return Response(estadisticas)
        else:
            return Response({'error': 'Campaña no encontrada'}, status=status.HTTP_400_BAD_REQUEST)
                            
# CRUD para clientes utilizando el repositorio
class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClienteSerializer

    def get_queryset(self):
        # Si necesitas filtrar o ordenar los clientes, puedes hacerlo aquí
        return Cliente.objects.all()


class EstadisticaCampanaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EstadisticaCampana.objects.all()
    serializer_class = EstadisticaCampanaSerializer


# Vista para importar datos desde CSV
class ImportarDatosView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        csv_file = request.FILES['csv_file']

        # Validar el archivo
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'El archivo debe tener extensión .csv'}, status=status.HTTP_400_BAD_REQUEST)

        # Procesar el archivo
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        # Campos requeridos y tipos de datos
        required_fields = ['nombre', 'email', 'telefono', 'usuario']
        field_types = {
            'nombre': str,
            'email': str,
            'telefono': str,
            'usuario': int  # Asumiendo que el usuario se identifica por un ID numérico
        }

        # Lista para almacenar errores
        errors = []

        #Valida el csv
        for row_index, row in enumerate(reader, start=1):
            try:
                # Validar campos requeridos existan y no esten vacios
                for field in required_fields:
                    if field not in row or not row[field]:
                        raise ValueError(f"El campo '{field}' es obligatorio en la fila {row_index}")

                # Validar tipos de datos y convierte con field_type si es necesario
                for field, field_type in field_types.items():
                    if field in row and row[field]:
                        row[field] = field_type(row[field])

                # Obtener el objeto Usuario correspondiente
                usuario = Usuario.objects.get(id=row['usuario'])

                # Crear o actualizar el objeto Cliente
                cliente, created = Cliente.objects.update_or_create(
                    nombre=row['nombre'],
                    email=row['email'],
                    telefono=row['telefono'],
                    usuario=usuario,
                    defaults={
                        # Valores por defecto si el cliente no existe
                    }
                )
            except ValueError as e:
                errors.append(f"Error en la fila {row_index}: {e}")
            except Usuario.DoesNotExist:
                errors.append(f"Error en la fila {row_index}: El usuario con ID {row['usuario']} no existe")

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Datos importados con éxito'})


# INTEGRACION G CALENDAR

class CalendarView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def fetch_events(request):
    try:
        # Autenticacion con api Google Calendar
        creds = Credentials.from_authorized_user_file(
            'token.json')  # Path to your token file
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Creacion del servicio de la api
        service = build('calendar', 'v3', credentials=creds)

        # Extraer eventos de Google Calendar
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events_data = events_result.get('items', [])

        # Guardar eventos en la base de datos
        for event_data in events_data:
            start_time = event_data['start'].get(
                'dateTime', event_data['start'].get('date'))
            end_time = event_data['end'].get(
                'dateTime', event_data['end'].get('date'))
            start_time = datetime.datetime.fromisoformat(start_time)
            end_time = datetime.datetime.fromisoformat(end_time)
            Event.objects.create(
                summary=event_data.get('summary', ''),
                start_time=start_time,
                end_time=end_time
            )

        #Extraer y mostrar eventos desde la base de datos.
        events = Event.objects.all()
        context = {'events': events}
        return render(request, 'calendar_integration/calendar_events.html', context)

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")