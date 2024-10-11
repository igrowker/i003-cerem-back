from django.urls import path, include
from rest_framework import routers
from api.views import view
from .swagger import schema_view  # Importación correcta de schema_view desde swagger.py
from api.views.view import CustomTokenObtainPairView, CustomTokenRefreshView
from api.controllers.UsuarioController import UsuarioViewSet

# Routers para las vistas de la API
router = routers.DefaultRouter()
router.register(r'tareas', view.TareaViewSet, basename='tareas')
router.register(r'campanas', view.CampanaViewSet, basename='campanas')
router.register(r'clientes', view.ClienteViewSet, basename='clientes')
router.register(r'estadisticas-campanas', view.EstadisticaCampanaViewSet, basename='estadisticas-campanas')
router.register(r'usuarios', UsuarioViewSet)  # Esto crea los endpoints CRUD para Usuario

# URLs para la API
urlpatterns = [
    path('', include(router.urls)),
    path('campanas/<int:pk>/estadisticas/', view.CampanaEstadisticaViewSet.as_view({'get': 'estadisticas'}), name='campana-estadisticas'),
    path('importar-datos/', view.ImportarDatosView.as_view(), name='importar-datos'),
    # Swagger y Redoc para la documentación de la API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Rutas para autenticación JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    # Otras rutas personalizadas
    path('fetch-events/', view.fetch_events_view, name='fetch-events'),
]
