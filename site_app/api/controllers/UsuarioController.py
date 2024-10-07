from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action  # Importar el decorador
from ..models import Usuario
from ..serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()  # Obtiene todos los usuarios de la base de datos
    serializer_class = UsuarioSerializer  # Asocia el serializer correspondiente
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder a estos endpoints

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_password(self, request, pk=None):
        usuario = self.get_object()
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"error": "New password required."}, status=status.HTTP_400_BAD_REQUEST)

        usuario.set_password(new_password)
        usuario.save()
        return Response({"message": "Password updated successfully."}, status=status.HTTP_204_NO_CONTENT)
