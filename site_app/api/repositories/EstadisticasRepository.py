from api.models import EstadisticaCampana

#Crea un repositorio para gestionar la persistencia y recuperacion de las estadisticas
class EstadisticasRepository:

    #Recupera estadisticas de una campaña especifica
    @staticmethod
    def obtener_estadisticas_por_campana(campana_id):
        return EstadisticaCampana.objects.filter(campana_id=campana_id)
    
    #Crea nuevas estadisticas para una campaña
    @staticmethod
    def crear_estadisticas(campana, tasa_apertura, tasa_conversion, clicks):
        estadistica = EstadisticaCampana.objects.create(
            campana=campana,
            tasa_apertura=tasa_apertura,
            tasa_conversion=tasa_conversion,
            clicks=clicks
        )
        return estadistica
        from .models import EstadisticaCampana

    def calcular_estadisticas(self, campana):
        try:
            estadistica = EstadisticaCampana.objects.get(campana=campana)
            return {
                'tasa_apertura': estadistica.tasa_apertura,
                'tasa_conversion': estadistica.tasa_conversion,
                'clicks': estadistica.clicks
            }
        except EstadisticaCampana.DoesNotExist:
            return None