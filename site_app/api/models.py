from django.db import models


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Tarea(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class Campana(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rendimiento = models.OneToOneField(
        'EstadisticaCampana', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='rendimiento'
    )


class EstadisticaCampana(models.Model):
    id = models.AutoField(primary_key=True)
    campana = models.ForeignKey(
        Campana, on_delete=models.CASCADE, related_name='estadisticas'
    )
    tasa_apertura = models.FloatField()
    tasa_conversion = models.FloatField()
    clicks = models.IntegerField()
