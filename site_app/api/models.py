# Create your models here.
from django.db import models

# Modelo para representar a los usuarios del CRM.
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)  # Identificador único del usuario.
    nombre = models.CharField(max_length=255)  # Nombre del usuario.
    email = models.EmailField(unique=True)  # Correo electrónico, único para cada usuario.
    password = models.CharField(max_length=255)  # Contraseña del usuario.

# Modelo para las tareas, que se sincronizan con Google Calendar y Keep.
class Tarea(models.Model):
    id = models.AutoField(primary_key=True)  # Identificador único de la tarea.
    descripcion = models.CharField(max_length=255)  # Descripción breve de la tarea.
    fecha = models.DateTimeField()  # Fecha y hora de la tarea.
    estado = models.CharField(max_length=50)  # Estado de la tarea (ej. pendiente, completada).
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario al que pertenece la tarea.

# Modelo para las campañas de marketing, asistidas por la IA Llama 2.
class Campana(models.Model):
    id = models.AutoField(primary_key=True)  # Identificador único de la campaña.
    nombre = models.CharField(max_length=255)  # Nombre de la campaña.
    descripcion = models.TextField()  # Descripción detallada de la campaña.
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la campaña.
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario que creó la campaña.
    rendimiento = models.OneToOneField('EstadisticaCampana', on_delete=models.CASCADE, null=True, blank=True)  # Estadísticas de rendimiento de la campaña.

# Modelo para los clientes, almacenando información relevante.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)  # Identificador único del cliente.
    nombre = models.CharField(max_length=255)  # Nombre del cliente.
    email = models.EmailField()  # Correo electrónico del cliente.
    telefono = models.CharField(max_length=20)  # Teléfono del cliente.
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de registro del cliente.
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario que agregó al cliente.

# Modelo para las estadísticas de rendimiento de las campañas.
class EstadisticaCampana(models.Model):
    id = models.AutoField(primary_key=True)  # Identificador único de la estadística.
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE)  # Campaña asociada a estas estadísticas.
    tasa_apertura = models.FloatField()  # Porcentaje de correos abiertos.
    tasa_conversion = models.FloatField()  # Porcentaje de conversiones (ej. ventas).
    clicks = models.IntegerField()  # Número total de clics en la campaña.
