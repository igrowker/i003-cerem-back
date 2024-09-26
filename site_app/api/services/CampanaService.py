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
        self.generador_texto = pipeline("text-generation", model="facebook/bart-large-cnn")
        self.campana_repository = CampanaRepository() 

    def crear_campana_con_contenido(self, data):
        serializer = CampanaSerializer(data=data)
        
        if not serializer.is_valid():  # Validación del serializer
            logging.error(f"Error de validación al crear la campaña: {serializer.errors}")
            return serializer, Status.HTTP_400_BAD_REQUEST, {"error": serializer.errors}

        try:
            campana = self.campana_repository.create(serializer.validated_data) 

            prompt = f"Generar contenido creativo y persuasivo para una campaña de marketing sobre {campana.tema}. El tono debe ser {campana.tono} y la longitud máxima {campana.longitud_maxima} palabras."
            contenido = self.generador_texto(prompt, max_length=campana.longitud_maxima)[0]['generated_text']

            campana.contenido = contenido
            self.campana_repository.update(campana.id, {'contenido': contenido})  

            return serializer, Status.HTTP_201_CREATED, {"message": "Campaña creada con éxito."}

        except Exception as e:
            logging.error(f"Error al generar contenido para la campaña {campana.id}: {str(e)}")
            return serializer, Status.HTTP_500_INTERNAL_SERVER_ERROR, {"error": "Error al generar el contenido de la campaña"}