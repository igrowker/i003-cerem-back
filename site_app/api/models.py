from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from cryptography.fernet import Fernet
#Gestor Usuarios Personalizados. 
class UserManager(BaseUserManager):

    def _create_user(self, email, name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email=email,
            name=name,
            is_staff=is_staff,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    #Crea User
    def create_user(self, email, name, password=None, **extra_fields):
        return self._create_user(email, name, password, False, **extra_fields)

    #Crea Super User
    def create_superuser(self, email, name, password=None, **extra_fields):
        return self._create_user(email, name, password, True, **extra_fields)

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
    

#Clientes asociados a un User
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'clientes'


#Tareas asignadas a User
class Tarea(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tareas'


#Campana gestionadas por User
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
    clics_totales = models.IntegerField(default=0)
    conversiones_totales = models.IntegerField(default=0)
    # Campos para almacenar información relacionada con Google Calendar y Keep (opcional)
    google_calendar_event_id = models.CharField(max_length=255, null=True, blank=True)
    google_keep_note_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'campanas'


#Estadisticas de la campana
class EstadisticaCampana(models.Model):
    id = models.AutoField(primary_key=True)
    campana = models.ForeignKey(
        Campana, on_delete=models.CASCADE, related_name='estadisticas'
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