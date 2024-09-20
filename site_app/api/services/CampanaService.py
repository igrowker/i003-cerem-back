from grpc import Status
from transformers import pipeline
from ..models import Campana
from ..serializers import CampanaSerializer
from ..repositories import CampanaRepository  # Importar el repositorio
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import logging

class CampanaService:
    def __init__(self):
        self.generador_texto = pipeline("text-generation", model="llama-2")
        self.campana_repository = CampanaRepository()  # Instanciar el repositorio

    def crear_campana_con_contenido(self, data):
        serializer = CampanaSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            campana = self.campana_repository.create(serializer.validated_data)  # Crear la campaña a través del repositorio

            prompt = f"Generar contenido creativo y persuasivo para una campaña de marketing sobre {campana.tema}. El tono debe ser {campana.tono} y la longitud máxima {campana.longitud_maxima} palabras."
            contenido = self.generador_texto(prompt, max_length=100)[0]['generated_text']
            campana.contenido = contenido
            self.campana_repository.update(campana.id, {'contenido': contenido})  # Actualizar la campaña a través del repositorio

        except Exception as e:
            logging.error(f"Error al generar contenido para la campaña {campana.id}: {str(e)}")
            return serializer, Status.HTTP_400_BAD_REQUEST, {"error": "Error al generar el contenido de la campaña"}

        return serializer, Status.HTTP_201_CREATE