from django.urls import path, include
from rest_framework import routers,permissions
from api.controllers.EstadisticasController import EstadisticasCampanaViewSet
from rest_framework.routers import DefaultRouter
from api.controllers.ClienteController import ClienteViewSet
from api.controllers.CampanaController import CampanaViewSet
from api.controllers.UsuarioController import UsuarioViewSet
from api import views
from .views.view import TareaViewSet, CampanaViewSet,CampanaCrearViewSet, ClienteViewSet, AgregarClienteViewSet, EstadisticasCampanaViewSet, ImportarDatosView,CalendarView,fetch_events, TareaGoogleCalendarView, CustomTokenObtainPairView, CustomTokenRefreshView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Creamos un router para manejar las URLs de los ViewSets
router = routers.DefaultRouter()
router.register(r'campanas', CampanaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'tareas', TareaViewSet)
router.register(r'calendar', CalendarView, basename='calendar')
router.register(r'usuarios', UsuarioViewSet)  # Esto crea los endpoints CRUD para Usuario

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Tu API",
        default_version='v1',
        description="Descripción de tu API",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Permite importar datos de clientes desde un archivo CSV o similar.
    path('datos/importar/', ImportarDatosView.as_view(), name='importar_datos'), 
    # Integración con Google Calendar
    path('fetch-events/', fetch_events, name='fetch_events'),
    path('', include('api.calendar_integration.urls')),
    # Incluye las rutas generadas por el router
    path('', include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('api/tareas/', TareaGoogleCalendarView.as_view(), name='tarea-google-calendar-list'),
    path('api/estadisticas/campana/<int:pk>/', EstadisticasCampanaViewSet.as_view(), name='estadisticas-campana-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] 