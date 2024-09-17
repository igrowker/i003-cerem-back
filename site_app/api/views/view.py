from rest_framework import viewsets, permissions,status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from services import EstadisticaCampanaService,CampanaService,ClienteService
from models import Tarea, Campana, Cliente, EstadisticaCampana,Usuario
from serializers import TareaSerializer, CampanaSerializer, ClienteSerializer, EstadisticaCampanaSerializer
from transformers import pipeline
import csv

#Funcionabilidades de la Tarea. Con post marca tareas completadas

class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    @action(detail=True, methods=['post'])
    def completar_tarea(self, request, pk=None):
        tarea = self.get_object()
        tarea.completado = True
        tarea.save()
        return Response({'message': 'Tarea completada'})

class CampanaCrearViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        campana_service = CampanaService()
        data = request.data
        try:
            serializer = campana_service.crear_campana_con_inhaltdo(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CampanaEstadisticaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        campana = self.get_object()
        estadistica_service = EstadisticaCampanaService()
        estadisticas = estadistica_service.calcular_estadisticas(campana)
        return Response(estadisticas)
    
    @action(detail=True, methods=['post'])
    def generar_contenido(self, request, pk=None):
        campana = self.get_object()
        generador_texto = pipeline("text-generation", model="gpt2")
        prompt = f"Generar contenido para una campaña de marketing sobre {campana.tema}"
        contenido = generador_texto(prompt, max_length=100)[0]['generated_text']
        # Actualizar la campaña con el contenido generado
        campana.contenido = contenido
        campana.save()
        return Response({'message': 'Contenido generado con éxito'})

#CRUD para clientes con acceso limitado a user Autenticado
class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

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
