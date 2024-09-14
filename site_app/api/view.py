from rest_framework import viewsets, permissions,status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tarea, Campana, Cliente, EstadisticaCampana,Usuario
from .serializers import TareaSerializer, CampanaSerializer, ClienteSerializer, EstadisticaCampanaSerializer
from transformers import pipeline
import csv

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

class CampanaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        campana = self.get_object()
        # Calcular estadísticas de la campaña
        estadisticas = {
            'tasa_apertura': campana.email_enviados / campana.emails_totales,
            'ctr': campana.clics_totales / campana.email_enviados if campana.email_enviados > 0 else 0,
            'tasa_conversion': campana.conversiones_totales / campana.clics_totales if campana.clics_totales > 0 else 0
        }
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

        for row_index, row in enumerate(reader, start=1):
            try:
                # Validar campos requeridos
                for field in required_fields:
                    if field not in row or not row[field]:
                        raise ValueError(f"El campo '{field}' es obligatorio en la fila {row_index}")

                # Validar tipos de datos
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