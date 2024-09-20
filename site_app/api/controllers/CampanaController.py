from argparse import Action
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import APIException

migrationTest
from ..models import Campana
from ..serializers import CampanaSerializer
from ..services import CampanaService
from transformers import pipeline


class CampanaContentGenerationError(APIException):
    pass


class CampanaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Campana.objects.all()
    serializer_class = CampanaSerializer

    def __init__(self, **kwargs):
        self.campana_service = CampanaService()
        super().__init__(**kwargs)

    @Action(detail=True, methods=['post'])
    def generar_contenido(self, request, pk=None):
        campana = self.get_object()
        try:
            contenido = self.campana_service.generar_contenido(campana)
            campana.contenido = contenido
            campana.save()
            return Response(CampanaSerializer(campana).data)
        except CampanaContentGenerationError as e:
            raise APIException(str(e))
        


