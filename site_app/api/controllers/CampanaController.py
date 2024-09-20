
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Campana
from ..serializers import CampanaSerializer
from ..services import CampanaService
from transformers import pipeline

class CampanaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

    def __init__(self, **kwargs):
        self.campana_service = CampanaService()
        super().__init__(**kwargs)

    @action(detail=True, methods=['post'])
    def generar_contenido(self, request, pk=None):
        campana = self.get_object()
        contenido = self.campana_service.generar_contenido(campana)
        campana.contenido = contenido
        campana.save()
        return Response({'message': 'Contenido generado con éxito'})