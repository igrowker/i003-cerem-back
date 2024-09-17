from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.EstadisticasService import EstadisticaCampanaService

#Controlador que maneja los endpoints relacionados con las estadisticas de campaña

class EstadisticasCampanaViewSet(APIView):
    estadisticas_service = EstadisticaCampanaService()

    def get(self, request, campana_id):
        # Obtener las estadisticas de una campaña especifica
        estadisticas = self.estadisticas_service.obtener_estadisticas(campana_id)
        if estadisticas:
            data = {
                "tasa_apertura": estadisticas.tasa_apertura,
                "tasa_conversion": estadisticas.tasa_conversion,
                "clicks": estadisticas.clicks
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "No se encontraron estadísticas"}, status=status.HTTP_404_NOT_FOUND)