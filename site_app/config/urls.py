"""
URL configuration for site_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from api.views import view
from .swagger import schema_view

# Routers para las vistas de la API
router = routers.DefaultRouter()
router.register(r'tareas', view.TareaViewSet, basename='tareas')
router.register(r'campanas', view.CampanaViewSet, basename='campanas')
router.register(r'clientes', view.ClienteViewSet, basename='clientes')
router.register(r'estadisticas-campanas', view.EstadisticaCampanaViewSet, basename='estadisticas-campanas')

# URLs para la API
urlpatterns = [
    path('', include(router.urls)),
    path('campanas/crear/', view.CampanaCrearViewSet.as_view(), name='campana-crear'),
    path('campanas/<int:pk>/estadisticas/', view.CampanaEstadisticaViewSet.as_view({'get': 'estadisticas'}), name='campana-estadisticas'),
    path('importar-datos/', view.ImportarDatosView.as_view(), name='importar-datos'),
    path('swagger/', view.schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('fetch-events/', view.fetch_events_view, name='fetch-events'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]