from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from site_app.api.services.EstadisticasService import EstadisticasRepository


#Controlador que maneja los endpoints relacionados con las estadisticas de campaña

class EstadisticasCampanaViewSet(APIView):
    estadisticas_service = EstadisticasRepository()

    def get(self, request, campana_id):
        estadisticas = self.estadisticas_service.obtener_estadisticas_por_campana(campana_id)  # Cambia el nombre del método
        if estadisticas:
            data = {
                "tasa_apertura": estadisticas.tasa_apertura,
                "tasa_conversion": estadisticas.tasa_conversion,
                "clicks": estadisticas.clicks
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "No se encontraron estadísticas"}, status=status.HTTP_404_NOT_FOUND)