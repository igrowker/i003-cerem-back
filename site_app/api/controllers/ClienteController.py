from rest_framework import viewsets, permissions
from ..models import Cliente
from ..serializers import ClienteSerializer
from ..services import ClienteService

from rest_framework.response import Response


class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClienteSerializer

    def get_queryset(self):
        # Si necesitas filtrar o ordenar los clientes, puedes hacerlo aquí
        return Cliente.objects.all()

    def create(self, request):
        cliente_service = ClienteService()
        cliente = cliente_service.crear_cliente(request.data)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        cliente_service = ClienteService()
        cliente = cliente_service.obtener_cliente(pk)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    def update(self, request, pk=None):
        cliente_service = ClienteService()
        cliente = cliente_service.actualizar_cliente(pk, request.data)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        cliente_service = ClienteService()
        cliente_service.eliminar_cliente(pk)
        return Response(status=204)