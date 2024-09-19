from grpc import Status
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from models import Tarea
from serializers import TareaSerializer
from services import TareaService

class TareaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def __init__(self, *args, **kwargs):
        self.tarea_service = TareaService()  # Inyecta el servicio de tareas
        super().__init__(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tarea = self.tarea_service.crear_tarea(serializer.validated_data)  # Utiliza el servicio para crear la tarea
        return Response(self.get_serializer(tarea).data, status=Status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.tarea_service.eliminar_tarea(instance.id)  # Utiliza el servicio para eliminar la tarea
        return Response(status=Status.HTTP_204_NO_CONTENT)