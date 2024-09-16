from django.db import models
from models import Campana

class EstadisticaService:
    def calcular_estadisticas(self, campana):
        # Lógica para calcular las estadísticas
        estadisticas = {
            'tasa_apertura': campana.email_enviados / campana.emails_totales if campana.emails_totales else 0,
            'ctr': campana.clics_totales / campana.email_enviados if campana.email_enviados else 0,
            'tasa_conversion': campana.conversiones_totales / campana.clics_totales if campana.clics_totales else 0
        }
        return estadisticas