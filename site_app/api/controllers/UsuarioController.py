from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Usuario
from ..serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()  # Obtiene todos los usuarios de la base de datos
    serializer_class = UsuarioSerializer  # Asocia el serializer correspondiente
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder a estos endpoints
