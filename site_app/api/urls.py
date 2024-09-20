from django.urls import path, include
from rest_framework import routers
from api.controllers.EstadisticasController import EstadisticasCampanaViewSet
from api.controllers.ClienteController import ClienteViewSet
from api.controllers.CampanaController import CampanaViewSet
from api import views
from api.views.view import (
    TareaViewSet, 
    CampanaViewSet, 
    ClienteViewSet, 
    #AgregarClienteViewSet, 
    #EstadisticasCampanaViewSet, 
    ImportarDatosView,
    CalendarView,
    fetch_events
)

# Creamos un router para manejar las URLs de los ViewSets
router = routers.DefaultRouter()
router.register(r'campanas', CampanaViewSet)  
router.register(r'clientes', ClienteViewSet) 
router.register(r'tareas', TareaViewSet) 
router.register(r'calendar', CalendarView, basename='calendar')


urlpatterns = [
        
    # Permite importar datos de clientes desde un archivo CSV o similar.
    path('datos/importar/', ImportarDatosView.as_view(), name='importar_datos'),
    
    #                   GCALENDAR OAUTH
    path('fetch-events/', fetch_events, name='fetch_events'),
    path('', include('api.calendar_integration.urls')),

    # Incluye las rutas generadas por el router
    path('', include(router.urls)),  
   
]
