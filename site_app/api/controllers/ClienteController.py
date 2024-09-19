from rest_framework.response import Response
from rest_framework import viewsets, permissions
from models import Cliente
from serializers import ClienteSerializer
from services import ClienteService

class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def __init__(self, **kwargs):
        self.cliente_service = ClienteService()
        super().__init__(**kwargs)