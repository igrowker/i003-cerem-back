from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Definir el esquema de seguridad Bearer Token
schema_view = get_schema_view(
    openapi.Info(
        title="Mi API",
        default_version='v1',
        description="Documentación de la API",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
