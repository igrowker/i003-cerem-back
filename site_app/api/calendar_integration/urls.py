from django.urls import path
from .views import fetch_events  # Asegúrate de que esto apunte correctamente a fetch_events

urlpatterns = [
    path('fetch-events/', fetch_events, name='fetch_events'),
]
