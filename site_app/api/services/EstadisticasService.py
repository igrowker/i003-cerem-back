from django.db import models, transaction
from ..models import EstadisticaCampana

class EstadisticasRepository:
    def obtener_estadisticas_por_campana(self, campana_id):
    
        try:
            return EstadisticaCampana.objects.get(campana__id=campana_id)
        except EstadisticaCampana.DoesNotExist:
            return None

    @transaction.atomic
    def crear_estadisticas(self, campana, tasa_apertura, tasa_conversion, clicks):
        estadistica = EstadisticaCampana(
            campana=campana,
            tasa_apertura=tasa_apertura,
            tasa_conversion=tasa_conversion,
            clicks=clicks
        )
        estadistica.save()
        return estadistica