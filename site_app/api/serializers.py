from rest_framework import serializers
from .models import Tarea, Campana, Cliente, EstadisticaCampana, Event
from cryptography import fernet



# Serializador para el modelo Tarea.
class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'  # Incluir todos los campos del modelo Tarea.

# Serializador para el modelo Campana.
class CampanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campana
        fields = '__all__'  # Incluir todos los campos del modelo Campana.

# Serializador para el modelo Cliente.
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__' 
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Descifrar los datos antes de devolverlos (si es necesario)
        key = instance.key
        f = fernet(key)
        data['email'] = f.decrypt(instance.email_encriptado).decode('utf-8')
        data['telefono'] = f.decrypt(instance.telefono_encriptado).decode('utf-8')
        return data # Incluir todos los campos del modelo Cliente.

# Serializador para el modelo EstadisticaCampana.
class EstadisticaCampanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadisticaCampana
        fields = '__all__'  # Incluir todos los campos del modelo EstadisticaCampana.

# Serializador para el modelo Event.
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'summary', 'start_time', 'end_time']