from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from cryptography.fernet import Fernet


# Gestor Usuarios Personalizados. 
class UserManager(BaseUserManager):
    def _create_user(self, email, nombre, password, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(
            email=email,
            nombre=nombre,
            is_staff=is_staff,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    # Crea User
    def create_user(self, email, nombre, password=None, **extra_fields):
        if not nombre:
            raise ValueError("Nombre is required")
        return self._create_user(email, nombre, password, False, **extra_fields)
    
    # Crea Super User
    def create_superuser(self, email, nombre, password=None, **extra_fields):
        return self._create_user(email, nombre, password, True, **extra_fields)

    def save(self, *args, **kwargs):
        # Generar una clave única para este cliente (si no existe)
        if not self.pk:
            key = Fernet.generate_key()
            self.key = key
        else:
            key = self.key

        # Cifrar el email y el teléfono
        f = Fernet(key)
        self.email_encriptado = f.encrypt(self.email.encode('utf-8'))
        self.telefono_encriptado = f.encrypt(self.telefono.encode('utf-8'))

        # Eliminar los campos originales
        del self.email
        del self.telefono

        super().save(*args, **kwargs)

class Usuario(AbstractBaseUser):
    class Meta:
        db_table = 'usuarios'

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self) -> str:
        return f"Usuario {self.id}. {self.email}"
    

# Clientes asociados a un User
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('api.Usuario', on_delete=models.CASCADE)

    class Meta:
        db_table = 'clientes'

    def clean(self):
        if not self.nombre:
            raise ValueError("Nombre is required")


# Tareas asignadas a User
class Tarea(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=50)
    usuario = models.ForeignKey('api.Usuario', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tareas'


# Campana gestionadas por User
class Campana(models.Model):
      # Definir las opciones como un enumerado
    EMAIL = 'email'
    GOOGLE_ADS = 'google_ads'
    SOCIAL_MEDIA = 'social_media'
    BANNER = 'banner'

    TIPO_CAMPANA_CHOICES = [
        (EMAIL, 'Email Marketing'),
        (GOOGLE_ADS, 'Google Ads'),
        (SOCIAL_MEDIA, 'Social Media'),
        (BANNER, 'Banner Advertising'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_finalizacion = models.DateField(null=True ,blank=True)
    usuario = models.ForeignKey('api.Usuario', on_delete=models.CASCADE)
    tipo_campana = models.CharField(max_length=50, choices=TIPO_CAMPANA_CHOICES, default=EMAIL)
    rendimiento = models.OneToOneField(
        'api.EstadisticaCampana', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='rendimiento'
    )
    clics_totales = models.IntegerField(default=0)
    conversiones_totales = models.IntegerField(default=0)
    google_calendar_event_id = models.CharField(max_length=255, null=True, blank=True)
    google_keep_note_id = models.CharField(max_length=255, null=True, blank=True)
    presupuesto = models.FloatField(null=True, blank=True)
    tamaño_audiencia = models.IntegerField(null=True, blank=True)  # target_audience_size

    class Meta:
        db_table = 'campanas'

    def clean(self):
        if not self.nombre:
            raise ValueError("Nombre is required")


# Estadisticas de la campana
class EstadisticaCampana(models.Model):
    id = models.AutoField(primary_key=True)
    campana = models.ForeignKey(
        'Campana', on_delete=models.CASCADE, related_name='estadisticas'
    )
    tasa_apertura = models.FloatField()
    tasa_conversion = models.FloatField()
    clicks = models.IntegerField()

    class Meta:
        db_table = 'estadisticasCampanas'
        

#                                                   GCALENDAR OAUTH
class Event(models.Model):
    summary = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.summary

class AuditLog(models.Model):
    campaign = models.ForeignKey(Campana, on_delete=models.CASCADE)
    user = models.ForeignKey('api.Usuario', on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    data_before = models.JSONField(null=True, blank=True)
    data_after = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
