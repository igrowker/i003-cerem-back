from rest_framework import status
from transformers import pipeline
from ..models import Campana, EstadisticaCampana, Usuario
from ..serializers import CampanaSerializer
from ..repositories.CampanaRepository import CampanaRepository  # Importa la clase
import logging
from datetime import timedelta
from django.db import IntegrityError 
from django.core.exceptions import ObjectDoesNotExist

class CampanaService:
    def __init__(self):
        self.generador_texto = pipeline("text-generation", model="facebook/bart-large-cnn")
        self.campana_repository = CampanaRepository()

    def calcular_rendimiento(self, estadistica ):
        # Lógica para calcular el rendimiento utilizando las estadísticas
        rendimiento = (estadistica.tasa_apertura + estadistica.tasa_conversion) / 2
        return rendimiento

    def crear_campana_con_contenido(self, data):
        serializer = CampanaSerializer(data=data)

        if serializer.is_valid():
            usuario_id = data.get('usuario')

            try:
                usuario = Usuario.objects.get(pk=usuario_id)

                campana = Campana(
                    nombre=serializer.validated_data['nombre'],
                    descripcion=serializer.validated_data['descripcion'],
                    usuario=usuario,
                    fecha_creacion=serializer.validated_data['fecha_creacion'],
                    fecha_inicio=serializer.validated_data['fecha_inicio']
                )

                duracion_campana = 1
                prompt = f"Generar contenido creativo y persuasivo para una campaña de marketing sobre {campana.nombre}. El tono debe ser {campana.descripcion} y la longitud máxima {duracion_campana} días."
                contenido = self.generador_texto(prompt, max_new_tokens=30)[0]['generated_text']
                campana.contenido = contenido
                campana.save()

                # Intenta obtener la EstadisticaCampana existente
                estadistica = EstadisticaCampana.objects.filter(campana=campana). first()

                if estadistica is None:
                    # Crea una nueva EstadisticaCampana si no existe
                    estadistica = EstadisticaCampana.objects.create(
                        campana=campana,
                        tasa_apertura=0.0,
                        tasa_conversion=0.0,
                        clicks=0
                    )

                # Asigna la EstadisticaCampana a la campaña
                campana.rendimiento = estadistica
                campana.save()

                return serializer, status.HTTP_201_CREATED, {"message": "Campaña creada con éxito"}

            except Usuario.DoesNotExist:
                error_message = {"error": "El usuario proporcionado no existe."}
                return serializer, status.HTTP_400_BAD_REQUEST, error_message
            except Exception as e:
                logging.error(f"Error al crear la campaña: {e}")
                return serializer, status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)}
        else:
            logging.error(f"Error de validación al crear la campaña: {serializer.errors}")
            return serializer, status.HTTP_400_BAD_REQUEST, {"error": serializer.errors}