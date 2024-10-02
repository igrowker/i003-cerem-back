from rest_framework import status
from transformers import pipeline
from ..models import Campana, EstadisticaCampana
from ..serializers import CampanaSerializer
from ..repositories.CampanaRepository import CampanaRepository  # Importa la clase
import logging

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
        
        if not serializer.is_valid():
            logging.error(f"Error de validación al crear la campaña: {serializer.errors}")
            return serializer, status.HTTP_400_BAD_REQUEST, {"error": serializer.errors}

        try:
            campana = self.campana_repository.create(serializer.validated_data['nombre'], serializer.validated_data['descripcion'], serializer.validated_data['usuario'], serializer.validated_data['fecha_creacion'])

            prompt = f"Generar contenido creativo y persuasivo para una campaña de marketing sobre {campana.nombre}. El tono debe ser {campana.descripcion} y la longitud máxima {campana.fecha_inicio} días."
            contenido = self.generador_texto(prompt, max_length=campana.fecha_inicio.days)[0]['generated_text']

            campana.contenido = contenido

            # Crear una instancia de EstadisticaCampana y calcular el rendimiento
            estadistica = EstadisticaCampana.objects.create(
                campana=campana,
                tasa_apertura=0.0,  # Valor predeterminado
                tasa_conversion=0.0,  # Valor predeterminado
                clicks=0  # Valor predeterminado
            )
            campana.rendimiento = self.calcular_rendimiento(estadistica)

            self.campana_repository.actualizar_campana(campana, contenido=contenido, rendimiento=campana.rendimiento)

            return serializer, status.HTTP_201_CREATED, {"message": "Campaña creada con éxito"}
        except Exception as e:
            logging.error(f"Error al crear la campaña: {e}")
            return serializer, status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": str(e)}