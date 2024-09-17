from django.urls import path
from api.controllers.EstadisticasController import EstadisticasCampanaViewSet
from views.view import (
    TareasView, 
    CrearCampanaView, 
    ClientesView, 
    AgregarClienteView, 
    EstadisticasCampanaView, 
    ImportarDatosView
)
from . import views

urlpatterns = [
    # Devuelve las estadísticas y rendimiento de una campaña específica.
    path('estadisticas/campana/<int:campana_id>/', EstadisticasCampanaViewSet.as_view(), name='estadisticas_campana'),
    
    # Devuelve todas las tareas y eventos de Google Calendar y Keep.
    path('tareas/', TareasView.as_view(), name='tareas'), 
    
    # Permite crear una campaña de marketing asistida por IA (Llama 2).
    path('campana/crear/', CrearCampanaView.as_view(), name='crear_campana'),
    
    # Devuelve un listado de todos los clientes y sus datos en tiempo real.
    path('clientes/', ClientesView.as_view(), name='clientes'), 
    
    # Agrega un nuevo cliente al CRM.
    path('clientes/agregar/', AgregarClienteView.as_view(), name='agregar_cliente'),
    
        
    # Permite importar datos de clientes desde un archivo CSV o similar.
    path('datos/importar/', ImportarDatosView.as_view(), name='importar_datos'),
    
    #                   GCALENDAR OAUTH
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('fetch-events/', views.fetch_events, name='fetch_events'),
    
]
