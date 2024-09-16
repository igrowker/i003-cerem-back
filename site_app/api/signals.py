from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Clic, Campana


#Incrementa en 1 los clics guardados en la DB
@receiver(post_save, sender=Clic)
def actualizar_clics_campana(sender, instance, created, **kwargs):
    if created:
        campana = instance.campana
        campana.clics_totales += 1
        campana.save()