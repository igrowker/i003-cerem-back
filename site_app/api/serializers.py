from rest_framework import serializers
from .models import Tarea, Campana, Cliente, EstadisticaCampana, Event, Usuario
from cryptography import fernet



# Serializador para el modelo Tarea.
class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'  # Incluir todos los campos del modelo Tarea.

# Serializador para el modelo Campana.
class CampanaSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    fecha_inicio = serializers.DateTimeField(
        input_formats=['%d/%m/%Y'], 
        format=None,  
        required=False,  
    )
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Campana
        fields = '__all__'
        extra_kwargs = {
            'rendimiento': {'required': False}
        }
# Serializador para el modelo Cliente.
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'  # Incluir todos los campos del modelo Cliente.

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Descifrar los datos antes de devolverlos (si es necesario)
        # Asegúrate de que el atributo key exista en el modelo Cliente
        if hasattr(instance, 'key'):
            key = instance.key
            f = fernet(key)
            data['email'] = f.decrypt(instance.email_encriptado).decode('utf-8')
            data['telefono'] = f.decrypt(instance.telefono_encriptado).decode('utf-8')
        return data

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






class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario  # Indica que este serializer está asociado al modelo Usuario
        fields = ['id', 'nombre', 'email', 'password', 'is_staff']  # Campos que se incluirán en el serializer
        extra_kwargs = {
            'password': {'write_only': True}  # El campo password será solo para escritura, no se incluirá en las respuestas
        }

    def create(self, validated_data):
        # Sobrescribe el método create para manejar la creación de un nuevo usuario
        usuario = Usuario(**validated_data)  # Crea una instancia de Usuario con los datos validados
        usuario.set_password(validated_data['password'])  # Establece la contraseña de forma segura (encriptada)
        usuario.save()  # Guarda la nueva instancia de usuario en la base de datos
        return usuario  # Devuelve el usuario recién creado

class PredecirRendimientoSerializer(serializers.Serializer):
    tipo_campana = serializers.ChoiceField(choices=[
        ('email', 'Email Marketing'),
        ('google_ads', 'Google Ads'),
        ('social_media', 'Social Media'),
        ('banner', 'Banner Advertising'),
    ])
    fecha_inicio = serializers.DateField()
    fecha_finalizacion = serializers.DateField()
    presupuesto = serializers.FloatField()
    tamaño_audiencia = serializers.IntegerField()

    # Validación para asegurarse de que la fecha_finalización sea posterior a la fecha_inicio
    def validate(self, data):
        if data['fecha_finalizacion'] <= data['fecha_inicio']:
            raise serializers.ValidationError("La fecha de finalización debe ser posterior a la fecha de inicio.")
        return data