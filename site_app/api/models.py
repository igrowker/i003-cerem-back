from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


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
    
    def create_user(self, email, name, password=None, **extra_fields):
        return self._create_user(email, name, password, False, **extra_fields)

    def create_superuser(self, email, name, password=None, **extra_fields):
        return self._create_user(email, name, password, True, **extra_fields)


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
