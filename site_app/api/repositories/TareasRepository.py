from django.db import models
from models import Tarea

class TareasRepository:
    def __init__(self):
        self.model=Tarea
    
    def crear_tarea(self,descripcion,fecha,estado,usuario):
        nueva_tarea=self.model(descripcion=descripcion,fecha=fecha,estado=estado,usuario=usuario)
        nueva_tarea.save()
        return nueva_tarea
    
    def obtener_tarea(self,usuario=None,estado=None):
        query=self.model.objects.all()
        if usuario:
            query=query.filter(usuario=usuario)
        if estado:
            query=query.filter(estado=estado)
        return query
    
    def obtener_tarea_por_id(self, tarea_id):
        try:
            return self.model.objects.get(pk=tarea_id)
        except self.model.DoesNotExist:
            return None

    def actualizar_tarea(self, tarea, descripcion=None, fecha=None, estado=None):
        if descripcion:
            tarea.descripcion = descripcion
        if fecha:
            tarea.fecha = fecha
        if estado:
            tarea.estado = estado
        tarea.save()
        return tarea

    def eliminar_tarea(self, tarea_id):
        try:
            tarea = self.model.objects.get(pk=tarea_id)
            tarea.delete()
            return True
        except self.model.DoesNotExist:
            return False