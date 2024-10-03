from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from rest_framework import generics
from django.shortcuts import get_object_or_404
import csv
from ..services import EstadisticasService,CampanaService,ClienteService,google_calendarService 
from ..services.CampanaService import CampanaService
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

# Swagger Schema Configuration
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

#combina tarea,evento
from rest_framework import generics
from django.db.models import Q


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

#Combina tarea con evento
class TareaGoogleCalendarView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
     
    serializer_class = TareaSerializer
    def get_queryset(self):
        user = self.request.user  # Obtenemos el usuario actual

        # Construimos una consulta que une Tarea y Event
        queryset = Tarea.objects.filter(usuario=user).values(
            'id', 'descripcion' ,'fecha', 'estado', 'usuario_id'
        ).union(
            Event.objects.filter(usuario=user).values(
                'id', 'summary' ,'start_time', 'end_time' 
            )
        )
        return queryset

# TareaViewSet with Swagger Documentation
class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    # Inyectamos el repositorio de tareas en el constructor
    def __init__(self, *args, **kwargs):
        self.tareas_repo = TareasRepository.TareasRepository()
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
        campana_service = CampanaService()
        data = request.data.copy()
        usuario_id = data.pop('usuario', None)  

        try:
            if usuario_id is not None:
                usuario = Usuario.objects.get(pk=usuario_id)
                
                serializer, status_code, response_data = campana_service.crear_campana_con_contenido(data | {'usuario': usuario.id})

                if status_code == status.HTTP_201_CREATED:
                    return Response(serializer.data, status=status_code)
                else:
                    return Response(response_data, status=status_code)
            else:
                return Response({'error': 'Falta el ID del usuario'}, status=status.HTTP_400_BAD_REQUEST)
        except Usuario .DoesNotExist:
            return Response({'error': 'El usuario proporcionado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# CampanaCrearViewSet with Swagger Documentation
class CampanaCrearViewSet(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# CampanaEstadisticaViewSet with Swagger Documentation
class CampanaEstadisticaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

    # Inyectamos los repositorios de campañas y estadísticas en el constructor
    def __init__(self, *args, **kwargs):
        self.campanas_repo = CampanaRepository.CampanaRepository()
        self.estadisticas_repo = EstadisticasRepository.EstadisticasRepository()
        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Obtener estadísticas de una campaña",
        operation_description="Obtiene las estadísticas de rendimiento de una campaña específica.",
        responses={200: 'Estadísticas de la campaña', 404: 'Campaña no encontrada'}
    )
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        campana = self.campanas_repo.obtener_por_id(campana_id=pk)
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
    def __init__(self, *args, **kwargs):
       self.estadisticas_repo = EstadisticasRepository.EstadisticasRepository() # Inyecta el repositorio
       super().__init__(*args, **kwargs)
    def get_object(self):
        campana_id = self.kwargs['pk']
        campana = get_object_or_404(Campana, pk=campana_id)
        estadisticas = self.estadisticas_repo.calcular_estadisticas(campana)  
        return estadisticas

# Vista para importar datos desde CSV
class ImportarDatosView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            return Response({'error': 'El archivo debe ser un CSV válido.'}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        required_fields = ['nombre', 'email', 'telefono', 'usuario_id'] #! Usamos usuario_id
        clientes_a_crear = []
        errors = []

        for row_index, row in enumerate(reader, start=2):  # Empezamos desde la fila 2, ya que la 1 son headers
            try:
                # Validar campos requeridos
                for field in required_fields:
                    if field not in row or not row[field]:
                        raise ValueError(f"El campo '{field}' es obligatorio en la fila {row_index}.")

                # Obtener el usuario (asumiendo que 'usuario_id' es el ID del usuario en el CSV)
                usuario = Usuario.objects.get(id=int(row['usuario_id']))

                cliente = Cliente(
                    nombre=row['nombre'],
                    email=row['email'],
                    telefono=row['telefono'],
                    usuario=usuario
                )
                clientes_a_crear.append(cliente)

            except Usuario.DoesNotExist:
                errors.append(f"Error en la fila {row_index}: No existe un usuario con ID {row['usuario_id']}.")
            except ValueError as e:
                errors.append(f"Error en la fila {row_index}: {str(e)}")

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Cliente.objects.bulk_create(clientes_a_crear)
            return Response({'message': 'Datos importados con éxito.'}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': f'Error al importar datos: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


# INTEGRACION G CALENDAR

def fetch_events_view(request):
    calendar_service = google_calendarService ()
    events = calendar_service.fetch_events()
