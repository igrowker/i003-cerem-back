from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from .models import Clic, Campana,AuditLog


#Incrementa en 1 los clics guardados en la DB
@receiver(post_save, sender=Clic)
def actualizar_clics_campana(sender, instance, created, **kwargs):
    if created:
        campana = instance.campana
        campana.clics_totales += 1
        campana.save()

@receiver(post_save, sender=Campana)
def create_audit_log(sender, instance, created, **kwargs):
    if created:
        action = "create"
    else:
        action = "edit"
    AuditLog.objects.create(
        campaign=instance,
        user=instance.updated_by or instance.created_by,
        action=action,
        data_before=instance.data_before,
        data_after=instance.to_json()
    )

@receiver(pre_delete, sender=Campana)
def delete_audit_log(sender, instance, **kwargs):
    AuditLog.objects.create(
        campaign=instance,
        user=instance.updated_by or instance.created_by,
        action="delete",
        data_before=instance.to_json()
    )