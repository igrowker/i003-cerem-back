from api.repositories.EstadisticasRepository import EstadisticasRepository

#Implementa el servicio que recopila y procesa los datos de las campañas
class EstadisticaCampanaService:

    def obtener_estadisticas(self, campana_id):
        return EstadisticasRepository.obtener_estadisticas_por_campana(campana_id)

    def procesar_estadisticas(self, campana, tasa_apertura, tasa_conversion, clicks):
        # Procesa y guarda las estadisticas de la campaña
        return EstadisticasRepository.crear_estadisticas(
            campana, tasa_apertura, tasa_conversion, clicks
        )
    
